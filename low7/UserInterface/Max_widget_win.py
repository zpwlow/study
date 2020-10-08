import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from UserInterface.MyLabel import MyLabel
from UserOperation import self_cap, self_CAM_NUM


class Max_widget_win(QWidget):
    def __init__(self, dow, data1, data2, data3):
        super(Max_widget_win, self).__init__()
        self.dow = dow
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.setWindowTitle(data3)
        self.setWindowFlags(Qt.WindowCloseButtonHint
                            | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.resize(self.width1 * 4, self.height1 * 4)
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setxy(45, 190, 125, 260, "关闭")
        self.newlab.setxy(170, 190, 250, 260, "上一页")
        self.newlab.setxy(295, 190, 375, 260, "下一页")
        self.lab2 = QLabel()
        self.lab2.resize(self.width1 * 4, self.height1 * 4)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 * 2, 90)
        self.newlab.setMaximumSize(450, 450)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 1, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 2, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 6)
        self.layout.addWidget(self.lab2, 4, 7, 10, 15)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
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
