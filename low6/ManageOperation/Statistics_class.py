from PyQt5.QtWidgets import QHBoxLayout,QMessageBox
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import User_report,Statistics_news
from ManageInterface.Statistics_class_win import Statistics_class_win,Classwindow,Classwindow2,Classwindow3
import sqlite3



class Statistics_class(QFrame):
    def __init__(self,data):
        super(Statistics_class, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.function = Statistics_class_win
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.function)

        self.data = data
        self.window = Classwindow(self, self.data[0])
        self.function.qtool.addItem(self.window, "学生学习信息")
        self.function.returnbut.clicked.connect(self.returnfun)
        self.function.search.clicked.connect(self.chang_fun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_news.Statistics_news())


    def clicked(self, data1,data2):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, User_report.User_report(data1,data2))

    def chang_fun(self):
        if (self.function.select_query.currentText() == '号码'):
            no = self.query.text()
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where Cno=(?) and number=(?)",(self.data[0],no,))
            self.datas = c.fetchall()
            if len(self.datas)>0:
                self.function.qtool.removeItem(0)
                self.coursewin = Classwindow2(self,self.data[0],no)
                self.function.qtool.addItem(self.coursewin, '查找的学生')
                self.function.query.setText("")
            else:
                QMessageBox.about(self, "抱歉!", "没有找到号码为:'"+no+"'的信息!!!")
        elif (self.function.select_query.currentText() == '姓名'):
            no = self.query.text()
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course,User_date where\
                 Join_Course.number=User_date.number and Cno=(?) and name like (?)", (self.data[0],'%'+no+'%',))
            self.datas = c.fetchall()
            if len(self.datas)>0:
                self.function.qtool.removeItem(0)
                self.coursewin = Classwindow3(self,self.data[0],'%'+no+'%')
                self.function.qtool.addItem(self.coursewin, '查找的学生')
                self.function.query.setText("")
            else:
                QMessageBox.about(self, "抱歉!", "没有找到号码为:'"+no+"'的信息!!!")