
import ManageOperation
from ManageInterface import Class_news_win, Statistics_news_win, Controller_myself_win


# 超级管理员功能
class Function:
    def __init__(self, win):
        super(Function, self).__init__()
        self.function = win
        self.function.mainbutton1.clicked.connect(self.select_fun1)
        self.function.mainbutton2.clicked.connect(self.select_fun2)
        self.function.mainbutton3.clicked.connect(self.select_fun3)

    def select_fun1(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Class_news_win.Class_news_win())

    def select_fun2(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_news_win.Statistics_news_win())

    def select_fun3(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_myself_win.Controller_myself_win())
