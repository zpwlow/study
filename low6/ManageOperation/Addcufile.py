from PyQt5.QtWidgets import QHBoxLayout,QMessageBox,QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QImage
import ManageOperation
from ManageOperation import Course_news,Add_System
from ManageInterface.Addcufile_win import Addcufile_win
import subprocess,os,fitz,glob,base64,re,sqlite3,zipfile



class Addcufile(QFrame):
    def __init__(self,data):
        super(Addcufile, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.addcufile = Addcufile_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.addcufile)

        self.data = data
        self.addcufile.returnbut.clicked.connect(self.returnfun)
        self.addcufile.addfile.clicked.connect(self.select_fun1)
        self.addcufile.addmufile.clicked.connect(self.select_fun2)
        self.addcufile.addsystem.clicked.connect(self.select_fun3)

    def returnfun(self):
        dow = Course_news.Course_news(self.data)
        #dow.changfun()
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0,dow)

    def select_fun1(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'ppt(*.ppt *.pptx);;)')
        if not path:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')
            return
        end_file = os.path.splitext(path)[1]
        file = os.path.split(path)[1][:-len(end_file)]
        file1 = './datas/tupian'
        fileNames = glob.glob(file1 + r'/*')
        if fileNames:
            for fileName in fileNames:
                os.remove(fileName)# 将pa 文件夹中的文件删除。
        if end_file == '.ppt' or end_file == '.pptx':
            self.ppt_to_pdf("./datas/wen/", path)
            pdf_path = "./datas/wen/" + file + '.pdf'
            self.pdf_to_image(pdf_path, file1)
            os.remove(pdf_path)
            self.file_to_zip(file1)
            zip_file = file1 + '.zip'
            with open(zip_file, "rb") as f:
                total = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            with open(file1 + '/image' + '1.jpg', "rb") as f:
                total2 = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            self.save_date(self.data, file, total, total2, '.zip', '.jpg')
            QMessageBox.about(self,"提示",'添加文件成功!!')
        else:
            QMessageBox.about(self, "提示", '添加文件失败!!')




    def select_fun2(self):
        fname = QFileDialog.getExistingDirectory(self, 'open file', '/')
        if fname:
            files = glob.glob(fname + r'/*')
            if files:
                for path in files:
                    end_file = os.path.splitext(path)[1]
                    file = os.path.split(path)[1][:-len(end_file)]
                    file1 = './datas/tupian'
                    fileNames = glob.glob(file1 + r'/*')
                    if fileNames:
                        for fileName in fileNames:
                            # 将pa 文件夹中的文件删除。
                            os.remove(fileName)
                    if end_file == '.ppt' or end_file == '.pptx':
                        self.ppt_to_pdf("./datas/wen/", path)
                        pdf_path = "./datas/wen/" + file + '.pdf'
                        self.pdf_to_image(pdf_path, file1)
                        os.remove(pdf_path)
                        self.file_to_zip(file1)
                        zip_file = file1 + '.zip'
                        with open(zip_file, "rb") as f:
                            total = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        with open(file1 + '/image' + '1.jpg', "rb") as f:
                            total2 = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        self.save_date(self.data, file, total, total2, '.zip', '.jpg')
                QMessageBox.about(self, "提示", '添加文件成功!!')
            else:
                QMessageBox.about(self, "提示", '该目录没有任何文件!!')
        else:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')

    def select_fun3(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0,Add_System.Add_System(self.data) )


    def save_date(self,data,file,total,total2,filename1,filename2):
        sqlpath = "./datas/database/ControllerSQ" + str(ManageOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Filename")
        no = len(c.fetchall())
        c.execute("insert into Filename VALUES(?,?,?,?,?,?)",
                  ('C'+str(no),data[0],data[1],file,filename1,filename2))
        c.execute("insert into Fileimage values(?,?)",('C'+str(no),total2))
        c.execute("insert into Filedate values(?,?)",('C'+str(no),total))
        conn.commit()
        c.close()
        conn.close()

    def pdf_to_image(self, pdf_path, file1):
        pdf = fitz.open(pdf_path)
        for pg in range(pdf.pageCount):
            page = pdf.loadPage(pg)  # 使用循环将所有转换为图片。
            pagePixmap = page.getPixmap()
            # 获取 image 格式
            imageFormat = QImage.Format_RGB888
            # 生成 QImage 对象
            pageQImage = QImage(pagePixmap.samples, pagePixmap.width,
                                pagePixmap.height, pagePixmap.stride,imageFormat)
            pageQImage.save(file1 + '/image' + '%s.jpg' % (pg + 1))
        pdf.close()

    def ppt_to_pdf(self, outfile, infile, timeout=None):
        """将ppt 转换为pdf
        函数说明:将路径为infile的ppt文件转换为pdf,保存进路径为outfile的pdf文件.
        参数: outfile(str):保存文件pdf 的路径.
        参数: infile(str):ppt文件的路径.
        参数: timeout:转换文件时的时间延迟.
        """
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', outfile, infile]
        process = subprocess.run(args, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=timeout)
        re.search('-> (.*?) using filter', process.stdout.decode())

    def word_to_pdf(self, outfile, infile, timeout=None):
        """将ppt 转换为pdf
        函数说明:将路径为infile的ppt文件转换为pdf,保存进路径为outfile的pdf文件.
        参数: outfile(str):保存文件pdf 的路径.
        参数: infile(str):ppt文件的路径.
        参数: timeout:转换文件时的时间延迟.
        """
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', outfile, infile]
        process = subprocess.run(args, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=timeout)
        re.search('-> (.*?) using filter', process.stdout.decode())

    def file_to_zip(self, path):  # 将文件夹压缩为压缩包。
        filepath = path + '.zip'
        if os.path.exists(filepath):
            os.remove(filepath)
        z = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()