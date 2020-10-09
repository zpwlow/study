from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont

# 注册
from SuperAdminisOperation import Logon


class Logon_win(QFrame):
    def __init__(self):
        super(Logon_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Logon.Logon(self)
        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.password2 = QLabel("确认密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        self.password2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.codeLineEdit.setMaximumSize(310, 40)
        # self.usrLineEdit2.setText(a)
        self.usrLine.setPlaceholderText("请输入手机号码")
        self.usrnameLine.setPlaceholderText("请输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请输入密码")
        self.pwdLineEdit2.setPlaceholderText("请重新输入密码")
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.codeLineEdit.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLine, 1, 5, 1, 14)
        self.layout.addWidget(self.usrname, 2, 3, 1, 1)
        self.layout.addWidget(self.usrnameLine, 2, 5, 1, 14)
        self.layout.addWidget(self.password1, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 3, 5, 1, 14)
        self.layout.addWidget(self.password2, 4, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 4, 5, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 5, 5, 1, 5)
        self.layout.addWidget(self.codebel, 5, 10, 1, 6)
        self.layout.addWidget(self.change_code, 5, 12, 1, 1)
        self.layout.addWidget(self.okBtn, 6, 5, 1, 14)
