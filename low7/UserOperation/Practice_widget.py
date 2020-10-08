import cv2
import datetime
import glob
import os
import sqlite3
import time
from PyQt5.QtGui import QPixmap
import UserOperation
from UserOperation import ContrastJob
from UserOperation.FingerDetection import figer_number


class Practice_widget():
    def __init__(self, win):
        super(Practice_widget, self).__init__()
        self.startime = datetime.datetime.now()
        self.window = win
        self.pa = './datas/tupian'
        self.a = 0
        list3 = win.data2[2].split("@")
        self.answers = []
        for list in list3:
            da = list.split("#")
            self.answers.append(da)
        self.fileNames = glob.glob(self.pa + r'/*')
        self.pa = self.fileNames[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.window.imagelab.setPixmap(pixmap)  # 在label上显示图片
        self.window.imagelab.setScaledContents(True)  # 让图片自适应label大小

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
                    # 关闭
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：关闭\n\t操作成功")
                    self.closewin()
                elif 375 < x < 475 and 270 < y < 340:
                    # 验证答案
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：验证答案\n\t操作成功")
                    self.contrast_answer()
                elif 125 < x < 225 and 410 < y < 480:
                    # 上一题
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一题\n\t操作成功")
                    self.lastfun()
                elif 375 < x < 475 and 410 < y < 480:
                    # 下一题
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：下一题\n\t操作成功")
                    self.addfun()

    # 关闭窗口
    def closewin(self):
        self.window.timer_next.stop()
        try:
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
            self.window.newlab.clear()
        except:
            pass
        ab = '%Y-%m-%d %H:%M:%S'
        endtime = datetime.datetime.now()
        b = endtime - self.startime
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)", (UserOperation.number,))
        data = c.fetchall()[0]
        da = data[3] + b.seconds
        conn.execute("update Student_date set stude_day =(?) where number=(?)",
                     (da, UserOperation.number))
        conn.commit()
        c.execute("select * from Coursetime where number=(?) and Cno=(?)",
                  (UserOperation.number, self.window.data1))
        data = c.fetchall()[0]
        da = data[2] + b.seconds
        conn.execute("update Coursetime set time =(?) where number=(?)and Cno=(?)",
                     (da, UserOperation.number, self.window.data1))
        conn.commit()
        conn.close()
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?)",
                     (self.startime.strftime(ab), self.window.data1,
                      self.window.data2, self.window.data3, endtime.strftime(ab)))
        conn.commit()
        conn.close()
        self.window.close()
        self.window.dow.changetime()

    # 识别输入区的答案
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

    # 判断答案是否正确,正确则输出
    def contrast_answer_right(self):
        self.window.movie.stop()
        self.window.progresslab.clear()
        self.window.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.window.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.window.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
        if data[1] > 0.85:
            for answer in self.answers:
                if answer[0] == self.filename:
                    if answer[1] == da:
                        self.window.answerlab.setText("答案：" +
                                                      answer[1] + "\n解析:\n" + answer[2])
                        self.window.messagelab.setText("提示!\n\t" + "回答正确！！")
                        x = 1
                        time.sleep(3)
        else:
            self.window.messagelab.setText("提示!\n\t" + "请写入答案后再验证答案！！！")
        if x == 0:
            self.window.messagelab.setText("提示!\n\t" + "回答错误\n\t请把正确答案放置在答案区！！")
            self.window.answerlab.setText("")
        self.window.timer_next.start(200)

    # 下一题
    def addfun(self):
        self.window.timer_next.stop()
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.window.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.window.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.window.answerlab.clear()
        except:
            self.a = self.a - 1
            self.pa = self.fileNames[self.a]
            self.window.messagelab.setText("提示!\n\t" + "这是最后一题")
        self.window.timer_next.start(200)

    # 上一题
    def lastfun(self):
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.window.messagelab.setText("提示!\n\t" + "这是第一题")
        else:
            self.window.timer_next.stop()
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.window.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.window.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.window.answerlab.clear()
            self.window.timer_next.start(200)
