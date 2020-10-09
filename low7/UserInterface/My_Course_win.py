from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout, QListWidget, QToolBox
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import  QColor
from PyQt5.QtCore import QSize
import base64
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM, User_report
import cv2

from UserOperation import My_Course


class My_Course_win(QFrame):
    def __init__(self):
        super(My_Course_win, self).__init__()
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.layout = QGridLayout()
        self.win = QWidget()
        self.horizontalLayout = QHBoxLayout(self)
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.qtool = QToolBox()
        self.image = None
        self.datalayer = My_Course.My_Course(self)
        self.newlab.setxy(45, 60, 125, 130, "返回")
        self.newlab.setxy(170, 60, 250, 130, "添加课程")
        self.newlab.setxy(45, 190, 125, 260, "上一页")
        self.newlab.setxy(170, 190, 250, 260, "下一页")
        self.newlab.setxy(45, 320, 125, 390, "课程一")
        self.newlab.setxy(170, 320, 250, 390, "课程二")
        self.newlab.setxy(295, 320, 375, 390, "课程二")
        self.devise_Ui()

    def devise_Ui(self):
        self.resize(self.width1 * 4, self.height1 * 4)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 * 2, 90)
        self.newlab.setMaximumSize(450, 450)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);"
                                 "font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.messagelab, 0, 12, 3, 10)
        self.layout.addWidget(self.progresslab, 2, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 2, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 6, 8)
        self.layout.addWidget(self.qtool, 3, 8, 10, 14)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
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


class CustomWidget(QWidget):
    def __init__(self, data, y):
        super(CustomWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        if y == 0:
            text = "课程一: "
        elif y == 1:
            text = "课程二: "
        elif y == 2:
            text = "课程三: "
        self.imagelab = QLabel()
        self.namelab = QLabel(text + data[2])
        self.teacherlab = QLabel("老师:")
        self.teacherlab2 = QLabel(str(data[3]))
        self.image_path = "./datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet(
            "QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.teacherlab.setMaximumSize(80, 40)
        self.teacherlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.teacherlab, 3, 8, 1, 1)
        self.layout.addWidget(self.teacherlab2, 3, 9, 1, 2)


class Coursewindow(QListWidget):
    def __init__(self, datas, sign):
        super(Coursewindow, self).__init__()
        x = 0
        y = 0
        for data in datas:
            if y == 3:
                break
            if x >= sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CustomWidget(data, y))
                y = y + 1
            x = x + 1
