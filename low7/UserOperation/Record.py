from PyQt5.QtGui import QPixmap
import time, sqlite3
import cv2, sys, datetime
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserInterface import Logon_win, Forget_win, Function_win


# 用户登录操作类
class Record():
    def __init__(self, win):
        super(Record, self).__init__()
        self.face = None
        self.window = win

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        if fingers is not None:
            print(fingers)
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 75 < x < 175 and 270 < y < 340:
                    # 上一步
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.number = self.data[-1]
                            self.window.usrLineEdit.setText(self.number)
                            self.data = self.data[:-1]
                        else:
                            self.number = ''
                            self.window.usrLineEdit.setText(self.number)
                            self.data = []
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请您把账号分段输入，再输入确定！！")
                    elif sign == 2:
                        if len(self.data1) > 0:
                            self.passw = self.data1[-1]
                            self.window.pwdLineEdit.setText(self.passw)
                            self.data1 = self.data1[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请您把密码分段输入，再输入确定！！")
                        else:
                            self.passw = ''
                            self.window.pwdLineEdit.setText(self.passw)
                            self.data1 = []
                            self.sign = 1
                            self.number = self.data[-1]
                            self.window.usrLineEdit.setText(self.number)
                            self.data = self.data[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请您把账号分段输入，再输入确定！！")
                elif 250 < x < 350 and 270 < y < 340:
                    # 确定
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()

                elif 425 < x < 525 and 270 < y < 340:
                    # 退出
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：退出\n\t操作成功")
                    time.sleep(1)
                    try:
                        self.window.timer_next.stop()
                        self.window.timer_camera.stop()
                        self.window.self_cap.release()  # 释放视频流
                        self.window.newlab.clear()
                    except:
                        pass
                    UserOperation.win.close()
                    sys.exit()
                elif 75 < x < 175 and 410 < y < 480:
                    # 忘记密码
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：忘记密码\n\t操作成功")
                    time.sleep(1)
                    self.forgetfun()
                elif 250 < x < 350 and 410 < y < 480:
                    # 登录
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：登录\n\t操作成功")
                    time.sleep(1)
                    self.accept()

                elif 425 < x < 525 and 410 < y < 480:
                    # 注册
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：注册\n\t操作成功")
                    time.sleep(1)
                    self.logonfun()

    # 识别操作区的手写文字
    def contrast_answer(self):
        self.window.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.window.setextlab.setText("正在识别输入中．．")
        self.window.progresslab.clear()
        self.window.progresslab.setMovie(self.window.movie)
        self.window.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    # 将操作区识别出来的文字写入界面
    def contrast_answer_right(self):
        self.window.movie.stop()
        self.window.progresslab.clear()
        self.window.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.window.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.window.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if len(self.number) < 11:
                if data[1] > 0.6:
                    try:
                        da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                    except:
                        da = data[0]
                    self.data.append(self.number)
                    self.number = self.number + da
                    self.window.usrLineEdit.setText(self.number)
                    self.window.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t"
                                                   + "如果输入错误请您手指指在＇上一步＇操作！！")
            if len(self.number) != 11:
                pass
            elif self.checking1():
                self.window.messagelab.setText("提示!\n\t" +
                                               "您输入的号码未注册！\n\t请您先注册！")
            else:
                self.window.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入密码\n\t" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.window.pwdLineEdit.setText(self.passw)
                self.window.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作！！")
        time.sleep(1)
        self.window.start(200)

    # 连接注册界面
    def logonfun(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
            self.window.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Logon_win.Logon_win())

    # 登录时检验号码是否没有注册
    def checking1(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.window.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    # 登录时判断密码是否正确
    def accept(self):
        if len(self.window.usrLineEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.window.usrLineEdit.text()) != 11:
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif self.checking1():
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            self.sign = 1
        elif len(self.window.pwdLineEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            d = 0
            for variate in c.fetchall():
                if variate[0] == self.window.usrLineEdit.text() \
                        and variate[2] == self.window.pwdLineEdit.text():
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:  # 连接主界面函数
                try:
                    self.window.timer_next.stop()
                    self.window.timer_camera.stop()
                    self.window.self_cap.release()  # 释放视频流
                    self.window.newlab.clear()
                except:
                    pass
                UserOperation.number = self.window.usrLineEdit.text()
                self.finddata()
                UserOperation.win.splitter.widget(0).setParent(None)
                UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())
            else:
                self.window.messagelab.setText("提示!\n\t" + "账号或密码输入错误")

    # 连接忘记密码界面
    def forgetfun(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
            self.window.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Forget_win.Forget_win())

    # 保存用户的登录时间
    def finddata(self):
        time1 = datetime.datetime.now()
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date")
        for variate in c.fetchall():
            if variate[0] == UserOperation.number:
                abcd = '%Y-%m-%d %H:%M:%S'
                b = datetime.datetime.strptime(variate[4], abcd)
                theTime = time1.strftime(abcd)
                if b.year == time1.year and b.month == time1.month and b.day == time1.day:
                    a = variate[2]
                else:
                    a = variate[2] + 1
                c.execute("update Student_date set logonday=(?),lasttime = (?) where number = (?)",
                          (a, theTime, UserOperation.number))
                conn.commit()
                break
        c.close()
        conn.close()
