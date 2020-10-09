from PyQt5.QtWidgets import QMessageBox
import sqlite3
import SuperAdminisOperation
from SuperAdminisInterface import Edit_Controller_win


class Chang_Controller_amend:
    def __init__(self, win):
        super(Chang_Controller_amend, self).__init__()
        self.chang = win
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller where number=(?)", (self.chang.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.chang.usrlab1.setText(self.chang.number)
        self.chang.amendedit1.setText(self.data[2])
        self.chang.returnBtn.clicked.connect(self.return_fun)
        self.chang.amendedit2.returnPressed.connect(self.enterPress2)
        self.chang.sure.clicked.connect(self.accept)

    def return_fun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Edit_Controller_win.Edit_Controller_win(self.number))

    def enterPress2(self):
        if len(self.chang.amendedit2.text()) == 0:
            QMessageBox.about(self.chang, "提示!", "新密码框不能为空！")
            self.chang.amendedit2.setFocus()
        else:
            self.chang.amendedit3.setFocus()

    def accept(self):
        if len(self.chang.amendedit2.text()) == 0:
            QMessageBox.about(self.chang, "提示!", "新密码框不能为空！")
            self.chang.amendedit2.setFocus()
        elif len(self.chang.amendedit3.text()) == 0:
            QMessageBox.about(self.chang, "提示!", "确认密码框不能为空！")
            self.chang.amendedit3.setFocus()
        elif self.chang.amendedit3.text() != self.chang.amendedit2.text():
            QMessageBox.about(self.chang, "提示!", "前后密码输入不一样！")
            self.chang.amendedit3.setFocus()
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            conn.execute("update Controller set password=(?) where number=(?)",
                         (self.chang.amendedit2.text(), self.chang.number,))
            conn.commit()
            conn.close()
            QMessageBox.about(self.chang, "提示!", "修改密码成功！！！")
            SuperAdminisOperation.win.splitter.widget(0).setParent(None)
            SuperAdminisOperation.win.splitter.insertWidget(0, Edit_Controller_win.Edit_Controller_win(self.chang.number))
