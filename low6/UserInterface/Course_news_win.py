from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout,QListWidget,QToolBox
from PyQt5.QtWidgets import QApplication,QHBoxLayout,QListWidgetItem
from PyQt5.QtGui import QPixmap,QMovie,QColor
from PyQt5.QtCore import QSize
import base64
from UserInterface.MyLabel import MyLabel



class Course_news_win(QWidget):
    def __init__(self):
        super(Course_news_win, self).__init__()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setxy(45, 60, 125, 130, "返回")
        self.newlab.setxy(170, 60, 250, 130, "练习")
        self.newlab.setxy(45, 190, 125, 260, "上一页")
        self.newlab.setxy(170, 190, 250, 260, "下一页")
        self.newlab.setxy(45, 320, 125, 390, "课件一")
        self.newlab.setxy(170, 320, 250, 390, "课件二")
        self.newlab.setxy(295, 320, 375, 390, "课件三")
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.resize(self.width1*4, self.height1*4)
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
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(450, 450)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);"
                                 "font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.messagelab, 0, 12, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 6, 8)
        self.layout.addWidget(self.qtool, 4, 8, 10, 14)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("./datas/progress_bar.gif")
        self.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小


#课件的item 设计
class CuFileWidget(QWidget):
    def __init__(self, data,y):
        super(CuFileWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        if y==0:
            text = "课件一: "
        elif y==1:
            text = "课件二: "
        elif y==2:
            text = "课件三: "
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(text +data[1])
        self.image_path = "./datas/image/image" + data[3]
        total = base64.b64decode(data[2])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(800, 80)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)

#课件的QList
class CuFileQlist(QListWidget):
    def __init__(self,datas,sign):
        super(CuFileQlist, self).__init__()
        self.datas = datas
        x = 0
        y = 0
        for data in self.datas:
            if y==3:
                break
            if x>=sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CuFileWidget(data,y))
                y=y+1
            x=x+1



#练习的item 设计
class CourseexWidget(QWidget):
    def __init__(self, data,y):
        super(CourseexWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        if y==0:
            text = "练习一: "
        elif y==1:
            text = "练习二: "
        elif y==2:
            text = "练习三: "
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.namelab = QLabel(text + data[1])
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.namelab.setMaximumSize(800, 100)
        self.layout.addWidget(self.namelab, 1, 1, 1, 1)

#练习的QList
class CourseexQlist(QListWidget):
    def __init__(self,datas,sign):
        super(CourseexQlist, self).__init__()
        self.datas = datas
        x = 0
        y = 0
        for data in self.datas:
            if y == 3:
                break
            if x >= sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CourseexWidget(data,y))
                y = y + 1
            x = x + 1