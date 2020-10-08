import ManageOperation
from ManageInterface import AddCourse_win, Function_win, Course_news_win
from ManageInterface.Class_news_win import Coursewindow


# 用户注册操作类
class Class_news:
    def __init__(self, win):
        super(Class_news, self).__init__()
        self.news = win
        self.add = AddCourse_win.AddCourse_win()
        self.window = Coursewindow.Coursewindow(self)
        self.news.qtool.addItem(self.window, '我的课程')

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function_win.Function_win())

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
        ManageOperation.win.splitter.insertWidget(0, Course_news_win.Course_news_win(data))
