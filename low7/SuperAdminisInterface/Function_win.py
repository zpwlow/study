from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QFrame
from PyQt5.QtWidgets import QHBoxLayout

# 超级管理员功能界面
from SuperAdminisOperation import Function


class Function_win(QFrame):
    def __init__(self):
        super(Function_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Function.Function(self)
        self.mainbutton1 = QPushButton("管理信息")  # 用户功能界面的控件
        self.mainbutton2 = QPushButton("爬虫")
        self.mainbutton3 = QPushButton("添加资料")
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

        self.mainbutton1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.layout.addWidget(self.mainbutton1, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.mainbutton2, 0, 1)
        self.layout.addWidget(self.mainbutton3, 0, 2)
        self.mainbutton1.setMaximumSize(a, b)
        self.mainbutton2.setMaximumSize(a, b)
        self.mainbutton3.setMaximumSize(a, b)