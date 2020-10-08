from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel,QMessageBox
from PyQt5.QtWidgets import QHBoxLayout,QApplication,QComboBox
from PyQt5.QtCore import Qt



class Addfile_win(QWidget):
    def __init__(self):
        super(Addfile_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.addfile = QPushButton("添加文件")
        self.addmufile = QPushButton("添加目录")
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b = self.screenRect.height() * 1.0 / 5
        a = self.screenRect.width() * 1.0 / 3

        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addmufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.layout.addWidget(self.returnbut, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.addfile, 1, 0)
        self.layout.addWidget(self.addmufile, 2, 0)
        self.returnbut.setMaximumSize(a, b)
        self.addfile.setMaximumSize(a, b)
        self.addmufile.setMaximumSize(a, b)


class Select_location(QWidget):
    def __init__(self,dow):
        super(Select_location, self).__init__()
        self.dow = dow
        self.setWindowTitle("选择文件保存位置")
        self.lab = QLabel("请选择文件保存的位置！！！！")
        self.typelab = QLabel("学习阶段")
        self.typebox = QComboBox()
        self.greadelab = QLabel("年级")
        self.greadebox = QComboBox()
        self.courselab = QLabel("科目")
        self.coursebox = QComboBox()
        self.sure = QPushButton("确定")
        self.devise_ui()

    def devise_ui(self):
        self.resize(750, 400)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            Qt.WindowCloseButtonHint |Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作

        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.lab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.typelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.greadelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.lab.setMaximumSize(400,80)
        self.typelab.setMaximumSize(80,50)
        self.greadelab.setMaximumSize(80,50)
        self.courselab.setMaximumSize(80,50)
        self.typebox.setMaximumSize(160, 50)
        self.greadebox.setMaximumSize(160, 50)
        self.coursebox.setMaximumSize(160, 50)
        self.sure.setMaximumSize(80,50)
        self.typebox.addItems(['','小学','初中','高中'])
        self.typebox.currentIndexChanged.connect(self.fun1)
        self.sure.clicked.connect(self.surefun)
        self.layout.addWidget(self.lab,0,2,1,6)
        self.layout.addWidget(self.typelab,1,0,1,1)
        self.layout.addWidget(self.typebox,1,1,1,2)
        self.layout.addWidget(self.greadelab,1,3,1,1)
        self.layout.addWidget(self.greadebox,1,4,1,2)
        self.layout.addWidget(self.courselab,1,6,1,1)
        self.layout.addWidget(self.coursebox,1,7,1,2)
        self.layout.addWidget(self.sure,2,8,1,1)

    def fun1(self):
        self.greadebox.clear()
        self.coursebox.clear()
        if self.typebox.currentText()=="小学":
            self.greadebox.addItems(['','一年级上册','一年级下册','二年级上册','二年级下册','三年级上册','三年级下册',
                                     '四年级上册','四年级下册','五年级上册','五年级下册','六年级上册','六年级下册'])
            self.coursebox.addItems(['','语文','数学','英语'])
        elif self.typebox.currentText()=="初中":
            self.greadebox.addItems(['','初一上册','初一下册','初二上册','初二下册','初三上册','初三下册',])
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])
        elif self.typebox.currentText()=="高中":
            self.greadebox.addItems(['','必修一','必修二','必修三','必修四','必修五',
                                     '选修一','选修二','选修三','选修四','选修五'])
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])

    def fun2(self):
        self.greadebox.clear()
        self.coursebox.clear()
        self.typebox.clear()
        self.typebox.addItems(['', '小学', '初中', '高中'])

    def surefun(self):
        if(self.greadebox.currentText()==""):
            QMessageBox.about(self, "提示", '年级的选项框不能为空!!')
        elif(self.typebox.currentText()==""):
            QMessageBox.about(self, "提示", '学习阶段的选项框不能为空!!')
        elif (self.coursebox.currentText()==""):
            QMessageBox.about(self, "提示", '科目的选项框不能为空!!')
        self.close()
        self.dow.clicked()

    def gettype(self):
        return self.typebox.currentText()

    def getgrade(self):
        return self.greadebox.currentText()

    def getcourse(self):
        return self.coursebox.currentText()
