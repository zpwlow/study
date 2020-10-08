from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel,QLineEdit
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont
import ManageOperation


# 管理员修改密码
class Controller_amend_win(QWidget):
    def __init__(self):
        super(Controller_amend_win, self).__init__()
        self.usrlab = QLabel("账号:")

        self.amendlab1 = QLabel("原密码:")
        self.amendlab2 = QLabel("新密码:")
        self.amendlab3 = QLabel("确认密码:")
        self.amendedit1 = QLineEdit()
        self.amendedit2 = QLineEdit()
        self.amendedit3 = QLineEdit()
        self.sure = QPushButton("确认修改")
        self.returnBtn = QPushButton("返回")
        self.devise_ui()

    def devise_ui(self):
        self.usrlab1 = QLabel(ManageOperation.number)
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(350, 0, 0, 0)
        self.usrlab.setMaximumSize(80, 40)
        self.amendlab1.setMaximumSize(80, 40)
        self.amendlab2.setMaximumSize(80, 40)
        self.amendlab3.setMaximumSize(100, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usrlab.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab3.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setMaximumSize(420, 40)
        self.amendedit1.setMaximumSize(420, 40)
        self.amendedit2.setMaximumSize(420, 40)
        self.amendedit3.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.amendedit1.setPlaceholderText("请输入原密码")
        self.amendedit2.setPlaceholderText("请输入新密码")
        self.amendedit3.setPlaceholderText("请重新输入密码")
        self.amendedit1.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.amendedit2.setFont(QFont("宋体", 16))
        self.amendedit3.setFont(QFont("宋体", 16))
        self.amendedit1.setEchoMode(QLineEdit.Password)
        self.amendedit2.setEchoMode(QLineEdit.Password)
        self.amendedit3.setEchoMode(QLineEdit.Password)
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.usrlab, 1, 3, 1, 1)
        self.layout.addWidget(self.usrlab1, 1, 5, 1, 5)
        self.layout.addWidget(self.amendlab1, 2, 3, 1, 1)
        self.layout.addWidget(self.amendedit1, 2, 5, 1, 5)
        self.layout.addWidget(self.amendlab2, 3, 3, 1, 1)
        self.layout.addWidget(self.amendedit2, 3, 5, 1, 5)
        self.layout.addWidget(self.amendlab3, 4, 3, 1, 1)
        self.layout.addWidget(self.amendedit3, 4, 5, 1, 5)
        self.layout.addWidget(self.sure, 5, 5, 1, 5)