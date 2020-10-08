import sqlite3

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QFrame

import ManageOperation
# 管理员我的界面
from ManageOperation import Controller_myself


class Controller_myself_win(QFrame):  # 增加一个编辑资料的按钮
    def __init__(self):
        super(Controller_myself_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Controller_myself.Controller_myself(self)
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.returnBtn = QPushButton("返回")
        self.ExditBtn = QPushButton("编辑")
        self.chang_image = QPushButton("换头像")
        self.name = QLabel("姓名:")
        self.sex = QLabel("性别:")
        self.number = QLabel("手机号:")
        self.year = QLabel("出生年月:")
        self.school = QLabel("学校:")
        self.amend = QPushButton("修改密码")
        self.withdraw = QPushButton('退出')
        self.tupian = QLabel()
        self.withdraw.clicked.connect(self.datawindow.return_win)
        self.returnBtn.clicked.connect(self.datawindow.return_fun)
        self.ExditBtn.clicked.connect(self.datawindow.edit_fun)
        self.chang_image.clicked.connect(self.datawindow.chang_fun)
        self.amend.clicked.connect(self.datawindow.amend_fun)
        self.devise_ui()

    def devise_ui(self):

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(100, 0, 0, 0)

        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)",
                  (ManageOperation.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.name1 = QLabel(self.data[1])  # 读取数据库中的信息，将信息输出label中
        self.sex1 = QLabel(self.data[3])
        self.number1 = QLabel(self.data[0])
        self.year1 = QLabel(self.data[2][0:4] + "年 " + self.data[2][5:] + ' 月')
        self.school1 = QLabel(self.data[4])
        self.returnBtn.setMaximumSize(60, 40)
        self.ExditBtn.setMaximumSize(60, 40)
        self.name.setMaximumSize(70, 40)
        self.sex.setMaximumSize(70, 40)
        self.number.setMaximumSize(70, 40)
        self.school.setMaximumSize(70, 40)
        self.year.setMaximumSize(100, 40)
        self.name1.setMaximumSize(350, 40)
        self.sex1.setMaximumSize(350, 40)
        self.number1.setMaximumSize(350, 40)
        self.school1.setMaximumSize(350, 40)
        self.year1.setMaximumSize(350, 40)
        self.amend.setMaximumSize(500, 40)
        self.withdraw.setMaximumSize(500, 40)
        self.chang_image.setMaximumSize(90, 40)
        self.tupian.setMaximumSize(250, 250)
        self.chang_image.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.withdraw.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.ExditBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.name1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.layout.addWidget(self.tupian, 1, 1, 4, 4)
        self.layout.addWidget(self.chang_image, 5, 2, 1, 2)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.ExditBtn, 0, 10, 1, 1)
        self.layout.addWidget(self.name, 1, 6, 1, 1)
        self.layout.addWidget(self.name1, 1, 8, 1, 6)
        self.layout.addWidget(self.year, 2, 6, 1, 1)
        self.layout.addWidget(self.year1, 2, 8, 1, 6)
        self.layout.addWidget(self.sex, 3, 6, 1, 1)
        self.layout.addWidget(self.sex1, 3, 8, 1, 6)
        self.layout.addWidget(self.number, 4, 6, 1, 1)
        self.layout.addWidget(self.number1, 4, 8, 1, 6)
        self.layout.addWidget(self.school, 5, 6, 1, 1)
        self.layout.addWidget(self.school1, 5, 8, 1, 6)
        self.layout.addWidget(self.amend, 7, 6, 1, 6)
        self.layout.addWidget(self.withdraw, 8, 6, 1, 6)
