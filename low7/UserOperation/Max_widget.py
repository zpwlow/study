
from PyQt5.QtGui import  QPixmap

import cv2, sqlite3, glob, datetime
from UserOperation.FingerDetection import figer_number
import UserOperation


class Max_widget:
    def __init__(self,win):
        super(Max_widget, self).__init__()
        self.pa = './datas/tupian'
        self.a = 1
        self.window = win
        self.fileNames = glob.glob(self.pa + r'/*')
        self.startime = datetime.datetime.now()
        pa = self.fileNames[self.a - 1]
        pixmap = QPixmap(pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.window.lab2.setPixmap(pixmap)  # 在label上显示图片

    # 识别手指指的操作命令
    def finger_camera(self, image):
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            if fingers[0] == 1:
                if 45 < x < 125 and 190 < y < 260:
                    # 关闭
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n" + "本次操作为：关闭\n操作成功")
                    self.closewin()
                elif 170 < x < 250 and 190 < y < 260:
                    # 上一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                    self.cut_images()
                elif 295 < x < 375 and 320 < y < 390:
                    # 下一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                    self.add_images()

    def closewin(self):
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
        c.execute("select * from Student_date where number=(?)",
                  (UserOperation.number,))
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

    # 下一页ppt
    def add_images(self):
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
        except:
            self.a = self.a - 1
            self.window.messagelab.setText("提示!\n\t" + "这是最后一页")
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.window.lab2.setPixmap(pixmap)  # 在label上显示图片
        self.window.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.window.timer_next.start(200)

    # 上一页ppt
    def cut_images(self):
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.window.messagelab.setText("提示!\n\t" + "这是第一页")
        else:
            self.window.timer_next.stop()
            self.pa = self.fileNames[self.a]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.window.lab2.setPixmap(pixmap)  # 在label上显示图片
            self.window.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.window.timer_next.start(200)
