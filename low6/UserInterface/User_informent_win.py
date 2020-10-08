from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout,QLineEdit
from PyQt5.QtWidgets import QApplication,QHBoxLayout
from PyQt5.QtGui import QFont,QMovie,QPixmap
from UserInterface.MyLabel import MyLabel


class User_informent_win(QWidget):
    def __init__(self):
        super(User_informent_win, self).__init__()
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearEdit = QLineEdit()
        self.sex = QLabel("性别:")
        self.sexEdit = QLineEdit()
        self.school = QLabel("学校:")
        self.grade = QLabel("年级")
        self.gradeEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel("输入区")  # 放置视频
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(75, 320, 175, 390, "上一步")
        self.newlab.setxy(250, 320, 350, 390, "确定")
        self.newlab.setxy(425, 320, 525, 390, "完成")
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
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.nameEdit.setPlaceholderText("请在输入区输入姓名")
        self.yearEdit.setPlaceholderText("请在输入区输入年月如:201912")
        self.sexEdit.setPlaceholderText("请在输入区输入性别")
        self.schoolEiit.setPlaceholderText("请在输入区输入学校名称")
        self.gradeEdit.setPlaceholderText("请在输入区输入年级")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.sexEdit.setFont(QFont("宋体", 14))
        self.yearEdit.setFont(QFont("宋体", 14))
        self.gradeEdit.setFont(QFont("宋体", 14))
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.name.setMaximumSize(100, 40)
        self.school.setMaximumSize(100, 40)
        self.year.setMaximumSize(100, 40)
        self.sex.setMaximumSize(100, 40)
        self.grade.setMaximumSize(100, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sexEdit.setMaximumSize(420, 40)
        self.gradeEdit.setMaximumSize(420, 40)
        self.yearEdit.setMaximumSize(420, 40)
        self.layout.addWidget(self.messagelab, 0, 12, 3, 10)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 11, 12)
        self.layout.addWidget(self.name, 4, 13, 1, 2)
        self.layout.addWidget(self.nameEdit, 4, 15, 1, 8)
        self.layout.addWidget(self.sex, 6, 13, 1, 2)
        self.layout.addWidget(self.sexEdit, 6, 15, 1, 8)
        self.layout.addWidget(self.year, 8, 13, 1, 2)
        self.layout.addWidget(self.yearEdit, 8, 15, 1, 8)
        self.layout.addWidget(self.school, 10, 13, 1, 2)
        self.layout.addWidget(self.schoolEiit, 10, 15, 1, 8)
        self.layout.addWidget(self.grade, 12, 13, 1, 2)
        self.layout.addWidget(self.gradeEdit, 12, 15, 1, 8)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("./datas/progress_bar.gif")
        self.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小