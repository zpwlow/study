from PyQt5.QtGui import QPixmap
import time, sqlite3
import cv2
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserInterface import Record_win, User_informent_win


# 用户注册操作类
class Logon:
    def __init__(self, win):
        super(Logon, self).__init__()
        self.window = win

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        print(fingers)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 125 < x < 225 and 270 < y < 340:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                    self.change_record()
                elif 375 < x < 475 and 270 < y < 340:
                    # 上一步
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.number = self.data[-1]
                            self.window.usrLine.setText(self.number)
                            self.data = self.data[:-1]
                        else:
                            self.number = ''
                            self.window.usrLine.setText(self.number)
                            self.data = []
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请您把账号分段输入，再输入确定！！")
                    elif sign == 2:
                        self.number = self.data[-1]
                        self.window.usrLine.setText(self.number)
                        self.data = self.data[:-1]
                        self.sign = 1
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请您把账号分段输入，再输入确定！！")
                    elif sign == 3:
                        if len(self.data1) > 0:
                            self.passw = self.data1[-1]
                            self.window.pwdLineEdit1.setText(self.passw)
                            self.data1 = self.data1[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请您把密码输入后，再输入确定！！")
                        else:
                            self.passw = ''
                            self.window.pwdLineEdit1.setText(self.passw)
                            self.data1 = []
                            self.window.usrnameLine.setText("")
                            self.sign = 2
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请您把用户名输入后，再输入确定！！")
                elif 125 < x < 225 and 410 < y < 480:
                    # 确定
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()
                elif 375 < x < 475 and 410 < y < 480:
                    # 注册
                    self.window.messagelab.setText("提示!\n" + "本次操作为：注册\n操作成功")
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
                    self.window.usrLine.setText(self.number)
                    self.window.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t" +
                                                   "如果输入错误请您在操作区输入＇上一步＇操作！！")
            if len(self.number) != 11:
                pass
            elif self.checking1():
                self.window.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n请您先登录！")
            else:
                self.window.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入昵称\n\t" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            self.window.usrnameLine.setText(data[0])
            self.window.messagelab.setText("提示!\n\t" + "用户名输入成功！请您输入密码(每次输入的数字不能超过四位数)\n\t" +
                                           "如果输入错误请您在操作区输入＇上一步＇操作！！")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.window.pwdLineEdit1.setText(self.passw)
                self.window.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                               "如果输入错误请您在操作区输入＇上一步＇操作！！")
        time.sleep(1)
        self.window.timer_next.start(200)

    # 注册时输入的号码检验是否已经注册过的
    def checking1(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.window.usrLine.text():
                return True
        c.close()
        conn.close()
        return False

    # 登录时密码在数据库中保存过来
    def save_data(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        a = self.window.usrLine.text()
        b = self.window.usrnameLine.text()
        c = self.window.pwdLineEdit1.text()
        conn.execute("INSERT INTO User VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    # 注册时将账号密码保存并登录。
    def accept(self):
        if len(self.window.usrLine.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.window.usrLine.text()) != 11:
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif self.checking1():
            self.window.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n\t请您登录！")
            self.sign = 1
        elif len(self.window.usrnameLine.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "用户名不能为空！")
            self.sign = 2
        elif len(self.window.pwdLineEdit1.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            try:
                self.window.timer_next.stop()
                self.window.timer_camera.stop()
                self.window.self_cap.release()  # 释放视频流
                self.window.newlab.clear()
            except:
                pass
            UserOperation.number = self.window.usrLine.text()
            self.save_data()
            UserOperation.win.splitter.widget(0).setParent(None)
            UserOperation.win.splitter.insertWidget(0, User_informent_win.User_informent_win())
            # 连接主窗口界面。

    # 连接用户登录界面
    def change_record(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
            self.window.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Record_win.Record_win())
