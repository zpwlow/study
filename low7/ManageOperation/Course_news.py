import ManageOperation
from ManageInterface import Class_news_win, Addcufile_win, Addexfile_win, Max_widget_win, Addexfileanswer_win
from ManageInterface.Course_news_win import CoursecuQlist, CourseexQlist


class Course_news:
    def __init__(self, win):
        super(Course_news, self).__init__()
        self.course = win
        self.window1 = CoursecuQlist(self, self.course.data)
        self.window2 = CourseexQlist(self, self.course.data)
        self.course.qtool.addItem(self.window1, self.course.data[1] + "　课件")
        self.course.qtool.addItem(self.window2, self.course.data[1] + "　练习")

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Class_news_win.Class_news_win())

    def addcufun(self):
        addcufile = Addcufile_win.Addcufile_win(self.course.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, addcufile)

    def addexfun(self):
        addexfile = Addexfile_win.Addexfile_win(self.course.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, addexfile)

    def clicked(self):
        self.max = Max_widget_win.Max_widget_win()
        self.max.show()

    def clicked2(self, data, answer):
        self.add = Addexfileanswer_win.Addexfileanswer_win(data, answer)
        self.add.show()
