from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel,QLineEdit
from PyQt5.QtWidgets import QHBoxLayout,QToolBox,QComboBox,QListWidgetItem,QListWidget
from PyQt5.QtGui import QPixmap,QColor,QFont
from PyQt5.QtCore import QSize
import sqlite3,base64,datetime



class Statistics_class_win(QWidget):
    def __init__(self):
        super(Statistics_class_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.select_query = QComboBox()
        self.query = QLineEdit()
        self.search = QPushButton("搜索")
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
        self.select_query.addItems(['号码','姓名'])
        self.select_query.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.search.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                         QPushButton{background-color:rgb(170,200, 50)}\
                                         QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.query.setPlaceholderText("请输入搜索内容")
        self.query.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.returnbut.setMaximumSize(100, 40)
        self.select_query.setMaximumSize(80, 40)
        self.query.setMaximumSize(350, 40)
        self.search.setMaximumSize(80, 40)
        self.lab.setMaximumSize(200, 40)
        self.layout.addWidget(self.select_query, 0, 10, 1, 1)
        self.layout.addWidget(self.query, 0, 11, 1, 5)
        self.layout.addWidget(self.search, 0, 16, 1, 1)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 0, 8, 19)


class classWidget(QWidget):
    def __init__(self, data):
        super(classWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.courselab = QLabel("加课天数:")
        self.joinlab = QLabel("学习用时:")
        self.numlab = QLabel("平均学习:")
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(data[2], abcd)
        a = (new - a1).days + 1
        self.courselab2 = QLabel(str(a)+"　天")
        ab = data[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.joinlab2 = QLabel(ac)
        ad = ab / a
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.numlab2 = QLabel(ae)
        self.image_path = "./datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.joinlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.joinlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.courselab.setMaximumSize(80, 40)
        self.joinlab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80, 40)
        self.courselab2.setMaximumSize(100, 40)
        self.joinlab2.setMaximumSize(100, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.courselab, 1, 8, 1, 1)
        self.layout.addWidget(self.joinlab, 2, 8, 1, 1)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.courselab2, 1, 9, 1, 2)
        self.layout.addWidget(self.joinlab2, 2, 9, 1, 2)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)

class Classwindow(QListWidget):
    def __init__(self, dow,data1):
        super(Classwindow, self).__init__()
        self.dow = dow
        self.data = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('./datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?)", (data1,data1,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data)

class Classwindow2(QListWidget):
    def __init__(self, dow,data1,data2):
        super(Classwindow2, self).__init__()
        self.dow = dow
        self.data1 = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?) \
                     and Join_Course.number=(?)", (data1,data1,data2,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data1)

class Classwindow3(QListWidget):
    def __init__(self, dow,data1,data2):
        super(Classwindow3, self).__init__()
        self.dow = dow
        self.data1 = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?) \
                     and User_date.name like (?)", (data1,data1,data2,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data1)