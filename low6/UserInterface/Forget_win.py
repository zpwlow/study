from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout,QLineEdit
from PyQt5.QtWidgets import QApplication,QHBoxLayout
from PyQt5.QtGui import QFont,QMovie,QPixmap
from UserInterface.MyLabel import MyLabel

# 用户忘记密码界面
class Forget_win(QWidget):
    def __init__(self):
        super(Forget_win, self).__init__()
        self.usr2 = QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(125, 270, 225, 340, "返回")
        self.newlab.setxy(375, 270, 475, 340, "上一步")
        self.newlab.setxy(125, 410, 225, 480, "确定")
        self.newlab.setxy(375, 410, 475, 480, "修改密码")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
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
        self.movie = QMovie("./datas/progress_bar.gif")
        self.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小