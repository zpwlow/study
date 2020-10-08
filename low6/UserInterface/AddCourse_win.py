from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout,QListWidget,QToolBox
from PyQt5.QtWidgets import QApplication,QHBoxLayout,QListWidgetItem
from PyQt5.QtGui import QPixmap,QMovie,QColor,QIcon
from PyQt5.QtCore import QSize
import base64
from UserInterface.MyLabel import MyLabel

class AddCourse_win(QWidget):
    def __init__(self):
        super(AddCourse_win, self).__init__()
        self.setWindowTitle("添加课程")
        self.setWindowIcon(QIcon("./datas/logo.ico"))
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(220, 150, 380, 230, "输入区")
        self.newlab.setxy(75, 300, 175, 370, "关闭")
        self.newlab.setxy(250, 300, 350, 370, "搜索")
        self.newlab.setxy(425, 300, 525, 370, "加入")
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1 , self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1/2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.qtool.setMaximumSize(self.width1/2, self.height1-100)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.messagelab, 0, 11, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.qtool, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("./datas/progress_bar.gif")
        self.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小


class CourseQlist(QListWidget):
    def __init__(self,  datas):
        super(CourseQlist, self).__init__()
        item = QListWidgetItem(self)
        item.setSizeHint(QSize(800, 200))
        item.setBackground(QColor(240, 240, 240))
        self.setItemWidget(item, CourseWidget(datas))


class CourseWidget(QWidget):
    def __init__(self, data):
        super(CourseWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.data = data
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.numlab = QLabel("课程号:")
        self.numlab2 = QLabel(data[0])
        self.namelab = QLabel("课程名:")
        self.namelab2 = QLabel(data[1])
        self.teacherlab = QLabel("教师:")
        self.teacherlab2 = QLabel(data[2])
        self.image_path = "./datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.namelab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(200, 200)
        self.namelab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80,40)
        self.teacherlab.setMaximumSize(80,40)
        self.namelab2.setMaximumSize(200, 40)
        self.numlab2.setMaximumSize(200, 40)
        self.teacherlab2.setMaximumSize(200, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 5, 3)
        self.layout.addWidget(self.numlab, 0, 3, 1, 1)
        self.layout.addWidget(self.namelab, 1, 3, 1, 1)
        self.layout.addWidget(self.teacherlab,2,3,1,1)
        self.layout.addWidget(self.numlab2, 0, 4, 1, 3)
        self.layout.addWidget(self.namelab2, 1, 4, 1, 3)
        self.layout.addWidget(self.teacherlab2, 2, 4, 1, 3)

