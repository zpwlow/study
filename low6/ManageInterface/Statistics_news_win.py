from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QToolBox,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtCore import QSize
import sqlite3,base64
import ManageOperation

#统计信息
class Statistics_news_win(QWidget):
    def __init__(self):
        super(Statistics_news_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.lab = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.lab.setMaximumSize(200, 40)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 0, 8, 19)


class StatisticsWidget(QWidget):
    def __init__(self, data):
        super(StatisticsWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.numlab = QLabel("人数:")
        self.numlab2 = QLabel(str(data[2]))
        self.image_path = "./datas/image/image" + data[4]
        total = base64.b64decode(data[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.numlab.setMaximumSize(80, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)

class Statisticswindow(QListWidget):
    def __init__(self, dow):
        super(Statisticswindow, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('./datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,name,numble,total,filename \
                  from Course,Course_image,Teacher_Course \
                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                    and number=(?)", (ManageOperation.number,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, StatisticsWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            self.dow.clicked(da)