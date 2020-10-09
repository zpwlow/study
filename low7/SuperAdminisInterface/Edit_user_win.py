from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QComboBox, QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont


# 编辑用户信息
from SuperAdminisOperation import Edit_user


class Edit_user_win(QFrame):
    def __init__(self,number):
        super(Edit_user_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Edit_user.Edit_user(self)
        self.number = number
        self.sure = QPushButton("确认")
        self.amend = QPushButton("修改用户密码")
        self.returnBtn = QPushButton("返回")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.grade = QLabel("选择年级")
        self.gradecb = QComboBox()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        yearnb = []
        for i in range(1980, 2020):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        grade = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级',
                 '初一', '初二', '初三',
                 '高一', '高二', '高三']
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(255,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.school.setMaximumSize(50, 40)
        self.returnBtn.setMaximumSize(60, 40)
        self.amend.setMaximumSize(190, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)
        self.grade.setMaximumSize(95, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)
        self.gradecb.setMaximumSize(420, 40)
        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.gradecb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.yearcb.addItems(yearnb)
        self.monthcb.addItems(monthmb)

        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.amend, 0, 10, 1, 1)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 4, 1, 18)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 4, 1, 18)
        self.layout.addWidget(self.year, 3, 3, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 4, 1, 8)
        self.layout.addWidget(self.monthcb, 3, 10, 1, 7)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 4, 1, 18)
        self.layout.addWidget(self.grade, 5, 3, 1, 1)
        self.layout.addWidget(self.gradecb, 5, 4, 1, 18)
        self.layout.addWidget(self.sure, 6, 4, 1, 18)