from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Class_news,Statistics_news,Controller_myself
from ManageInterface.Function_win import Function_win



# 超级管理员功能
class Function(QFrame):
    def __init__(self):
        super(Function, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.function = Function_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.function)

        self.function.mainbutton1.clicked.connect(self.select_fun1)
        self.function.mainbutton2.clicked.connect(self.select_fun2)
        self.function.mainbutton3.clicked.connect(self.select_fun3)

    def select_fun1(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Class_news.Class_news())

    def select_fun2(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_news.Statistics_news())

    def select_fun3(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0,Controller_myself.Controller_myself())