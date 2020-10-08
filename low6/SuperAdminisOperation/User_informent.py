from PyQt5.QtWidgets import QHBoxLayout,QFileDialog,QApplication
from PyQt5.QtWidgets import QFrame,QMessageBox
from PyQt5.QtGui import QPixmap
import base64,sqlite3,os,datetime
import SuperAdminisOperation
from SuperAdminisOperation import Controller_news
from SuperAdminisInterface.User_informent_win import User_informent_win



class User_informent(QFrame):
    def __init__(self,number):
        super(User_informent, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.informent =  User_informent_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.informent)

        self.number = number
        self.image()
        self.informent.sure.clicked.connect(self.connect_fun)
        self.informent.chang_image.clicked.connect(self.chang_fun)

    def image(self):
        self.image_path = "./datas/image/a7.jpeg"
        self.file = os.path.splitext(self.image_path)[1]
        self.informent.tupian.setPixmap(QPixmap(self.image_path))
        self.informent.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
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
        b = self.informent.yearcb.currentText() + '-' + self.informent.monthcb.currentText()
        c = self.informent.sexcb.currentText()
        d = self.informent.schoolEiit.text()
        e = self.informent.gradecb.currentText()
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab)
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_date VALUES(?,?,?,?,?,?)", (self.number, a, b, c, d, e))
        conn.execute("insert into User_image values(?,?,?)",(self.number, total, self.file,))
        conn.execute("INSERT INTO Student_date VALUES(?,?,?,?,?)",
                     (self.number, theTime, 1, 0.0, theTime))
        conn.commit()
        conn.close()
        sqlpath = "./datas/database/SQ" + str(self.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:                                  # 开始时间  ， 课程号，课程名， 文件名 ， 结束时间
            c.execute('''CREATE TABLE User_data(strat_time text,Cno text,Coursename text, filename text,last_time text)''')
        except:
            pass
        c.close()
        conn.close()

    def connect_fun(self):
        if len(self.informent.nameEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "姓名框不能为空！！")
            self.informent.nameEdit.setFocus()
        if len(self.informent.schoolEiit.text()) == 0:
            QMessageBox.about(self, "提示!", "学校框不能为空！！")
            self.informent.schoolEiit.setFocus()
        else:
            self.save_data()
            SuperAdminisOperation.win.splitter.widget(0).setParent(None)
            SuperAdminisOperation.win.splitter.insertWidget(0, Controller_news.Controller_news())
            QMessageBox.about(self, "提示", '添加用户成功!!')
