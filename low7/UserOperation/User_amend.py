import cv2
import sqlite3
import time
import UserOperation
from UserInterface import User_Myself_win
from UserOperation import ContrastJob
from UserOperation.FingerDetection import figer_number


class User_amend:
    def __init__(self, win):
        super(User_amend, self).__init__()
        self.window = win
        self.sign = 1
        self.passw1 = ''
        self.passw2 = ''
        self.data = []
        self.data1 = []

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        if fingers is not None:
            # print(fingers)
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 75 < x < 175 and 270 < y < 340:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_Myself_win.User_Myself_win())
                elif 250 < x < 350 and 270 < y < 340:
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()
                    # 确定
                elif 425 < x < 525 and 270 < y < 340:
                    # 修改
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：修改\n\t操作成功")
                    self.accept()
                elif 75 < x < 175 and 410 < y < 480:
                    # 上一步
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.passw1 = self.data[-1]
                            self.window.amendedit1.setText(self.passw1)
                            self.data = self.data[:-1]
                        else:
                            self.passw1 = ''
                            self.window.amendedit1.setText(self.passw1)
                            self.data = []
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把原密码分段输入输入区后，再在操作区输入确定！！")
                    elif sign == 2:
                        if len(self.data1) > 0:
                            self.passw2 = self.data1[-1]
                            self.window.amendedit2.setText(self.passw2)
                            self.data1 = self.data1[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请把新密码分段输入输入区后，再在操作区输入确定！！")
                        else:
                            self.passw2 = ''
                            self.window.amendedit2.setText(self.passw2)
                            self.data1 = []
                            self.sign = 1
                            self.passw1 = self.data[-1]
                            self.window.amendedit1.setText(self.passw1)
                            self.data = self.data[:-1]
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "请把原密码分段输入输入区后，再在操作区输入确定！！")
                elif 250 < x < 350 and 410 < y < 480:
                    # 下一步
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：下一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        self.sign = 2
                    elif sign == 2:
                        self.accept()

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()

    def contrast_answer(self):
        self.window.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.window.setextlab.setText("正在识别输入中．．")
        self.window.progresslab.setMovie(self.window.movie)
        self.window.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob.ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def contrast_answer_right(self):
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.window.amendedit1.setText(self.passw)
                self.window.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                               "如果输入错误请您在操作区输入上一步操作！\n\t输入完整后可输入下一步")
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.window.amendedit1.setText(self.passw)
                self.window.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                               "如果输入错误请您在操作区输入上一步操作!\n\t输入完整后可输入登录")
        time.sleep(1)
        self.window.timer_next.start(200)

    def accept(self):
        if len(self.window.amendedit1.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "原密码没有填写")
        elif len(self.window.amendedit2.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif len(self.window.amendedit3.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif self.window.amendedit3.text() != self.window.amendedit2.text():
            self.window.messagelab.setText("提示!\n\t" + "前后密码输入不一样！")
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            sign = 0
            for variate in c.fetchall():
                if variate[0] == UserOperation.number and variate[2] == self.window.amendedit1.text():
                    conn.execute("update User set password=(?) where number=(?)",
                                 (self.window.amendedit2.text(), variate[0],))
                    conn.commit()
                    sign = 1
                    break
            c.close()
            conn.close()
            if sign == 0:
                self.window.messagelab.setText("提示!\n\t" + "原密码输入错误！！")
                self.sign = 1
            else:
                self.window.messagelab.setText("提示!\n\t" + "修改成功！！")
                try:
                    self.window.timer_next.stop()
                    self.window.timer_camera.stop()
                    self.window.self_cap.release()  # 释放视频流
                    self.window.newlab.clear()
                except:
                    pass
                time.sleep(1)
                UserOperation.win.splitter.widget(0).setParent(None)
                UserOperation.win.splitter.insertWidget(0, User_Myself_win.User_Myself_win())
