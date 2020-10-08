from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont


# 用户登录界面
from ManageOperation import Record


class Record_win(QFrame):
    def __init__(self):
        super(Record_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Record.Record(self)
        self.usr = QLabel("用户:")
        self.password = QLabel("密码:")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("登录")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.forgetbtn = QLabel()
        self.logonbtn = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.password.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.password.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrLineEdit.setPlaceholderText("请输入手机号码")
        self.usrLineEdit.setMaximumSize(420, 40)
        self.usrLineEdit.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(420, 40)
        self.pwdLineEdit.setPlaceholderText("请输入密码")
        self.pwdLineEdit.setFont(QFont("宋体", 16))
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.codeLineEdit.setFont(QFont("宋体", 16))
        self.codeLineEdit.setMaximumSize(310, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.codebel.setMaximumSize(100, 40)
        self.forgetbtn.setText("<A href='www.baidu.com'>忘记密码</a>")
        self.logonbtn.setText("<A href='www.baidu.com'>注册</a>")
        self.forgetbtn.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.logonbtn.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.forgetbtn.setMaximumSize(90, 50)
        self.logonbtn.setMaximumSize(50, 50)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 1, 4, 1, 14)
        self.layout.addWidget(self.password, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 2, 4, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 3, 4, 1, 5)
        self.layout.addWidget(self.codebel, 3, 9, 1, 6)
        self.layout.addWidget(self.change_code, 3, 11, 1, 1)
        self.layout.addWidget(self.okBtn, 4, 4, 1, 14)
        self.layout.addWidget(self.forgetbtn, 5, 4, 1, 2)
        self.layout.addWidget(self.logonbtn, 5, 10, 1, 2)
