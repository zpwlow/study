from PyQt5.QtWidgets import QWidget,QToolBox, QPushButton, QGridLayout,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QMessageBox,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtCore import QSize
import base64,sqlite3,shutil,os,zipfile,glob
import ManageOperation

#添加系统课件
class Add_System_win(QWidget):
    def __init__(self):
        super(Add_System_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.doubleselect = QPushButton("重新选择")
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
        self.doubleselect.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.doubleselect.setMaximumSize(100,40)
        self.lab.setMaximumSize(200, 40)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.doubleselect,0,17,1,2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)

#添加系统课件的item 设计
class AddsystemWidget(QWidget):
    def __init__(self,dow,data,da):
        super(AddsystemWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.dow = dow
        self.data = data
        self.da = da
        self.imagelab = QLabel()
        self.addbut = QPushButton("添加")
        self.namelab = QLabel(da[0])
        self.image_path = "../datas/image/image" + da[4]
        total = base64.b64decode(da[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.addbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(800, 80)
        self.addbut.setMaximumSize(80,40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.addbut.clicked.connect(self.addfile)
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.addbut,3,8,1,1)

    def addfile(self):
        sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Filename")
        no = len(c.fetchall())
        c.execute("insert into Filename VALUES(?,?,?,?,?,?)",
                  ('C' + str(no), self.data[0], self.data[1], self.da[0], self.da[2], self.da[4]))
        c.execute("insert into Fileimage values(?,?)", ('C' + str(no), self.da[3]))
        c.execute("insert into Filedate values(?,?)", ('C' + str(no), self.da[1]))
        conn.commit()
        c.close()
        conn.close()
        QMessageBox.about(self, "提示", '添加成功!!')


#添加系统课件的QList
class AddsystemQlist(QListWidget):
    def __init__(self, dow, data,greade,course):
        super(AddsystemQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "./datas/database/Data.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        if greade[:3]=="一年级":
            c.execute("select name,First_Grade_data.total,First_Grade.filename, \
                            First_Grade_image.total,First_Grade_image.filename from \
                            First_Grade,First_Grade_data,First_Grade_image  where \
                            First_Grade.no = First_Grade_data.no and First_Grade.no =First_Grade_image.no \
                            and level2=(?) and level3=(?)",(greade,course))
        else:
            QMessageBox.about(self, "提示", '其他功能暂未实现!!')
        self.datas = c.fetchall()
        for da in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, AddsystemWidget(self,data,da))


    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index]
            zip_path = "./datas/wen/xinwen.zip"
            total = base64.b64decode(da[1])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            self.zip_to_files(zip_path)
            self.dow.clicked()

    def zip_to_files(self, zippath):  # 将压缩包解压
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