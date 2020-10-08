import base64
import sqlite3
import time
import cv2
import datetime
from PyQt5.QtGui import QPixmap
import UserOperation
from UserInterface import Function_win
from UserOperation.ContrastJob import ContrastJob
from UserOperation.FingerDetection import figer_number


class User_informent:
    def __init__(self, win):
        super(User_informent, self).__init__()
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
                if 75 < x < 175 and 320 < y < 390:
                    # 完成
                    self.window.messagelab.setText("提示!\n\t"
                                                   + "本次操作为：完成\n\t操作成功!")
                    self.connect_fun()
                elif 250 < x < 350 and 320 < y < 390:
                    # 上一步
                    self.window.messagelab.setText("提示!\n\t"
                                                   + "本次操作为：上一步\n\t操作成功!")
                    sign = self.sign
                    if sign == 1:
                        self.window.nameEdit.setText("")
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的姓名输入输入区后，再在操作区输入确定！！")
                    elif sign == 2:
                        self.window.nameEdit.setText("")
                        self.sign = 1
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的姓名输入输入区后，再在操作区输入确定！！")
                    elif sign == 3:
                        self.window.sexEdit.setText("")
                        self.sign = 2
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的性别输入输入区后，再在操作区＇输入确定！！")
                    elif sign == 4:
                        self.window.yearEdit.setText("")
                        self.sign = 3
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的出生年月输入输入区后，再在操作区输入确定！！")
                    elif sign == 5:
                        self.window.schoolEiit.setText("")
                        self.sign = 4
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的学校输入输入区后，再在操作区输入确定！！")
                    elif sign == 6:
                        self.window.gradeEdit.setText("")
                        self.sign = 5
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "请把您的年级输入输入区后，再在操作区输入确定！！")
                elif 425 < x < 525 and 320 < y < 390:
                    # 确定
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功!")
                    self.contrast_answer()

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
            self.window.nameEdit.setText(data[0])
            self.window.messagelab.setText("提示!\n\t" + "姓名输入成功！请您下一步输入性别\n\t" +
                                           "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 2
        elif self.sign == 2:
            self.window.sexEdit.setText(data[0])
            self.window.messagelab.setText("提示!\n\t" + "性别输入成功！请您下一步输入出生年月\n\t" +
                                           "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
                except:
                    da = data[0]
                self.window.yearEdit.setText(da)
                self.window.messagelab.setText("提示!\n\t" + "出生年月输入成功！请您下一步输入学校" +
                                               "\n\t如果输入错误请您操作区输入＇上一步＇操作")
                self.sign = 4
        elif self.sign == 4:
            self.window.schoolEiit.setText(data[0])
            self.window.messagelab.setText("提示!\n\t" + "学校输入成功！请您下一步输入年级" +
                                           "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 5
        elif self.sign == 5:
            self.window.gradeEdit.setText(data[0])
            self.window.messagelab.setText("提示!\n\t" + "年级输入成功！" +
                                           "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 6
        time.sleep(1)
        self.window.timer_next.start(200)

    # 连接用户主界面
    def connect_fun(self):
        if len(self.window.nameEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "姓名框不能为空！！")
            self.sign = 1
        elif len(self.window.sexEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "性别框不能为空！！")
            self.sign = 2
        elif len(self.window.yearEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "出生年月框不能为空！！")
            self.sign = 3
        elif len(self.window.schoolEiit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "学校框不能为空！！")
            self.sign = 4
        elif len(self.window.gradeEdit.text()) == 0:
            self.window.messagelab.setText("提示!\n\t" + "年级框不能为空！！")
            self.sign = 5
        else:
            try:
                self.window.timer_next.stop()
                self.window.timer_camera.stop()
                self.window.self_cap.release()  # 释放视频流
                self.window.newlab.clear()
            except:
                pass
            self.save_data()
            UserOperation.win.splitter.widget(0).setParent(None)
            UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())

    # 保存用户的信息
    def save_data(self):
        self.image_path = "./datas/image/a7.jpeg"
        a = self.window.nameEdit.text()
        b = self.window.yearEdit.text()
        c = self.window.sexEdit.text()
        d = self.window.schoolEiit.text()
        e = self.window.gradeEdit.text()
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab)
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_date VALUES(?,?,?,?,?,?)",
                     (UserOperation.number, a, b, c, d, e))
        conn.execute("insert into User_image values(?,?,?)",
                     (UserOperation.number, total, '.jpeg',))
        conn.execute("INSERT INTO Student_date VALUES(?,?,?,?,?)",
                     (UserOperation.number, theTime, 1, 0.0, theTime))
        conn.commit()
        conn.close()
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:  # 开始时间  ， 课程号，课程名， 文件名 ， 结束时间
            c.execute('''CREATE TABLE User_data(strat_time text,
                Cno text,Coursename text, filename text,last_time text)''')
        except:
            pass
        c.close()
        conn.close()
