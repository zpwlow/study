from PyQt5.QtWidgets import  QMessageBox, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import ManageOperation
from ManageInterface import Class_news_win
import os, sqlite3, datetime, base64


# 添加课程
class AddCourse:
    def __init__(self,win):
        super(AddCourse, self).__init__()
        self.window = win
        self.image()


    def image(self):
        conn = sqlite3.connect('./datas/database/Information.db')
        c = conn.cursor()
        c.execute("select * from Course")
        b = len(c.fetchall())
        year = datetime.date.today().year
        self.Cno = str(year) + str(b)
        self.window.courselab2.setText(self.Cno)
        self.image_path = "../datas/image/a7.jpeg"
        self.file = os.path.splitext(self.image_path)[1]
        self.window.tupian.setPixmap(QPixmap(self.image_path))
        self.window.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self.window, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.image_path = path
            self.file = os.path.splitext(self.image_path)[1]
            self.window.tupian.setPixmap(QPixmap(self.image_path))
            self.window.tupian.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.image()

    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def conclefun(self):
        self.window.close()

    def save_data(self):
        name = self.window.nameEdit.text()
        filename = os.path.splitext(self.image_path)[1]
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO Course VALUES(?,?,?)", (self.Cno, name, 0,))
        conn.execute("INSERT INTO Course_image VALUES(?,?,?)", (self.Cno, total, filename,))
        conn.execute("INSERT INTO Teacher_Course VALUES(?,?)", (ManageOperation.number, self.Cno,))
        conn.commit()
        conn.close()

    def sure_fun(self):
        if len(self.window.nameEdit.text()) == 0:
            QMessageBox.about(self.window, "提示!", "课程名不能为空！！")
            self.window.nameEdit.setFocus()
        else:
            self.save_data()
            self.window.close()
            ManageOperation.win.splitter.widget(0).setParent(None)
            ManageOperation.win.splitter.insertWidget(0, Class_news_win.Class_news_win())
