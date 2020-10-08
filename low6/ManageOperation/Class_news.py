from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Function,AddCourse,Course_news
from ManageInterface.Class_news_win import Class_news_win,Coursewindow



#用户注册操作类
class Class_news(QFrame):
    def __init__(self):
        super(Class_news, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.news = Class_news_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.news)

        self.add = AddCourse.AddCourse()
        self.window = Coursewindow.Coursewindow(self)
        self.news.qtool.addItem(self.window, '我的课程')
        self.news.returnbut.clicked.connect(self.returnfun)
        self.news.addcourse.clicked.connect(self.addfun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function.Function())

    def addfun(self):
        self.add.nameEdit.setText('')
        self.add.image()
        # 接受子窗口传回来的信号  然后调用主界面的函数
        self.add.my_Signal.connect(self.changfun)
        self.add.show()

    def changfun(self):
        self.news.qtool.removeItem(0)
        self.window = Coursewindow.Coursewindow(self)
        self.news.qtool.addItem(self.window, '我的课程')

    def clicked(self, data):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Course_news.Course_news(data))