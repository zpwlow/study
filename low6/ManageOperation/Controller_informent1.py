from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Controller_myself
from ManageInterface.Controller_informent1_win import Controller_informent1_win
import sqlite3




class Controller_informent1(QFrame):
    def __init__(self):
        super(Controller_informent1, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.informent = Controller_informent1_win
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.informent)

        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)", (ManageOperation.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.informent.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.informent.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.informent.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.informent.nameEdit.setText(self.data[1])
        self.informent.schoolEiit.setText(self.data[4])
        self.informent.sure.clicked.connect(self.connect_fun)
        self.informent.returnBtn.clicked.connect(self.return_fun)

    def return_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_myself.Controller_myself())

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
        ManageOperation.win.splitter.insertWidget(0, Controller_myself.Controller_myself())