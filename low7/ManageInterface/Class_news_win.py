from PyQt5.QtWidgets import QWidget, QToolBox, QPushButton, QGridLayout, QLabel, QMenu, QFrame
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem, QAction
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QSize
import base64, sqlite3
import ManageOperation
from ManageOperation import Class_news


class Class_news_win(QFrame):
    def __init__(self):
        super(Class_news_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Class_news.Class_news(self)
        self.returnbut = QPushButton("返回")
        self.addcourse = QPushButton("添加课程")
        self.lab = QLabel()
        self.returnbut.clicked.connect(self.datawindow.returnfun)
        self.addcourse.clicked.connect(self.datawindow.addfun)
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
        self.addcourse.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.addcourse.setMaximumSize(100, 40)
        self.lab.setMaximumSize(200, 40)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.addcourse, 0, 17, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)


class CustomWidget(QWidget):
    def __init__(self, data):
        super(CustomWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.courselab = QLabel("课程编号:")
        self.numlab = QLabel("人数:")
        self.courselab2 = QLabel(data[0])
        self.numlab2 = QLabel(str(data[2]))
        self.image_path = "./datas/image/image" + data[4]
        total = base64.b64decode(data[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.courselab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.courselab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80, 40)
        self.courselab2.setMaximumSize(100, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.courselab, 1, 8, 1, 1)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.courselab2, 1, 9, 1, 2)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)


class Coursewindow(QListWidget):
    def __init__(self, dow):
        super(Coursewindow, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
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
            self.setItemWidget(item, CustomWidget(data))

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            rely = QMessageBox.question(self, "提示!", "该操作会删除整个课程的数据\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Course where Cno=(?)", (self.datas[index][0]))
            c.execute("delete from Course_image where Cno=(?)", (self.datas[index][0]))
            c.execute("delete from Teacher_Course where Cno=(?)", (self.datas[index][0]))
            c.execute("delete from Join_Course where Cno=(?)", (self.datas[index][0]))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '课程删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            self.dow.clicked(da)
