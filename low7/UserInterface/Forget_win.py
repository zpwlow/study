from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout, QLineEdit
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QFont
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM
from UserOperation import Forget
import cv2


# 用户忘记密码界面
class Forget_win(QFrame):
    def __init__(self):
        super(Forget_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.usr2 = QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频

        self.image = None
        self.face = None
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(125, 270, 225, 340, "返回")
        self.newlab.setxy(375, 270, 475, 340, "上一步")
        self.newlab.setxy(125, 410, 225, 480, "确定")
        self.newlab.setxy(375, 410, 475, 480, "修改密码")
        self.datalayer = Forget.Forget(self)
        self.devise_Ui()

    def devise_Ui(self):

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.usrLineEdit2.setPlaceholderText("请在输入区输入手机号码(一次输入不能超过四位数)")
        self.pwdLineEdit2.setPlaceholderText("请在输入区输入新的密码(一次输入不能超过四位数)")
        self.usrLineEdit2.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.messagelab, 0, 13, 3, 8)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 10, 12)
        self.layout.addWidget(self.usr2, 6, 13, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 6, 14, 1, 8)
        self.layout.addWidget(self.pwd2, 9, 13, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 9, 14, 1, 8)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image, self.face))
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
        self.face = show[self.newlab.y1:self.newlab.y2,
                    self.newlab.x1:self.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.newlab.setPixmap(QPixmap.fromImage(showImage))
