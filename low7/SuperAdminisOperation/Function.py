import SuperAdminisOperation
from SuperAdminisInterface import Controller_news_win, Reptile_win, Addfile_win


# 超级管理员功能
class Function:
    def __init__(self, win):
        super(Function, self).__init__()
        self.function = win
        self.function.mainbutton1.clicked.connect(self.select_fun1)
        self.function.mainbutton2.clicked.connect(self.select_fun2)
        self.function.mainbutton3.clicked.connect(self.select_fun3)

    def select_fun1(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0,Controller_news_win.Controller_news_win())

    def select_fun2(self):  # 连接爬虫
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Reptile_win.Reptile_win())

    def select_fun3(self):  # 连接添加资料
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Addfile_win.Addfile_win())