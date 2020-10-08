from PyQt5.QtWidgets import  QMessageBox
import ManageOperation
from ManageInterface import User_report_win, Statistics_news_win
from ManageInterface.Statistics_class_win import Classwindow, Classwindow2, Classwindow3
import sqlite3


class Statistics_class:
    def __init__(self, win):
        super(Statistics_class, self).__init__()
        self.function = win
        self.window = Classwindow(self, self.function.data[0])
        self.function.qtool.addItem(self.window, "学生学习信息")
        self.function.returnbut.clicked.connect(self.returnfun)
        self.function.search.clicked.connect(self.chang_fun)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_news_win.Statistics_news_win())

    def clicked(self, data1, data2):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, User_report_win.User_report_win(data1, data2))

    def chang_fun(self):
        if self.function.select_query.currentText() == '号码':
            no = self.function.query.text()
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where Cno=(?) and number=(?)",
                      (self.function.data[0], no,))
            self.datas = c.fetchall()
            if len(self.datas) > 0:
                self.function.qtool.removeItem(0)
                self.coursewin = Classwindow2(self, self.function.data[0], no)
                self.function.qtool.addItem(self.coursewin, '查找的学生')
                self.function.query.setText("")
            else:
                QMessageBox.about(self.function, "抱歉!", "没有找到号码为:'" + no + "'的信息!!!")
        elif self.function.select_query.currentText() == '姓名':
            no = self.function.query.text()
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course,User_date where\
                 Join_Course.number=User_date.number and Cno=(?) and name like (?)",
                      (self.function.data[0], '%' + no + '%',))
            self.datas = c.fetchall()
            if len(self.datas) > 0:
                self.function.qtool.removeItem(0)
                self.coursewin = Classwindow3(self, self.function.data[0], '%' + no + '%')
                self.function.qtool.addItem(self.coursewin, '查找的学生')
                self.function.query.setText("")
            else:
                QMessageBox.about(self.function, "抱歉!", "没有找到号码为:'" + no + "'的信息!!!")
