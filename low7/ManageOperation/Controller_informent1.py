import ManageOperation
from ManageInterface import Controller_myself_win
from ManageOperation import Controller_myself
import sqlite3


class Controller_informent1:
    def __init__(self, win):
        super(Controller_informent1, self).__init__()
        self.informent = win
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)",
                  (ManageOperation.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.informent.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.informent.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.informent.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.informent.nameEdit.setText(self.data[1])
        self.informent.schoolEiit.setText(self.data[4])

    def return_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_myself_win.Controller_myself_win())

    def save_data(self):
        a = self.informent.nameEdit.text()
        b = self.informent.yearcb.currentText() + '-' + self.informent.monthcb.currentText()
        c = self.informent.sexcb.currentText()
        d = self.informent.schoolEiit.text()
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("update Controller_data set name =(?),birthday=(?),sex=(?),school=(?) where number=(?)",
                     (a, b, c, d, ManageOperation.number))
        conn.commit()
        conn.close()

    def connect_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        self.save_data()
        Controller_myself.Controller_myself().devise_ui()
        ManageOperation.win.splitter.insertWidget(0, Controller_myself_win.Controller_myself_win())
