from PyQt5.QtWidgets import QWidget, QAbstractItemView, QPushButton, QGridLayout,QLineEdit,QListWidget
from PyQt5.QtWidgets import QHBoxLayout,QComboBox,QTableWidget,QHeaderView,QLabel,QMessageBox,QListWidgetItem
from PyQt5.QtGui import QFont,QPixmap,QColor
from PyQt5.QtCore import QSize
import base64,sqlite3

class Controller_news_win(QWidget):
    def __init__(self):
        super(Controller_news_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.addusr = QPushButton("添加用户")
        self.addcontroller = QPushButton("添加管理员")
        self.seeapply = QPushButton("查看申请")
        self.editbut = QPushButton("编辑")
        self.deletebut = QPushButton("删除")
        self.selectbox = QComboBox()
        self.query = QLineEdit()
        self.searchbut = QPushButton("搜索")
        self.table = QTableWidget()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.Lchild_win1 = QWidget()  # 左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)  # 设置左侧部件布局为网格
        self.Rchild_win1 = QWidget()  # 右侧控件布局
        self.win_layout2 = QGridLayout()  # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)  # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1, 0, 0, 20, 2)  # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1, 0, 2, 20, 20)  # 右侧部件在第1行第3列，占20行20列

        self.table.setStyleSheet("QTableWidget{background-color:rgb(235,235,235);font:13pt '宋体';font-weight:Bold;};")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不能编辑table
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addusr.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addcontroller.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.seeapply.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.editbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.deletebut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.searchbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.query.setPlaceholderText("请输入搜索内容")
        self.query.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.selectbox.addItems(['号码', '姓名','学校'])
        self.selectbox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.editbut.setMaximumSize(100,40)
        self.deletebut.setMaximumSize(100,40)
        self.selectbox.setMaximumSize(100,40)
        self.query.setMaximumSize(240,40)
        self.searchbut.setMaximumSize(100,40)
        self.win_layout1.addWidget(self.returnbut, 1, 0, 2, 2)
        self.win_layout1.addWidget(self.addusr, 3, 0, 2, 2)
        self.win_layout1.addWidget(self.addcontroller, 5, 0, 2, 2)
        self.win_layout1.addWidget(self.seeapply, 7, 0, 2, 2)
        self.win_layout2.addWidget(self.editbut,1,1,1,2)
        self.win_layout2.addWidget(self.deletebut,1,7,1,2)
        self.win_layout2.addWidget(self.selectbox,1,12,1,2)
        self.win_layout2.addWidget(self.query,1,14,1,4)
        self.win_layout2.addWidget(self.searchbut,1,18,1,2)
        self.win_layout2.addWidget(self.table,2,0,18,20)


class CourseWidget(QWidget):
    def __init__(self,dow, data):
        super(CourseWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.data = data
        self.dow = dow
        self.imagelab = QLabel()
        self.numberlab1 = QLabel("号码:")
        self.numberlab2 =QLabel(data[0])
        self.namelab1 = QLabel("姓名:")
        self.namelab2 = QLabel(data[3])
        self.yearlab1 = QLabel("出生年月:")
        self.yearlab2 = QLabel(data[4])
        self.sexlab1 = QLabel("性别:")
        self.sexlab2 = QLabel(data[5])
        self.schoollab1 = QLabel("学校:")
        self.schoollab2 = QLabel(data[6])
        self.agreebut = QPushButton("同意")
        self.rejectbut = QPushButton("拒绝")

        self.image_path = "./datas/image/image" + data[8]
        total = base64.b64decode(data[7])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.namelab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.namelab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numberlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numberlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.yearlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.yearlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sexlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sexlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.schoollab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.schoollab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.agreebut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(0,255, 0)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.rejectbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(255,0, 0)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab1.setMaximumSize(80, 40)
        self.namelab2.setMaximumSize(100, 40)
        self.numberlab1.setMaximumSize(80, 40)
        self.numberlab2.setMaximumSize(150, 40)
        self.yearlab1.setMaximumSize(80, 40)
        self.yearlab2.setMaximumSize(100, 40)
        self.sexlab1.setMaximumSize(80, 40)
        self.sexlab2.setMaximumSize(80, 40)
        self.schoollab1.setMaximumSize(80, 40)
        self.schoollab2.setMaximumSize(150, 40)
        self.agreebut.setMaximumSize(80,40)
        self.rejectbut.setMaximumSize(80,40)
        self.agreebut.clicked.connect(self.agreefun)
        self.rejectbut.clicked.connect(self.rejectfun)
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab1, 1, 3, 1, 1)
        self.layout.addWidget(self.namelab2,1,4,1,1)
        self.layout.addWidget(self.yearlab1,2,3,1,1)
        self.layout.addWidget(self.yearlab2,2,4,1,1)
        self.layout.addWidget(self.sexlab1,3,3,1,1)
        self.layout.addWidget(self.sexlab2,3,4,1,1)
        self.layout.addWidget(self.numberlab1,1,6,1,1)
        self.layout.addWidget(self.numberlab2,1,7,1,2)
        self.layout.addWidget(self.schoollab1,2,6,1,1)
        self.layout.addWidget(self.schoollab2,2,7,1,2)
        self.layout.addWidget(self.agreebut,3,9,1,1)
        self.layout.addWidget(self.rejectbut,3,10,1,1)

    def agreefun(self):
        sqlpath = "./datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        conn.execute("INSERT INTO Controller VALUES(?,?,?)", (self.data[0], self.data[1], self.data[2],))
        conn.execute("insert into Controller_image values(?,?,?)", (self.data[0], self.data[7], self.data[8],))
        conn.commit()
        conn.execute("INSERT INTO Controller_data VALUES(?,?,?,?,?)",
                     (self.data[0],self.data[3],self.data[4],self.data[5],self.data[6],))
        c.execute("delete from Controller2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_image2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_data2 where number=(?)", (self.data[0],))
        c.close()
        conn.commit()
        conn.close()
        self.dow.deleteitem(self.data[0])
        QMessageBox.about(self, "提示!", "操作成功！！")

    def rejectfun(self):
        sqlpath = "./datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("delete from Controller2 where number=(?)",(self.data[0],))
        c.execute("delete from Controller_image2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_data2 where number=(?)", (self.data[0],))
        conn.commit()
        c.close()
        conn.close()
        self.dow.deleteitem(self.data[0])
        QMessageBox.about(self, "提示!", "操作成功！！")

class CourseQlist(QListWidget):
    def __init__(self):
        super(CourseQlist, self).__init__()
        sqlpath = "./datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Controller2.number,usrname,password,name,birthday,sex,school,total,filename from \
                  Controller2,Controller_data2,Controller_image2 where \
                   Controller2.number = Controller_data2.number and \
                    Controller2.number = Controller_image2.number")
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CourseWidget(self,data))

    def deleteitem(self,data):
        x= 0
        for da in self.datas:
            if da[0]==data:
                item = self.takeItem(x)
                # 删除widget
                self.removeItemWidget(item)
                del item
                break
            x= x+1