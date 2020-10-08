from PyQt5.QtWidgets import QWidget,QApplication, QPushButton, QGridLayout
from PyQt5.QtWidgets import QHBoxLayout

#添加练习
class Addexfile_win(QWidget):
    def __init__(self):
        super(Addexfile_win, self).__init__()
        self.returnbut = QPushButton("返回")
        self.addfile = QPushButton("添加文件")
        self.addmufile = QPushButton("添加目录")
        self.addsystem = QPushButton("从系统添加")
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b = self.screenRect.height() * 1.0 / 4
        a = self.screenRect.width() * 1.0 / 5
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addmufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addsystem.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.layout.addWidget(self.returnbut, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.addfile,0 , 1)
        self.layout.addWidget(self.addmufile, 1, 0)
        self.layout.addWidget(self.addsystem,1,1)
        self.returnbut.setMaximumSize(a, b)
        self.addfile.setMaximumSize(a, b)
        self.addmufile.setMaximumSize(a, b)
        self.addsystem.setMaximumSize(a,b)