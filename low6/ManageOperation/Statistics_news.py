from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Function,Statistics_class
from ManageInterface.Statistics_news_win import Statistics_news_win,Statisticswindow



# 超级管理员功能
class Statistics_news(QFrame):
    def __init__(self):
        super(Statistics_news, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.statistics = Statistics_news_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.statistics)

        self.window = Statisticswindow(self)
        self.statistics.qtool.addItem(self.window, '我的课程')
        self.statistics.returnbut.clicked.connect(self.returnfun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function.Function())

    def clicked(self, data):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_class.Statistics_class(data))