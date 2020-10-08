from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout
from PyQt5.QtWidgets import QApplication,QHBoxLayout
from PyQt5.QtCore import Qt
from UserInterface.MyLabel import MyLabel

class Max_widget_win(QWidget):
    def __init__(self):
        super(Max_widget_win, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint
                            | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool |Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()/4
        self.width1 = self.screenRect.width()/4
        self.resize(self.width1*4, self.height1*4)
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
        self.lab2.resize(self.width1*4, self.height1*4)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(450, 450)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 1, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 2, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 6)
        self.layout.addWidget(self.lab2, 4, 7, 10, 15)