import ManageOperation
from ManageInterface import Statistics_class_win, Function_win
from ManageInterface.Statistics_news_win import Statisticswindow


# 超级管理员功能
class Statistics_news:
    def __init__(self, win):
        super(Statistics_news, self).__init__()
        self.statistics = win
        self.window = Statisticswindow(self)
        self.statistics.qtool.addItem(self.window, '我的课程')
        self.statistics.returnbut.clicked.connect(self.returnfun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function_win.Function_win())

    def clicked(self, data):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_class_win.Statistics_class_win(data))
