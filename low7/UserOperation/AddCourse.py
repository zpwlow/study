import cv2
import datetime
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import UserOperation
from UserInterface.AddCourse_win import CourseQlist
from UserOperation.ContrastJob import ContrastJob
from UserOperation.FingerDetection import figer_number


class My_Course:
    def __init__(self, win):
        super(My_Course, self).__init__()
        self.window = win
        self.sign = 0

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 75 < x < 175 and 300 < y < 370:
                    # 关闭
                    self.window.messagelab.setText("提示!\n\t"
                                                   + "本次操作为：关闭\n\t操作成功")
                    self.clear_cap()
                    self.window.close()
                elif 250 < x < 350 and 300 < y < 370:
                    # 搜索
                    self.window.messagelab.setText("提示!\n\t"
                                                   + "本次操作为：搜索\n\t操作成功")
                    self.contrast_answer()
                elif 425 < x < 525 and 300 < y < 370:
                    # 加入
                    self.window.messagelab.setText("提示!\n\t"
                                                   + "本次操作为：加入\n\t操作成功")
                    self.joinfun()

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()

    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    # 检测窗口关闭发射信号
    def closeEvent(self, event):
        self.sendEditContent()

    # 识别输入区的手写数字
    def contrast_answer(self):
        self.window.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.window.setextlab.setText("正在识别输入中．．")
        self.window.progresslab.setMovie(self.window.movie)
        self.window.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.chang_fun)
        self.contrastjob.start()

    # 将识别的输入信息写在界面
    def chang_fun(self):
        self.window.movie.stop()
        self.window.progresslab.clear()
        self.window.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.window.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.window.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        if data[1] > 0.6:
            x = 1
            try:
                da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
            except:
                da = data[0]

            self.window.messagelab.setText("提示!\n\t" + "本次搜索内容为：" + da)
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Course.Cno,Course.name,Controller_data.name,numble,total,filename \
                                                  from Course,Controller_data,Course_image,Teacher_Course \
                                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                                   and Teacher_Course.number=Controller_data.number and \
                                                    Course.Cno=(?)", (da,))
            self.datas = c.fetchall()
            if len(self.datas) > 0:
                self.data = self.datas[0]
                self.coursewin = CourseQlist(self.data)
                self.window.qtool.removeItem(0)
                self.window.qtool.addItem(self.coursewin, '查找的课程')
                self.window.qtool.setStyleSheet(
                    "QToolBox{background:rgb(240,240,240);font-weight:Bold;color:rgb(0,0,0);}")
            else:
                try:
                    self.window.qtool.removeItem(0)
                except:
                    pass
                self.window.messagelab.setText("提示!\n\t"
                                               + "没有找到课程号为:'" + da + "'的信息!!!")
        if x == 0:
            self.window.messagelab.setText("提示!\n\t" + "没有找到课程" + "的任何信息!!!")
            try:
                self.window.qtool.removeItem(0)
            except:
                pass
        self.window.timer_next.start(200)

    # 加入课程
    def joinfun(self):
        if len(self.data) > 0:
            ab = '%Y-%m-%d %H:%M:%S'
            theTime = datetime.datetime.now().strftime(ab)
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where number=(?) and Cno=(?)",
                      (UserOperation.number, self.data[0],))
            n = len(c.fetchall())
            if n > 0:
                c.close()
                conn.close()
                self.window.messagelab.setText("提示!\n\t" +
                                               "您已经加入此课程了!\n\t不用重复加入!!")
            else:
                c.execute("insert into Join_Course values(?,?,?)",
                          (UserOperation.number, self.data[0], theTime,))
                c.execute("insert into Coursetime values(?,?,?)",
                          (UserOperation.number, self.data[0], 0.0,))
                c.execute("update Course set numble=(?) where Cno=(?)",
                          (self.data[3] + 1, self.data[0],))
                conn.commit()
                c.close()
                conn.close()
                self.window.messagelab.setText("提示!\n\t" + "加入成功!!!")
        else:
            self.window.messagelab.setText("提示!\n\t" + "您没有搜索出任何课程，请重新搜索!!!")
