from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QTableWidget, QFrame
from PyQt5.QtWidgets import QHBoxLayout

from ManageOperation import User_report


class User_report_win(QFrame):
    def __init__(self,data1,data2):
        super(User_report_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = User_report.User_report(self)
        self.da1 = data1
        self.da2 = data2
        self.returnBtn = QPushButton("返回")
        self.day = QLabel("学习天数:")
        self.learntime = QLabel("学习总时长:")
        self.avglearn = QLabel("日均学习:")
        self.table = QTableWidget()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        #        self.layout.setContentsMargins (300, 0, 0, 0)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                         QPushButton{background-color:rgb(170,200, 50)}\
                                         QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.day.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learntime.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.returnBtn.setMaximumSize(60, 40)
        self.day.setMaximumSize(120, 40)
        self.learntime.setMaximumSize(130, 40)
        self.avglearn.setMaximumSize(120, 40)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.day, 0, 3, 1, 1)
        self.layout.addWidget(self.learntime, 0, 6, 1, 1)
        self.layout.addWidget(self.avglearn, 0, 9, 1, 1)