from PyQt5.QtWidgets import QHBoxLayout,QApplication,QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
import ManageOperation
from ManageOperation import Function,Logon,Controller_amend,Controller_informent1
from ManageInterface.Controller_myself_win import Controller_myself_win
import sqlite3,base64,os




class Controller_myself(QFrame):
    def __init__(self):
        super(Controller_myself, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.myself = Controller_myself_win
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.myself)

        self.myself.withdraw.clicked.connect(self.return_win)
        self.myself.returnBtn.clicked.connect(self.return_fun)
        self.myself.ExditBtn.clicked.connect(self.edit_fun)
        self.myself.chang_image.clicked.connect(self.chang_fun)
        self.myself.amend.clicked.connect(self.amend_fun)
        self.image()

    def image(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_image where number=(?)", (ManageOperation.number,))
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
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
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
        ManageOperation.win.splitter.insertWidget(0, Controller_amend.Controller_amend())

    def return_win(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Logon.Logon())

    def return_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Function.Function())

    def edit_fun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Controller_informent1.Controller_informent1())