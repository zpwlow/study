import sqlite3
import SuperAdminisOperation
from SuperAdminisInterface import Controller_news_win, Chang_Controller_amend_win


class Edit_Controller:
    def __init__(self, win):
        super(Edit_Controller, self).__init__()
        self.edit = win
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)",
                  (self.edit.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.edit.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.edit.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.edit.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.edit.nameEdit.setText(self.data[1])
        self.edit.schoolEiit.setText(self.data[4])
        self.edit.sure.clicked.connect(self.connect_fun)
        self.edit.returnBtn.clicked.connect(self.return_fun)
        self.edit.amend.clicked.connect(self.connect_fun1)

    def return_fun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Controller_news_win.Controller_news_win())

    def save_data(self):
        a = self.edit.nameEdit.text()
        b = self.edit.yearcb.currentText() + '-' + self.edit.monthcb.currentText()
        c = self.edit.sexcb.currentText()
        d = self.edit.schoolEiit.text()
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("update User_data set name =(?),birthday=(?),sex=(?),school=(?) where number=(?)",
                     (a, b, c, d, self.edit.number))
        conn.commit()
        conn.close()

    def connect_fun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        self.save_data()
        Controller_news_win.Controller_news_win().devise_ui()
        SuperAdminisOperation.win.splitter.insertWidget(0, Controller_news_win.Controller_news_win())

    def connect_fun1(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Chang_Controller_amend_win.Chang_Controller_amend_win(self.edit.number))
