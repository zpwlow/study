from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout, QLineEdit
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QFont
import UserOperation
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM, User_amend
import cv2


# 用户修改密码
class User_amend_win(QFrame):
    def __init__(self):
        super(User_amend_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.usrlab1 = QLabel(str(UserOperation.number))
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.usrlab = QLabel("账号:")
        self.amendlab1 = QLabel("原密码:")
        self.amendlab2 = QLabel("新密码:")
        self.amendedit1 = QLineEdit()
        self.amendedit2 = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．

        self.image = None
        self.face = None
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(75, 270, 175, 340, "返回")
        self.newlab.setxy(250, 270, 350, 340, "确定")
        self.newlab.setxy(425, 270, 525, 340, "修改")
        self.newlab.setxy(75, 410, 175, 480, "上一步")
        self.newlab.setxy(250, 410, 350, 480, "下一步")
        self.datalayer = User_amend.User_amend(self)
        self.devise_Ui()

    def devise_Ui(self):

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.usrlab.setMaximumSize(80, 40)
        self.amendlab1.setMaximumSize(80, 40)
        self.amendlab2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usrlab.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setMaximumSize(420, 40)
        self.amendedit1.setMaximumSize(420, 40)
        self.amendedit2.setMaximumSize(420, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 * 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.amendedit1.setPlaceholderText("请在输入区输入原密码")
        self.amendedit2.setPlaceholderText("请在输入区输入新密码")
        self.amendedit1.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.amendedit2.setFont(QFont("宋体", 16))
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")

        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.layout.addWidget(self.messagelab, 0, 10, 3, 7)
        self.layout.addWidget(self.progresslab, 2, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 2, 3, 1, 6)
        self.layout.addWidget(self.newlab, 5, 0, 6, 9)
        self.layout.addWidget(self.usrlab, 5, 9, 1, 1)
        self.layout.addWidget(self.usrlab1, 5, 10, 1, 7)
        self.layout.addWidget(self.amendlab1, 7, 9, 1, 1)
        self.layout.addWidget(self.amendedit1, 7, 10, 1, 7)
        self.layout.addWidget(self.amendlab2, 9, 9, 1, 1)
        self.layout.addWidget(self.amendedit2, 9, 10, 1, 7)
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
