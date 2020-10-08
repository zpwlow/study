from PyQt5.QtGui import QPixmap
import time, sqlite3
import cv2, datetime
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserInterface import Record_win, Function_win


class Forget:
    def __init__(self, win):
        super(Forget, self).__init__()
        self.window = win

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 125 < x < 225 and 270 < y < 340:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功!")
                    self.return_record()
                elif 375 < x < 475 and 270 < y < 340:
                    # 上一步
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功!")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.number = self.data[-1]
                            self.window.usrLineEdit2.setText(self.number)
                            self.data = self.data[:-1]
                        else:
                            self.number = ''
                            self.window.usrLineEdit2.setText(self.number)
                            self.data = []
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把账号分段输入输入区后，再在操作区输入确定！！")
                    elif sign == 2:
                        if len(self.data1) > 0:
                            self.passw = self.data1[-1]
                            self.window.pwdLineEdit2.setText(self.passw)
                            self.data1 = self.data1[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请把密码分段输入输入区后，再在操作区输入确定！！")
                        else:
                            self.passw = ''
                            self.window.pwdLineEdit2.setText(self.passw)
                            self.data1 = []
                            self.sign = 1
                            self.number = self.data[-1]
                            self.window.usrLineEdit2.setText(self.number)
                            self.data = self.data[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请把账号分段输入输入区后，再在操作区输入确定！！")
                elif 125 < x < 225 and 410 < y < 480:
                    # 确定
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功!")
                    self.contrast_answer()
                elif 375 < x < 475 and 410 < y < 480:
                    # 注册
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：修改\n\t操作成功")
                    self.accept()

    # 识别操作区的手写文字
    def contrast_answer(self):
        self.window.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.window.setextlab.setText("正在识别输入中．．")
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
                    self.window.usrLineEdit2.setText(self.number)
                    self.window.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n" +
                                                   "如果输入错误请您在操作区输入＇上一步＇操作")
            if len(self.number) != 11:
                pass
            elif self.checking1():
                self.window.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n请您先注册！")
            else:
                self.window.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入密码\n" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作")
                self.sign = 2
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.window.pwdLineEdit2.setText(self.passw)
                self.window.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作")
        time.sleep(1)
        self.window.timer_next.start(200)

    # 忘记密码时检验号码是否没有注册
    def checking1(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.window.usrLineEdit2.text():
                return False
        c.close()
        conn.close()
        return True

    # 忘记密码时将新的密码在数据库中修改过来
    def savedate(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.window.usrLineEdit2.text():
                UserOperation.number = variate[0]
                conn.execute("update User set password=(?) where number=(?)",
                             (self.window.pwdLineEdit2.text(), variate[0],))
                break
        conn.commit()
        c.close()
        conn.close()

    # 忘记密码时验证是否可以登录
    def accept(self):
        if len(self.window.usrLineEdit2.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.window.usrLineEdit2.text()) != 11:
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif self.checking1():
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            self.sign = 1
        elif len(self.window.pwdLineEdit2.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            self.savedate()
            self.finddata()
            try:
                self.window.timer_next.stop()
                self.window.timer_camera.stop()
                self.window.self_cap.release()  # 释放视频流
                self.window.newlab.clear()
            except:
                pass
            # 设置一个查询用户年级的函数
            UserOperation.win.splitter.widget(0).setParent(None)
            UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())
            # 连接主窗口界面。

    # 返回登录界面
    def return_record(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
            self.window.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Record_win.Record_win())

    # 保存用户登录时间
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
