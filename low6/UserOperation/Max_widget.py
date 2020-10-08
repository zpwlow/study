from PyQt5.QtWidgets import QHBoxLayout,QWidget
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.Max_widget_win import Max_widget_win
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3,glob,datetime
from UserOperation.FingerDetection import figer_number
import UserOperation

class Max_widget(QWidget):
    def __init__(self,dow,data1,data2,data3):
        super(Max_widget, self).__init__()
        self.pa = './datas/tupian'
        self.a = 1
        self.dow = dow
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.fileNames = glob.glob(self.pa + r'/*')
        self.startime = datetime.datetime.now()
        self.setWindowTitle(data3)
        self.max_win = Max_widget_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.max_win)
        pa = self.fileNames[self.a - 1]
        pixmap = QPixmap(pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.max_win.lab2.setPixmap(pixmap)  # 在label上显示图片
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.max_win.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.max_win.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            if fingers[0] == 1:
                if x > 45 and x < 125 and y > 190 and y < 260:
                    # 关闭
                    self.timer_next.stop()
                    self.max_win.messagelab.setText("提示!\n" + "本次操作为：关闭\n操作成功")
                    self.closewin()
                elif x > 170 and x < 250 and y > 190 and y < 260:
                    # 上一页
                    self.timer_next.stop()
                    self.max_win.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                    self.cut_images()
                elif x > 295 and x < 375 and y > 320 and y < 390:
                    # 下一页
                    self.timer_next.stop()
                    self.max_win.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                    self.add_images()

    def closewin(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.max_win.newlab.clear()
        except:
            pass
        ab = '%Y-%m-%d %H:%M:%S'
        endtime = datetime.datetime.now()
        b = endtime- self.startime
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)",
                  (UserOperation.number,))
        data= c.fetchall()[0]
        da = data[3] + b.seconds
        conn.execute("update Student_date set stude_day =(?) where number=(?)",
                     (da, UserOperation.number))
        conn.commit()
        c.execute("select * from Coursetime where number=(?) and Cno=(?)",
                  (UserOperation.number,self.data1))
        data = c.fetchall()[0]
        da = data[2] + b.seconds
        conn.execute("update Coursetime set time =(?) where number=(?)and Cno=(?)",
                     (da, UserOperation.number,self.data1))
        conn.commit()
        conn.close()
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?)",
                       (self.startime.strftime(ab), self.data1, self.data2, self.data3, endtime.strftime(ab)))
        conn.commit()
        conn.close()
        self.close()
        self.dow.changetime()

    # 下一页ppt
    def add_images(self):
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
        except:
            self.a = self.a - 1
            self.max_win.messagelab.setText("提示!\n\t" + "这是最后一页")
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.max_win.lab2.setPixmap(pixmap)  # 在label上显示图片
        self.max_win.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.timer_next.start(900)

    # 上一页ppt
    def cut_images(self):
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.max_win.messagelab.setText("提示!\n\t" + "这是第一页")
        else:
            self.timer_next.stop()
            self.pa = self.fileNames[self.a]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.max_win.lab2.setPixmap(pixmap)  # 在label上显示图片
            self.max_win.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.timer_next.start(900)