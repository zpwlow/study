from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
import glob, os, zipfile, sqlite3, base64
import ManageOperation


class Addexfilewin:
    def __init__(self, win):
        super(Addexfilewin, self).__init__()
        self.add = win
        self.a = 0
        self.files = glob.glob(self.add.fname + r'/*')
        self.filemu = os.path.split(self.add.fname)[1]
        self.answer = []
        self.pa = self.files[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.add.imagelab.setPixmap(pixmap)  # 在label上显示图片


    def addfun(self):
        text1 = self.add.answerEdit.text()
        text2 = self.add.analysisEdit.toPlainText()
        if len(text1) == 0:
            QMessageBox.about(self.add, "提示", '您没有填写答案！！')
        elif len(text2) == 0:
            QMessageBox.about(self.add, "提示", '您没有填写答案！！')
        else:
            self.a = self.a + 1
            try:
                self.pa = self.files[self.a]
                self.answer.append([self.filename, text1, text2])
                self.filename = os.path.split(self.pa)[1]
                b = 0
                for answer in self.answer:
                    if answer[0] == self.filename:
                        self.add.answerEdit.setText(answer[1])
                        self.add.analysisEdit.setText(answer[2])
                        self.answer.remove(answer)
                        b = 1
                        break
                if b == 0:
                    self.add.answerEdit.setText("")
                    self.add.analysisEdit.setText("")
                pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
                self.add.imagelab.setPixmap(pixmap)  # 在label上显示图片
                self.add.imagelab.setScaledContents(True)  # 让图片自适应label大小
            except:
                self.a = self.a - 1
                QMessageBox.about(self.add, "提示", '这是最后一题了!!')

    def cutfun(self):
        text1 = self.add.answerEdit.text()
        text2 = self.add.analysisEdit.toPlainText()
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            QMessageBox.about(self.add, "提示", '这是第一题了!!')
        else:
            self.answer.append([self.filename, text1, text2])
            self.pa = self.files[self.a]
            self.filename = os.path.split(self.pa)[1]
            for answer in self.answer:
                if answer[0] == self.filename:
                    self.add.answerEdit.setText(answer[1])
                    self.add.analysisEdit.setText(answer[2])
                    self.answer.remove(answer)
                    break
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.add.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.add.imagelab.setScaledContents(True)  # 让图片自适应label大小

    def surefun(self):
        a = self.a + 1
        try:
            pa = self.files[a]
            QMessageBox.about(self.add, "提示", '请您把所有题目设置答案后才可以保存！！')
        except:
            text1 = self.add.answerEdit.text()
            text2 = self.add.analysisEdit.toPlainText()
            if len(text1) == 0:
                QMessageBox.about(self.add, "提示", '您没有填写答案！！')
            elif len(text2) == 0:
                QMessageBox.about(self.add, "提示", '您没有填写答案！！')
            else:
                self.answer.append([self.filename, text1, text2])
                self.file_to_zip(self.add.fname)
                filepath = './datas/tupian' + '.zip'
                with open(filepath, "rb") as f:
                    total = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                filename1 = '.zip'
                sqlpath = "./datas/database/ControllerSQ" + \
                          str(ManageOperation.number) + "L.db"
                conn = sqlite3.connect(sqlpath)
                c = conn.cursor()
                c.execute("select * from Filename2")
                no = len(c.fetchall())
                ab = []
                for da in self.answer:
                    str5 = "#".join(da)
                    ab.append(str5)
                str5 = "@".join(ab)
                print(str5)
                c.execute("insert into Filename2 VALUES(?,?,?,?,?,?)",
                          ('C' + str(no), self.add.data[0], self.add.data[1],
                           self.filemu, str5, filename1,))
                c.execute("insert into Filedate2 values(?,?)",
                          ('C' + str(no), total))
                conn.commit()
                c.close()
                conn.close()
                self.add.close()

    def conclefun(self):
        self.add.close()

    def file_to_zip(self, path):  # 将文件夹压缩为压缩包。
        filepath = './datas/tupian' + '.zip'
        if os.path.exists(filepath):
            os.remove(filepath)
        z = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
