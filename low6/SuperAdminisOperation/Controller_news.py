from PyQt5.QtWidgets import QHBoxLayout,QTableWidgetItem,QCheckBox
from PyQt5.QtWidgets import QFrame,QMessageBox,QToolBox,QWidget
from PyQt5.QtGui import Qt,QBrush,QColor
from captcha.image import ImageCaptcha
import random,sqlite3
import SuperAdminisOperation
from SuperAdminisOperation import User_Logon,Edit_Controller,Function,Controller_Logon,Edit_user
from SuperAdminisInterface.Controller_news_win import Controller_news_win,CourseQlist




class Controller_news(QFrame):
    def __init__(self):
        super(Controller_news, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.news = Controller_news_win
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.news)

        self.data = []
        self.news.returnbut.clicked.connect(self.returnfun)
        self.news.addusr.clicked.connect(self.addusrfun)
        self.news.addcontroller.clicked.connect(self.addcontrollerfun)
        self.news.seeapply.clicked.connect(self.seeapplyfun)
        self.news.editbut.clicked.connect(self.edit_fun)
        self.news.searchbut.clicked.connect(self.searchfun)
        self.news.deletebut.clicked.connect(self.deletedata)

    def returnfun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Function.Function())

    def addusrfun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, User_Logon.User_Logon())

    def addcontrollerfun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Controller_Logon.Controller_Logon())

    def seeapplyfun(self):
        self.news.table.close()
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window = CourseQlist()
        self.qtool.addItem(self.window, "管理员申请注册")
        self.news.win_layout2.addWidget(self.qtool, 2, 0, 18, 20)
        self.qtool.show()

    def edit_fun(self):
        n =0
        for data in self.data:
            if data[0].isChecked():
                n+=1
        if n != 1:
            QMessageBox.about(self, "提示!", "抱歉，该功能只能选择一个用户进行编辑！！" )
            return
        for data in self.data:
            if data[0].isChecked():
                if data[2]=="用户":
                    SuperAdminisOperation.win.splitter.widget(0).setParent(None)
                    SuperAdminisOperation.win.splitter.insertWidget(0, Edit_user.Edit_user(data[1]))
                elif data[2] == "管理员":
                    SuperAdminisOperation.win.splitter.widget(0).setParent(None)
                    SuperAdminisOperation.win.splitter.insertWidget(0, Edit_Controller.Edit_Controller(data[1]))


    def searchfun(self):
        self.news.table.setColumnCount(7)
        self.news.table.setHorizontalHeaderLabels(['选择', '用户', '姓名', '出生年月', '性别', '学校', '身份'])
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        d = self.news.query.text()
        if (d ==''):
            QMessageBox.about(self, "提示!", "搜索内容不能为空！！！")
            return
        elif (self.news.selectbox.currentText() == '姓名'):
            c.execute("select * from User_date where name = (?)", (d, ))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where name =(?) ",(d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b+c)>0:
                self.news.table.setRowCount(b+c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],"用户"])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.news.table.item(i, 2).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.news.table.item(i, 2).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有查到任何信息" )
        elif (self.news.selectbox.currentText() == '号码'):
            c.execute("select * from User_date where number = (?)", (d,))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where number =(?) ", (d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b + c) > 0:
                self.news.table.setRowCount(b + c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'用户'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.news.table.item(i, 1).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.news.table.item(i, 1).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有该用户的任何信息" )
        elif (self.news.selectbox.currentText() == '学校'):
            c.execute("select * from User_date where school = (?)", (d,))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where school =(?) ", (d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b + c) > 0:
                self.news.table.setRowCount(b + c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'用户'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.news.table.item(i, 5).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.news.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.news.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.news.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.news.table.item(i, 5).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有该用户的任何信息" )
        try:
            self.qtool.close()
            self.qtool.deleteLater()
        except:
            pass
        self.news.query.setText("")
        self.news.win_layout2.addWidget(self.table, 2, 0, 18, 20)
        self.news.table.show()

    def deletedata(self):
        n = 0
        for data in self.data:
            if data[0].isChecked():
                n += 1
        if n == 0:
            QMessageBox.about(self, "提示!", "您没有选择任何用户，请您重新选择！！")
            return
        rely = QMessageBox.question(self, "提示!", "该操作会造成数据无法恢复！！！\n确定删除？？？" , QMessageBox.Yes|QMessageBox.No ,QMessageBox.Yes)
        if rely ==  65536:
            return
        removeline =[]
        for data in self.data:
            if data[0].isChecked():
                row = self.news.table.rowCount()
                for x in range(row, 0, -1):
                    if data[1] == self.news.table.item(x ,1).text():
                        self.news.table.removeRow(x)
                        removeline.append(data)
        if len(removeline)>0:
            for line in removeline:
                self.data.remove(line)
        sqlpath ='./datas/database/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        for line in removeline:
            if line[2]=="用户":
                c.execute("delete from User where number = (?)", (line[1],))
                c.execute("delete from User_image where number = (?)", (line[1],))
                c.execute("delete from User_date where number = (?)", (line[1],))
                c.execute("delete from Student_date where number = (?)", (line[1],))
            elif line[2]=="管理员":
                c.execute("delete from Controller where number = (?)", (line[1],))
                c.execute("delete from Controller_data where number = (?)", (line[1],))
                c.execute("delete from Controller_image where number = (?)", (line[1],))
        conn.commit()
        c.close()
        conn.close()
