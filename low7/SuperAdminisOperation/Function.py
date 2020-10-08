from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import SuperAdminisOperation
from SuperAdminisOperation import Controller_news,Reptile,Addfile
from SuperAdminisInterface.Function_win import Function_win


# 超级管理员功能
class Function(QFrame):
    def __init__(self):
        super(Function, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.function = Function_win
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.function)

        self.function.mainbutton1.clicked.connect(self.select_fun1)
        self.function.mainbutton2.clicked.connect(self.select_fun2)
        self.function.mainbutton3.clicked.connect(self.select_fun3)

    def select_fun1(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0,Controller_news.Controller_news())

    def select_fun2(self):  # 连接爬虫
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Reptile.Reptile())

    def select_fun3(self):  # 连接添加资料
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Addfile.Addfile())