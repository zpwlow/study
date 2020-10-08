from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout
from PyQt5.QtWidgets import QApplication,QHBoxLayout
from UserInterface.MyLabel import MyLabel


# 用户我的界面
class User_Myself_win(QWidget):
    def __init__(self,data):
        super(User_Myself_win, self).__init__()
        self.name = QLabel("姓名:")
        self.sex = QLabel("性别:")
        self.number = QLabel("手机号:")
        self.year = QLabel("出生年月:")
        self.school = QLabel("学校:")
        self.grade = QLabel("年级:")
        self.data = data
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setxy(125, 300, 225, 370, "返回")
        self.newlab.setxy(375, 300, 475, 370, "修改密码")
        self.devise_ui()

    def devise_ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)

        self.name1 = QLabel(self.data[1])  # 读取数据库中的信息，将信息输出label中
        self.sex1 = QLabel(self.data[3])
        self.number1 = QLabel(self.data[0])
        self.year1 = QLabel(self.data[2][0:4] + "年 " + self.data[2][5:] + ' 月')
        self.school1 = QLabel(self.data[4])
        self.grade1 = QLabel(self.data[5])
        self.name.setMaximumSize(70, 40)
        self.sex.setMaximumSize(70, 40)
        self.number.setMaximumSize(70, 40)
        self.school.setMaximumSize(70, 40)
        self.year.setMaximumSize(100, 40)
        self.grade.setMaximumSize(70, 40)
        self.name1.setMaximumSize(350, 40)
        self.sex1.setMaximumSize(350, 40)
        self.number1.setMaximumSize(350, 40)
        self.school1.setMaximumSize(350, 40)
        self.grade1.setMaximumSize(350, 40)
        self.year1.setMaximumSize(350, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.name1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.layout.addWidget(self.messagelab, 0, 9, 3, 8)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 8)
        self.layout.addWidget(self.name, 3, 9, 1, 2)
        self.layout.addWidget(self.name1, 3, 10, 1, 6)
        self.layout.addWidget(self.year, 4, 9, 1, 2)
        self.layout.addWidget(self.year1, 4, 11, 1, 6)
        self.layout.addWidget(self.sex, 5, 9, 1, 2)
        self.layout.addWidget(self.sex1, 5, 11, 1, 6)
        self.layout.addWidget(self.number, 6, 9, 1, 2)
        self.layout.addWidget(self.number1, 6, 11, 1, 6)
        self.layout.addWidget(self.school, 7, 9, 1, 2)
        self.layout.addWidget(self.school1, 7, 11, 1, 6)
        self.layout.addWidget(self.grade, 8, 9, 1, 2)
        self.layout.addWidget(self.grade1, 8, 11, 1, 6)