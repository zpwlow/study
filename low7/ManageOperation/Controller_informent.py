from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
import os, sqlite3, time, base64
import ManageOperation
from ManageInterface import Record_win


# 管理员信息填写
class Controller_informent:
    def __init__(self, win):
        super(Controller_informent, self).__init__()
        self.informent = win
        self.image()

    def image(self):
        self.image_path = "./datas/image/a7.jpeg"
        self.file = os.path.splitext(self.image_path)[1]
        self.informent.tupian.setPixmap(QPixmap(self.image_path))
        self.informent.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self.informent, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.image_path = path
            self.file = os.path.splitext(self.image_path)[1]
            self.informent.tupian.setPixmap(QPixmap(self.image_path))
            self.informent.tupian.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.image()

    def save_data(self):
        a = self.informent.nameEdit.text()
        b = self.informent.yearcb.currentText() + '-' \
            + self.informent.monthcb.currentText()
        c = self.informent.sexcb.currentText()
        d = self.informent.schoolEiit.text()
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("insert into Controller_image2 values(?,?,?)",
                     (ManageOperation.number, total, self.file,))
        conn.commit()
        conn.execute("INSERT INTO Controller_data2 VALUES(?,?,?,?,?)",
                     (ManageOperation.number, a, b, c, d,))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/ControllerSQ" +  str(ManageOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:  # 文件信息表 序号    课程号    课程名      文件名    文件后缀
            c.execute('''CREATE TABLE Filename(no text,Cno text,Cname text,name text,filename1 text,filename2 text)''')
        except:
            pass
        try:
            c.execute('''CREATE TABLE fileimage(no text,total LONGBLOB )''')
        except:
            pass
        try:
            c.execute('''CREATE TABLE Filedate(no text,total LONGBLOB )''')
        except:
            pass
        try:  # 文件信息表 序号    课程号    课程名      文件名  答案  文件后缀
            c.execute('''CREATE TABLE Filename2(no text,Cno text,Cname text,name text,answer text,filename1 text)''')
        except:
            pass
        try:
            c.execute('''CREATE TABLE Filedate2(no text,total LONGBLOB )''')
        except:
            pass
        c.close()
        conn.close()

    def connect_fun(self):
        if len(self.informent.nameEdit.text()) == 0:
            QMessageBox.about(self.informent, "提示!", "姓名框不能为空！！")
            self.informent.nameEdit.setFocus()
        if len(self.informent.schoolEiit.text()) == 0:
            QMessageBox.about(self.informent, "提示!", "学校框不能为空！！")
            self.informent.schoolEiit.setFocus()
        else:
            self.save_data()
            QMessageBox.about(self.informent, "提示!", "等待超级管理员的验证通过后再登录！！\n请您耐心等待！！")
            time.sleep(2)
            ManageOperation.win.splitter.widget(0).setParent(None)
            ManageOperation.win.splitter.insertWidget(0, Record_win.Record_win())
