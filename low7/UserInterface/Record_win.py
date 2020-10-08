from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout, QLineEdit
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QFont, QMovie, QPixmap
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM
from UserOperation import Record
import cv2


# 用户登录界面类
class Record_win(QFrame):
    def __init__(self):
        super(Record_win, self).__init__()
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
        self.usr = QLabel("用户:")
        self.password = QLabel("密码:")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.datalayer = Record.Record(self)
        self.image = None
        self.face = None
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(75, 270, 175, 340, "上一步")
        self.newlab.setxy(250, 270, 350, 340, "确定")
        self.newlab.setxy(425, 270, 525, 340, "退出")
        self.newlab.setxy(75, 410, 175, 480, "忘记密码")
        self.newlab.setxy(250, 410, 350, 480, "登录")
        self.newlab.setxy(425, 410, 525, 480, "注册")
        self.devise_Ui()

    def devise_Ui(self):

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.password.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.password.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit.setPlaceholderText("请在输入框输入手机号码(一次输入不能超过四位数)")
        self.usrLineEdit.setMaximumSize(420, 40)
        self.usrLineEdit.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(420, 40)
        self.pwdLineEdit.setPlaceholderText("请在输入框输入密码(一次输入不能超过四位数)")
        self.pwdLineEdit.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.messagelab, 0, 12, 4, 7)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 2, 0, 10, 10)
        self.layout.addWidget(self.usr, 5, 11, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 5, 12, 1, 8)
        self.layout.addWidget(self.password, 7, 11, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 7, 12, 1, 8)
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
        self.face = show[self.record_win.newlab.y1:self.record_win.newlab.y2,
                    self.record_win.newlab.x1:self.record_win.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框
