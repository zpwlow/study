from PyQt5.QtWidgets import QHBoxLayout,QFileDialog,QApplication
from PyQt5.QtWidgets import QFrame,QMessageBox,QHBoxLayout
from PyQt5.QtGui import QPixmap
import base64,sqlite3,os,glob
import SuperAdminisOperation
from SuperAdminisOperation import Function
from SuperAdminisInterface.Addfile_win import Addfile_win,Select_location
from SuperAdminisInterface.Reptile_win import Reptile_data



class Addfile(QFrame):
    def __init__(self):
        super(Addfile, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.informent =  Addfile_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.informent)

        self.dow = Select_location(self)
        self.returnbut.clicked.connect(self.returnfun)
        self.addfile.clicked.connect(self.select_fun1)
        self.addmufile.clicked.connect(self.select_fun2)

    def returnfun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Function.Function())

    def select_fun1(self):
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'ppt(*.ppt *.pptx);;word(*.docx *.doc)')
        if not self.path:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')
            return
        self.sign = 1
        self.dow.fun2()
        self.dow.show()


    def clicked(self):
        if self.sign==1:
            self.fun1()
        elif self.sign == 2:
            self.fun2()

    def fun1(self):
        try:
            self.chang_file(self.path)
            QMessageBox.about(self, "提示", '添加文件成功!!')
        except:
            QMessageBox.about(self, "提示", '添加文件失败!!')


    def select_fun2(self):
        fname = QFileDialog.getExistingDirectory(self, 'open file', '/')
        if fname:
            self.files = glob.glob(fname + r'/*')
            if self.files:
                self.sign = 2
                self.dow.fun2()
                self.dow.show()
            else:
                QMessageBox.about(self, "提示", '该目录没有任何文件!!')
        else:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')

    def fun2(self):
        for path in self.files:
            try:
                self.chang_file(path)
            except:
                pass
        QMessageBox.about(self, "提示", '添加文件成功!!')

    def chang_file(self,path):
        end_file = os.path.splitext(path)[1]
        file = os.path.split(path)[1][:-len(end_file)]
        file1 = './datas/tupian'
        fileNames = glob.glob(file1 + r'/*')
        if fileNames:
            for fileName in fileNames:
                # 将pa 文件夹中的文件删除。
                os.remove(fileName)
        if end_file == '.ppt' or end_file == '.pptx':
            Reptile_data().ppt_to_pdf("./datas/wen/", path)
            pdf_path = "./datas/wen/" + file + '.pdf'
            Reptile_data().pdf_to_image(pdf_path, file1)
            os.remove(pdf_path)
            Reptile_data().file_to_zip(file1)
            zip_file = file1 + '.zip'
            with open(zip_file, "rb") as f:
                total = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            with open(file1 + '/image' + '1.jpg', "rb") as f:
                total2 = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            self.save_date(file, total, total2, '.zip', '.jpg')

        elif end_file == '.docx' or end_file == '.doc':
            Reptile_data().word_to_pdf("./datas/wen/", path)
            pdf_path = "./datas/wen/" + file + '.pdf'
            Reptile_data().pdf_to_image(pdf_path, file1)
            os.remove(pdf_path)
            Reptile_data().file_to_zip(file1)
            zip_file = file1 + '.zip'
            with open(zip_file, "rb") as f:
                total = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            with open(file1 + '/image' + '1.jpg', "rb") as f:
                total2 = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            self.save_date(file, total, total2, '.zip', '.jpg')



    def save_date(self,file,total,total2,filename1,filename2):
        type = self.dow.gettype()
        grade = self.dow.getgrade()
        course = self.dow.getcourse()
        sqlpath = "./datas/database/Data.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        if grade[:3]=="一年级":
            c.execute("select * from First_Grade")
            no = len(c.fetchall())
            c.execute("insert into First_Grade VALUES(?,?,?,?,?,?)", ('C' + str(no),type,grade,course,file,filename1,))
            c.execute("insert into First_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into First_Grade_image values(?,?,?)", ('C' + str(no), total2,filename2))
        elif grade[:3]=="二年级":
            c.execute("select * from Second_Grade")
            no = len(c.fetchall())
            c.execute("insert into Second_Grade VALUES(?,?,?,?,?,?)",
                      ('C' + str(no), type, grade, course, file, filename1,))
            c.execute("insert into Second_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into Second_Grade_image values(?,?,?)", ('C' + str(no), total2, filename2))
        elif grade[:3]=="三年级":
            c.execute("select * from Three_Grade")
            no = len(c.fetchall())
            c.execute("insert into Three_Grade VALUES(?,?,?,?,?,?)",
                      ('C' + str(no), type, grade, course, file, filename1,))
            c.execute("insert into Three_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into Three_Grade_image values(?,?,?)", ('C' + str(no), total2, filename2))
        elif grade[:3]=="四年级":
            c.execute("select * from Fourth_Grade")
            no = len(c.fetchall())
            c.execute("insert into Fourth_Grade VALUES(?,?,?,?,?,?)",
                      ('C' + str(no), type, grade, course, file, filename1,))
            c.execute("insert into Fourth_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into Fourth_Grade_image values(?,?,?)", ('C' + str(no), total2, filename2))
        elif grade[:3]=="五年级":
            c.execute("select * from Fifth_Grade")
            no = len(c.fetchall())
            c.execute("insert into Fifth_Grade VALUES(?,?,?,?,?,?)",
                      ('C' + str(no), type, grade, course, file, filename1,))
            c.execute("insert into Fifth_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into Fifth_Grade_image values(?,?,?)", ('C' + str(no), total2, filename2))
        elif grade[:3]=="六年级":
            c.execute("select * from Six_Grade")
            no = len(c.fetchall())
            c.execute("insert into Six_Grade VALUES(?,?,?,?,?,?)",
                      ('C' + str(no), type, grade, course, file, filename1,))
            c.execute("insert into Six_Grade_data values(?,?)", ('C' + str(no), total))
            c.execute("insert into Six_Grade_image values(?,?,?)", ('C' + str(no), total2, filename2))
        else:
            QMessageBox.about(self, "抱歉", "六年级以上的此功能暂未实现！！")
        conn.commit()
        c.close()
        conn.close()