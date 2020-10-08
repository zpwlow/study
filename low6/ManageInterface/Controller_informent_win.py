from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout,QLineEdit
from PyQt5.QtWidgets import QHBoxLayout,QComboBox
from PyQt5.QtGui import QFont

# 管理员信息填写
class Controller_informent_win(QWidget):
    def __init__(self):
        super(Controller_informent_win, self).__init__()
        self.sure = QPushButton("确认")
        self.chang_image = QPushButton("换头像")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.nameEdit = QLineEdit()
        self.tupian = QLabel()
        self.schoolEiit = QLineEdit()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(100, 0, 0, 0)
        yearnb = []
        for i in range(1960, 2005):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.chang_image.setStyleSheet(
            "QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setPlaceholderText("请输入姓名")
        self.schoolEiit.setPlaceholderText("请输入学校名称")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.chang_image.setMaximumSize(90, 40)
        self.school.setMaximumSize(50, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)
        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.tupian.setMaximumSize(250, 250)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.yearcb.addItems(yearnb)
        self.monthcb.addItems(monthmb)
        self.layout.addWidget(self.tupian, 1, 1, 4, 4)
        self.layout.addWidget(self.chang_image, 4, 2, 1, 2)
        self.layout.addWidget(self.name, 1, 6, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 8, 1, 8)
        self.layout.addWidget(self.sex, 2, 6, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 8, 1, 8)
        self.layout.addWidget(self.year, 3, 6, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 8, 1, 4)
        self.layout.addWidget(self.monthcb, 3, 11, 1, 7)
        self.layout.addWidget(self.school, 4, 6, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 8, 1, 8)
        self.layout.addWidget(self.sure, 6, 8, 1, 8)