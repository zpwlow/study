from PyQt5.QtWidgets import QHBoxLayout,QMessageBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
import ManageOperation
from ManageOperation import Controller_myself
from ManageInterface.Controller_amend_win import Controller_amend_win
import sqlite3,time




class Controller_amend(QFrame):
    def __init__(self):
        super(Controller_amend, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.amend = Controller_amend_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.amend)

        self.amend.returnBtn.clicked.connect(self.return_fun)
        self.amend.amendedit1.returnPressed.connect(self.enterPress1)
        self.amend.amendedit2.returnPressed.connect(self.enterPress2)
        self.amend.sure.clicked.connect(self.accept)

    def return_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_myself.Controller_myself())

    def enterPress1(self):
        if len(self.amend.amendedit1.text()) == 0:
            QMessageBox.about(self, "提示!", "原密码没有填写")
            self.amend.amendedit1.setFocus()
        else:
            self.amend.amendedit2.setFocus()

    def enterPress2(self):
        if len(self.amend.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amend.amendedit2.setFocus()
        else:
            self.amend.amendedit3.setFocus()

    def accept(self):
        if len(self.amend.amendedit1.text()) == 0:
            QMessageBox.about(self, "提示!", "原密码没有填写")
            self.amend.amendedit1.setFocus()
        elif len(self.amend.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amend.amendedit2.setFocus()
        elif len(self.amend.amendedit3.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amend.amendedit3.setFocus()
        elif self.amend.amendedit3.text() != self.amend.amendedit2.text():
            QMessageBox.about(self, "提示!", "前后密码输入不一样！")
            self.amend.amendedit3.setFocus()
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Controller")
            sign = 0
            for variate in c.fetchall():
                if variate[0] == ManageOperation.number and variate[2] == self.amend.amendedit1.text():
                    conn.execute("update Controller set password=(?) where number=(?)",
                                 (self.amend.amendedit2.text(), variate[0],))
                    conn.commit()
                    sign = 1
                    break
            c.close()
            conn.close()
            if sign == 0:
                QMessageBox.about(self, "提示!", "原密码输入错误！！")
                self.amend.amendedit1.setFocus()
            else:
                QMessageBox.about(self, "提示!", "修改成功！！")
                time.sleep(1)
                ManageOperation.win.splitter.widget(0).setParent(None)
                ManageOperation.win.splitter.insertWidget(0, Controller_myself.Controller_myself())