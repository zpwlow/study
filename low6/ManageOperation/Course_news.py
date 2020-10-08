from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Class_news,Max_widget,Addcufile,Addexfile,Addexfileanswer
from ManageInterface.Course_news_win import Course_news_win,CoursecuQlist,CourseexQlist




class Course_news(QFrame):
    def __init__(self,data):
        super(Course_news, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.course = Course_news_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.course)

        self.data = data
        self.window1 = CoursecuQlist(self, self.data)
        self.window2 = CourseexQlist(self, self.data)
        self.course.qtool.addItem(self.window1, self.data[1] + "　课件")
        self.course.qtool.addItem(self.window2, self.data[1] + "　练习")
        self.returnbut.clicked.connect(self.returnfun)
        self.addcufile.clicked.connect(self.addcufun)
        self.addexfile.clicked.connect(self.addexfun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Class_news.Class_news())

    def addcufun(self):
        addcufile = Addcufile.Addcufile(self.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, addcufile)

    def addexfun(self):
        addexfile = Addexfile.Addexfile(self.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, addexfile)


    def clicked(self):
        self.max = Max_widget.Max_widget()
        self.max.show()

    def clicked2(self,data,answer):
        self.add =  Addexfileanswer.Addexfileanswer(data,answer)
        self.add.show()