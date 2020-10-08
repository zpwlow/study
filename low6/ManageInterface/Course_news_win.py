from PyQt5.QtWidgets import QWidget,QToolBox, QPushButton, QGridLayout,QLabel,QMenu
from PyQt5.QtWidgets import QHBoxLayout,QMessageBox,QListWidget,QListWidgetItem,QAction
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtCore import QSize
import base64,sqlite3,shutil,os,zipfile,glob
import ManageOperation

class Course_news_win(QWidget):
    def __init__(self):
        super(Course_news_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.addcufile = QPushButton("添加课件")
        self.addexfile = QPushButton("添加练习")
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
        self.addcufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addexfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.addcufile.setMaximumSize(100, 40)
        self.addexfile.setMaximumSize(100,40)
        self.lab.setMaximumSize(200, 40)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.addcufile,0,15,1,2)
        self.layout.addWidget(self.addexfile, 0, 17, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)


#课件的item 设计
class CoursecuWidget(QWidget):
    def __init__(self, data):
        super(CoursecuWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
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
class CoursecuQlist(QListWidget):
    def __init__(self, dow, data):
        super(CoursecuQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                  Filename,Fileimage where Filename.no = Fileimage.no \
                   and Cno=(?) ", (data[0],))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CoursecuWidget(data))

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
            rely = QMessageBox.question(self, "提示!", "该操作会造成数据完全删除无法恢复\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Filename where no=(?)",(self.datas[index][0],))
            c.execute("delete from Fileimage where no=(?)", (self.datas[index][0],))
            c.execute("delete from Filedate where no=(?)", (self.datas[index][0],))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '文件删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Cname,name,total,filename1 from \
                       Filename,Filedate where Filename.no= Filedate.no \
                        and Filename.no=(?)",(da[0],))
            filedata = c.fetchall()[0]
            zip_path = './datas/'+filedata[0]
            if (not (os.path.exists(zip_path))):  # 创建文件夹。
                os.makedirs(zip_path)
            zip_path = zip_path +'/'+filedata[1]+filedata[3]
            total = base64.b64decode(filedata[2])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            zip_to_files(zip_path)
            self.dow.clicked()



#练习的item 设计
class CourseexWidget(QWidget):
    def __init__(self, data):
        super(CourseexWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.namelab = QLabel(data[1])
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.namelab.setMaximumSize(800, 60)
        self.layout.addWidget(self.namelab, 1, 1, 1, 1)

#练习的QList
class CourseexQlist(QListWidget):
    def __init__(self, dow, data):
        super(CourseexQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select no,name from Filename2 where Cno=(?) ", (data[0],))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 80))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CourseexWidget(data))

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
            rely = QMessageBox.question(self, "提示!", "该操作会造成数据完全删除无法恢复\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = "../datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Filename2 where no=(?)",(self.datas[index][0],))
            c.execute("delete from Filedate2 where no=(?)", (self.datas[index][0],))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '文件删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            sqlpath = "../datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Cname,name,answer,total,filename1 from \
                       Filename2,Filedate2 where Filename2.no= Filedate2.no \
                        and Filename2.no=(?)",(da[0],))
            filedata = c.fetchall()[0]
            zip_path = '../datas/'+filedata[0]
            if (not (os.path.exists(zip_path))):  # 创建文件夹。
                os.makedirs(zip_path)
            zip_path = zip_path +'/'+filedata[1]+filedata[4]
            total = base64.b64decode(filedata[3])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            zip_to_files(zip_path)
            self.dow.clicked2(da[0],filedata[2])




def zip_to_files(zippath):  # 将压缩包解压
    path = './datas/tupian'
    if (os.path.isdir(path)):  # 判断文件夹是否存在
        fileNames = glob.glob(path + r'/*')
        if fileNames:
            for fileName in fileNames:  # 将pa 文件夹中的文件删除。
                os.remove(fileName)
    else:
        os.mkdir(path)
    zf = zipfile.ZipFile(zippath)
    for fn in zf.namelist():  # 循环压缩包中的文件并保存进新文件夹。
        #right_fn = fn.replace('\\\\', '_').replace('\\', '_').replace('//', '_').replace('/', '_')  # 将文件名正确编码
        right_fn = fn.encode('cp437').decode('gbk')  # 将文件名正确编码
        right_fn = path + '/' + right_fn
        with open(right_fn, 'wb') as output_file:  # 创建并打开新文件
            with zf.open(fn, 'r') as origin_file:  # 打开原文件
                shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
    zf.close()
    os.remove(zippath)