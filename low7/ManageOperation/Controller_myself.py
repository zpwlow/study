import base64
import os
import sqlite3

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog

import ManageOperation
from ManageInterface import Controller_informent1_win, Function_win, Logon_win, Controller_amend_win


class Controller_myself:
    def __init__(self, win):
        super(Controller_myself, self).__init__()
        self.myself = win
        self.image()

    def image(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_image where number=(?)",
                  (ManageOperation.number,))
        data = c.fetchall()[0]
        c.close()
        conn.close()
        self.image_path = "./datas/image/image" + data[2]
        total = base64.b64decode(data[1])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.myself.tupian.setPixmap(QPixmap(self.image_path))
        self.myself.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self.myself, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.file = os.path.splitext(path)[1]
            self.myself.tupian.setPixmap(QPixmap(path))
            self.myself.tupian.setScaledContents(True)  # 让图片自适应label大小
            with open(path, "rb") as f:
                total = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            conn.execute("update Controller_image set total = (?),filename = (?) where number = (?)",
                         (total, self.file, ManageOperation.number))
            conn.commit()
            conn.close()
        else:
            self.image()

    def amend_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_amend_win.Controller_amend_win())

    def return_win(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Logon_win.Logon_win())

    def return_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function_win.Function_win())

    def edit_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_informent1_win.Controller_informent1_win())
