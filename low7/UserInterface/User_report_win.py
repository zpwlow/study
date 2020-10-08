from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QAbstractItemView
import UserOperation
import sqlite3, datetime
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM, User_report
import cv2


# 用户学习报告的界面
class User_report_win(QFrame):
    def __init__(self):
        super(User_report_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout(self)
        self.win = QWidget()
        self.day = QLabel("学习天数:")
        self.learntime = QLabel("学习总时长:")
        self.avglearn = QLabel("日均学习:")
        self.table = QTableWidget()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.datalayer = User_report.User_report(self)
        self.image = None
        self.newlab.setxy(150, 200, 250, 270, "返回")
        self.devise_Ui()
        self.information()

    def devise_Ui(self):

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.day.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learntime.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1, 90)
        self.newlab.setMaximumSize(450, 450)
        self.day.setMaximumSize(120, 40)
        self.learntime.setMaximumSize(130, 40)
        self.avglearn.setMaximumSize(120, 40)
        self.layout.addWidget(self.day, 1, 7, 1, 1)
        self.layout.addWidget(self.learntime, 1, 10, 1, 1)
        self.layout.addWidget(self.avglearn, 1, 13, 1, 1)
        self.layout.addWidget(self.messagelab, 1, 0, 2, 5)
        self.layout.addWidget(self.progresslab, 3, 0, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 1, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 5)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image))
        if not self.timer_camera.isActive():  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if not flag:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(200)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  # 翻转镜像--->对角翻转.
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.newlab.setPixmap(QPixmap.fromImage(showImage))

    def information(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)", (UserOperation.number,))
        self.data1 = c.fetchall()[0]
        c.close()
        conn.close()
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(self.data1[1], abcd)
        a = (new - a1).days + 1
        self.join = QLabel("已加入" + str(a) + "天")
        self.day1 = QLabel(str(self.data1[2]) + "天")
        ab = self.data1[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.learntime1 = QLabel(ac)
        ad = ab / self.data1[2]
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.avglearn1 = QLabel(ae)
        self.join.setStyleSheet("QLabel{color:rgb(0,200,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.day1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.learntime1.setStyleSheet(
            "QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.table.setStyleSheet("QTableWidget{background-color:rgb(255,255,255);font:13pt '宋体';font-weight:Bold;};");
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_data")
        data = c.fetchall()
        if len(data) > 15:
            data = data[-15:]
            self.table.setRowCount(15)
        else:
            b = len(data)
            self.table.setRowCount(b)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['开始学习时间', '文件类型', '文件名', '结束时间', '学习时长'])
        i = 0
        for variate in data:
            self.table.setItem(i, 0, QTableWidgetItem(variate[0]))
            self.table.setItem(i, 1, QTableWidgetItem(variate[2]))
            self.table.setItem(i, 2, QTableWidgetItem(variate[3]))
            self.table.setItem(i, 3, QTableWidgetItem(variate[4]))
            min = (datetime.datetime.strptime(variate[4], abcd) - datetime.datetime.strptime(variate[0], abcd)).seconds
            if (min / 3600) > 1:
                ac = str(int(min / 3600)) + '时' + str(round((min / 3600 - int(min / 3600)) * 60, 2)) + "分"
            else:
                ac = str(round(min / 60, 2)) + "分"
            self.table.setItem(i, 4, QTableWidgetItem(ac))
            i += 1
        self.join.setMaximumSize(300, 40)
        self.day1.setMaximumSize(150, 40)
        self.learntime1.setMaximumSize(150, 40)
        self.avglearn1.setMaximumSize(150, 40)
        self.layout.addWidget(self.day1, 1, 8, 1, 1)
        self.layout.addWidget(self.join, 1, 5, 1, 1)
        self.layout.addWidget(self.learntime1, 1, 11, 1, 1)
        self.layout.addWidget(self.avglearn1, 1, 14, 1, 1)
        self.layout.addWidget(self.table, 3, 5, 7, 15)
