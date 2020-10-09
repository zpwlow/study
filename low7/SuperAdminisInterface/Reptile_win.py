from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QTextEdit, QHBoxLayout, QMessageBox, QFrame
from PyQt5.QtWidgets import QComboBox,QLabel,QApplication
from PyQt5 import QtCore
from PyQt5 import QtGui
import os,  time, re
import glob
import random
import base64
from bs4 import BeautifulSoup
import fitz
import sqlite3
import requests
import zipfile
import shutil
import subprocess

from SuperAdminisOperation import Reptile


class Reptile_win(QFrame):
    def __init__(self):
        super(Reptile_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.datawindow = Reptile.Reptile(self)
        self.Reptile_child1but1 = QPushButton("返回")
        self.Reptile_child1but2 = QPushButton("开始")
        self.Reptile_child1but3 = QPushButton("暂停")
        self.Reptile_child1but4 = QPushButton("重新选择")
        self.window1tree = QTextEdit()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.Lchild_win1 = QWidget()  # 左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)  # 设置左侧部件布局为网格
        self.Rchild_win1 = QWidget()  # 右侧控件布局
        self.win_layout2 = QGridLayout()  # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)  # 设置右侧部件布局为网格

        self.layout.addWidget(self.Lchild_win1, 0, 0, 20, 2)  # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1, 0, 2, 20, 20)  # 右侧部件在第1行第3列，占20行20列
        self.Reptile_child1but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:34px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")

        self.Reptile_child1but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:34px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.Reptile_child1but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:34px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.Reptile_child1but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:34px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.Reptile_child1but1.setEnabled(False)
        self.Reptile_child1but2.setEnabled(False)
        self.Reptile_child1but3.setEnabled(False)
        self.Reptile_child1but4.setEnabled(False)
        self.win_layout1.addWidget(self.Reptile_child1but1, 1, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but2, 2, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but3, 3, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but4, 4, 0, 1, 2)
        self.win_layout2.addWidget(self.window1tree, 0, 0, 20, 20)



class RepliteJob(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    def __init__(self,dow):
        super(RepliteJob, self).__init__()
        self.dow = dow
        self.type = ''
        self.greade = ''
        self.course = ''
        self.sign = 1

    def setdata(self,type,greade,course):
        self.type = type
        self.greade = greade
        self.course = course

    def run(self):
        if self.type == "课件":
            if self.greade == "小学":
                if self.course == "数学":
                    self.updated.emit("小学数学 \n\n数据爬取如下:")
                    self.htmls = []
                    url = "http://old.pep.com.cn/xxsx/jszx/tbjxzy/xsjxkj/"
                    self.htmls = Reptile_data().crawling_url(url, 1)
                    if (len(self.htmls) != 0):
                        self.updated.emit("爬取网址成功！！！\n")
                    else:
                        self.updated.emit("爬取网址失败！！！\n")
                    self.htmls = list(set(self.htmls))  # 去重复元素
                    x=1
                    for html in self.htmls:
                        if self.sign == 1:
                            if Reptile_data().check_url(html):
                                self.updated.emit("第 " + str(x) + " 次")
                                data = Reptile_data().crawling_data('小学', '数学', 4, 64, html)
                                self.updated.emit(data)
                                x = x + 1
                                time.sleep(1)
                        else:
                            break
                elif self.course == "语文":
                    self.updated.emit("小学语文 \n\n数据爬取如下:")
                    self.htmls = []
                    urls = ["http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj1/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj2/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj3/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj4/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj5/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj6/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj7/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj8/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj9/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj10/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj11/",
                            "http://old.pep.com.cn/xiaoyu/jiaoshi/tbjx/sheji_1/kj12/"]
                    for url in urls:
                        data = Reptile_data().crawling_url(url, 0)
                        if (len(data) != 0):
                            for da in data:
                                self.htmls.append(da)
                            self.updated.emit("爬取网址成功！！！\n")
                        else:
                            self.updated.emit("爬取网址失败！！！\n")
                    self.htmls = list(set(self.htmls))  # 去重复元素
                    x=1
                    for html in self.htmls:
                        if self.sign == 1:
                            if Reptile_data().check_url(html):
                                self.updated.emit("第 " + str(x) + " 次")
                                data = Reptile_data().crawling_data('小学', '语文', 5, 64, html)
                                self.updated.emit(data)
                                x = x + 1
                                time.sleep(1)
                        else:
                            break
                elif self.course == "英语":
                    self.updated.emit("小学英语 \n\n数据爬取如下:")
                    self.htmls = []
                    url = "http://old.pep.com.cn/xe/jszx/tbjxzy/kjsc/PEPkjsc/"
                    self.htmls = Reptile_data().crawling_url(url, 0)
                    if (len(self.htmls) != 0):
                        self.updated.emit("爬取网址成功！！！\n")
                    else:
                        self.updated.emit("爬取网址失败！！！\n")
                    self.htmls = list(set(self.htmls))  # 去重复元素
                    x=1
                    for html in self.htmls:
                        if self.sign == 1:
                            if Reptile_data().check_url(html):
                                self.updated.emit("第 " + str(x) + " 次")
                                data = Reptile_data().crawling_data('小学', '英语', 6, 67, html)
                                self.updated.emit(data)
                                x = x + 1
                                time.sleep(1)
                        else:
                            break
            else:
                QMessageBox.about(self.dow, "抱歉", '其他的数据爬去功能暂时还未完成!!')
        else:
            QMessageBox.about(self.dow, "抱歉", '其他的数据爬去功能暂时还未完成!!')


    def stop(self):
        self.sign = 0

class Reptile_data():
    def __init__(self):
        super(Reptile_data, self).__init__()

    def get_agent(self):  # 模拟浏览器
        '''
        模拟header的user-agent字段，
        返回一个随机的user-agent字典类型的键值对
        '''
        agents = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
                  'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
        fakeheader = {}
        fakeheader['User-agent'] = agents[random.randint(0, len(agents) - 1)]
        return fakeheader

    def check_url(self, url):  # 检查网页是否已经爬取过
        r = requests.get(url, headers=self.get_agent())
        r = r.text
        data = len(r)
        sqlpath = "./datas/database/Data.db"
        conn = sqlite3.connect(sqlpath)
        d = conn.cursor()
        d.execute("select * from successfulurl")
        for variate in d.fetchall():
            if variate[0] == url and variate[1] == data:
                return False
        d.close()
        conn.close()
        return True

    def crawling_url(self, url, sign):  # 爬取网页网址
        for j in range(0, 10):  # 使用循环，避免爬取网址时出错，无法进行下面的爬取。
            try:
                content = requests.get(url, timeout=10, headers=self.get_agent())
                content.encoding = content.apparent_encoding
                soup = BeautifulSoup(content.text, 'lxml')
                soups = soup.find_all('div', attrs={'class': 'clear'})
                self.htmls = []
                for soup in soups:
                    datas = soup.find_all('a')
                    for data in datas:
                        # 对于一些网址可以这样处理，将多余的字符从网址中出去。
                        data = data['href'].replace('\n', '').replace('.../', '').replace('../', '').replace('./', '')
                        if sign:
                            data = url[:-7] + data
                        else:
                            data = url + data
                        self.htmls.append(data)

                return self.htmls
            except:
                pass

    def crawling_url2(self, url, sign):  # 爬取网页网址
        for j in range(0, 10):  # 使用循环，避免爬取网址时出错，无法进行下面的爬取。
            try:
                content = requests.get(url, timeout=10, headers=self.get_agent())
                content.encoding = content.apparent_encoding
                soup = BeautifulSoup(content.text, 'lxml')
                soups = soup.find_all('div', attrs={'class': 'ttlist'})
                self.htmls = []
                for soup in soups:
                    datas = soup.find_all('a')
                    for data in datas:
                        # 对于一些网址可以这样处理，将多余的字符从网址中出去。
                        data = data['href'].replace('.../', '').replace('../', '').replace('./', '')
                        if sign:
                            data = url[:-9] + data
                        else:
                            data = url + data
                        self.htmls.append(data)
                return self.htmls
            except:
                pass

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

    def zip_to_files(self, zippath):
        # 将压缩包解压
        path = zippath[:-4]
        if (os.path.isdir(path)):
            # 判断文件夹是否存在
            fileNames = glob.glob(path + r'/*')
            if fileNames:
                for fileName in fileNames:
                    # 将pa 文件夹中的文件删除。
                    os.remove(fileName)
        else:
            os.mkdir(path)
        zf = zipfile.ZipFile(zippath)
        for fn in zf.namelist():
            # 循环压缩包中的文件并保存进新文件夹。
            right_fn = fn.encode('cp437').decode('gbk')  # 将文件名正确编码
            right_fn = right_fn.replace('\\\\', '_').replace('\\', '_').replace('//', '_').replace('/', '_')  # 将文件名正确编码
            right_fn = path + '/' + right_fn
            with open(right_fn, 'wb') as output_file:
                # 创建并打开新文件
                with zf.open(fn, 'r') as origin_file:
                    # 打开原文件
                    shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
        zf.close()
        os.remove(zippath)

    def pdf_to_image(self, pdf_path, file1):
        fileNames = glob.glob(file1 + r'/*')
        if fileNames:
            for fileName in fileNames:
                # 将pa 文件夹中的文件删除。
                os.remove(fileName)
        pdf = fitz.open(pdf_path)
        x=1
        for pg in range(pdf.pageCount):
            page = pdf.loadPage(pg)  # 使用循环将所有转换为图片。
            pagePixmap = page.getPixmap()
            # 获取 image 格式
            imageFormat = QtGui.QImage.Format_RGB888
            # 生成 QImage 对象
            pageQImage = QtGui.QImage(pagePixmap.samples, pagePixmap.width, pagePixmap.height, pagePixmap.stride,
                                      imageFormat)
            pageQImage.save(file1 + '/image' +str(x)+ '.jpg')
            x=x+1
        pdf.close()

    def ppt_to_pdf(self, outfile, infile, timeout=None):
        """将ppt 转换为pdf
        函数说明:将路径为infile的ppt文件转换为pdf,保存进路径为outfile的pdf文件.
        参数: outfile(str):保存文件pdf 的路径.
        参数: infile(str):ppt文件的路径.
        参数: timeout:转换文件时的时间延迟.
        """
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', outfile, infile]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        re.search('-> (.*?) using filter', process.stdout.decode())

    def word_to_pdf(self, outfile, infile, timeout=None):
        """将word 转换为pdf
        函数说明:将路径为infile的word文件转换为pdf,保存进路径为outfile的pdf文件.
        参数: outfile(str):保存文件pdf 的路径.
        参数: infile(str):word文件的路径.
        参数: timeout:转换文件时的时间延迟.
        """
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', outfile, infile]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        re.search('-> (.*?) using filter', process.stdout.decode())

    # 爬取课件数据
    def crawling_data(self, file1, file3, a, b, url):
        # a 代表爬取文件名的位置，b代表组成网址时需要减少的字符串长度
        try:
            r = requests.get(url, timeout=10, headers=self.get_agent())
            data = len(r.text)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'lxml')
            da = soup.find_all('a', target="_self")
            file2 = da[a].text
            title = soup.find('title').text.replace('\n', '').replace('/', '_')
            try:
                soup1 = soup.find('div', id="downloadcontent")
                url2 = soup1.find('a').get('href').replace('.../', '').replace('../', '').replace('./', '')
                url2 = url[0:b] + url2
            except:
                soup1 = soup.find('div', id="doccontent")
                url2 = soup1.find('A').get('href')
            filename = url2[-4:]
            file = './datas/wen/xinwen' + filename
            d = requests.get(url2, timeout=10, headers=self.get_agent())
            with open(file, 'wb')as f:
                # 将网上的文件下载保存进电脑。
                for chunk in d.iter_content(chunk_size=100):
                    f.write(chunk)
            f.close()
            if filename == ".ppt":
                pa = "./datas/tupian"  # 保存图片的路径
                self.ppt_to_pdf("./datas/wen/", file)  # 将ppt转换为图片。
                pdf_path = r"./datas/wen/xinwen.pdf"
                self.pdf_to_image(pdf_path, pa)
                os.remove(pdf_path)
                self.file_to_zip(pa)  # 将文件夹压缩为压缩包。
                filen = pa + ".zip"  # 压缩包的路径
                with open(filen, "rb") as f:
                    total = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                time.sleep(2)
                filen = r"./datas/tupian/image1.jpg"
                with open(filen, "rb") as f:
                    total2 = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                filename1 = '.zip'
                self.savedata(file1, file2, file3, title, total, total2, filename1, ".jpg")
            elif filename == '.zip':
                self.zip_to_files(file)  # 将压缩包解压。
                pa1 = r'./datas/wen/xinwen'  # 解压后的文件名
                fileNames = glob.glob(pa1 + r'/*')  # 读取解压文件夹里的文件。
                for fileName in fileNames:
                    end_file = os.path.splitext(fileName)[1]
                    filena = os.path.split(fileName)[1][:-len(end_file)]
                    if end_file == '.ppt' or end_file == '.pptx':
                        pa = r"./datas/tupian"  # 保存图片的路径
                        self.ppt_to_pdf("./datas/wen/", fileName)  # 将ppt转换为图片。
                        pdf_path = "./datas/wen/" + filena + '.pdf'
                        self.pdf_to_image(pdf_path, pa)
                        os.remove(pdf_path)
                        self.file_to_zip(pa)  # 将文件夹压缩为压缩包。
                        filen = pa + ".zip"  # 压缩包的路径
                        with open(filen, "rb") as f:
                            total = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        time.sleep(2)
                        filen = r"./datas/tupian/image1.jpg"
                        with open(filen, "rb") as f:
                            total2 = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        filename1 = ".zip"
                        self.savedata(file1, file2, file3, title, total, total2, filename1, ".jpg")
                        break
            sqlpath = "./datas/database/Data.db"
            conn = sqlite3.connect(sqlpath)
            conn.execute("insert into successfulurl(url,howbyte)values(?,?)", (url, data))
            conn.commit()
            conn.close()
            return (title + "\n爬取成功\n")
        except:
            return ("爬取错误\n")

    def savedata(self,file1,file2,file3,title,total,total2,filename1,filename2):
        sqlpath = "./datas/database/Data.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        if file2[:3]=="一年级":
            c.execute("select * from First_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO First_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3,title, filename1))
            conn.execute("insert into First_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into First_Grade_image values(?,?,?)", ("S" + str(no + 1), total2,filename2))
        elif file2[:3]=="二年级":
            c.execute("select * from Second_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO Second_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3, title, filename1))
            conn.execute("insert into Second_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into Second_Grade_image values(?,?,?)", ("S" + str(no + 1), total2, filename2))
        elif file2[:3]=="三年级":
            c.execute("select * from Three_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO Three_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3, title, filename1))
            conn.execute("insert into Three_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into Three_Grade_image values(?,?,?)", ("S" + str(no + 1), total2, filename2))
        elif file2[:3]=="四年级":
            c.execute("select * from Fourth_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO Fourth_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3, title, filename1))
            conn.execute("insert into Fourth_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into Fourth_Grade_image values(?,?,?)", ("S" + str(no + 1), total2, filename2))
        elif file2[:3]=="五年级":
            c.execute("select * from Fifth_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO Fifth_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3, title, filename1))
            conn.execute("insert into Fifth_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into Fifth_Grade_image values(?,?,?)", ("S" + str(no + 1), total2, filename2))
        elif file2[:3]=="五年级":
            c.execute("select * from Six_Grade")
            no = len(c.fetchall())
            conn.execute("INSERT INTO Six_Grade VALUES(?,?,?,?,?,?)",
                         ("S" + str(no + 1), file1, file2, file3, title, filename1))
            conn.execute("insert into Six_Grade_data values(?,?)", ("S" + str(no + 1), total))
            conn.execute("insert into Six_Grade_image values(?,?,?)", ("S" + str(no + 1), total2, filename2))
        conn.commit()
        c.close()
        conn.close()


class Select_Reptile(QWidget):
    def __init__(self,dow):
        super(Select_Reptile, self).__init__()
        self.dow = dow
        self.setWindowTitle("选择爬取的内容")
        self.lab = QLabel("请选择爬取的内容！！！！")
        self.typelab = QLabel("文件类型")
        self.typebox = QComboBox()
        self.greadelab = QLabel("年级")
        self.greadebox = QComboBox()
        self.courselab = QLabel("科目")
        self.coursebox = QComboBox()
        self.sure = QPushButton("确定")
        self.concle = QPushButton("取消")
        self.devise_ui()

    def devise_ui(self):
        self.resize(750, 400)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作

        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.lab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.typelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.greadelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.concle.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.lab.setMaximumSize(400,80)
        self.typelab.setMaximumSize(80,50)
        self.greadelab.setMaximumSize(80,50)
        self.courselab.setMaximumSize(80,50)
        self.typebox.setMaximumSize(160, 50)
        self.greadebox.setMaximumSize(160, 50)
        self.coursebox.setMaximumSize(160, 50)
        self.sure.setMaximumSize(80,40)
        self.concle.setMaximumSize(80,40)
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.typebox.addItems(['','课件','练习'])
        self.greadebox.addItems(['','小学','初中','高中'])
        self.greadebox.currentIndexChanged.connect(self.fun1)
        self.sure.clicked.connect(self.surefun)
        self.concle.clicked.connect(self.conclefun)
        self.layout.addWidget(self.lab,0,2,1,6)
        self.layout.addWidget(self.typelab,1,0,1,1)
        self.layout.addWidget(self.typebox,1,1,1,2)
        self.layout.addWidget(self.greadelab,1,3,1,1)
        self.layout.addWidget(self.greadebox,1,4,1,2)
        self.layout.addWidget(self.courselab,1,6,1,1)
        self.layout.addWidget(self.coursebox,1,7,1,2)
        self.layout.addWidget(self.sure,2,7,1,1)
        self.layout.addWidget(self.concle,2,8,1,1)

    def fun1(self):
        self.coursebox.clear()
        if self.greadebox.currentText()=="小学":
            self.coursebox.addItems(['','语文','数学','英语'])
        elif self.greadebox.currentText()=="初中":
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])
        elif self.greadebox.currentText()=="高中":
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])

    def fun2(self):
        self.greadebox.clear()
        self.coursebox.clear()
        self.typebox.clear()
        self.typebox.addItems(['', '课件', '练习'])
        self.greadebox.addItems(['', '小学', '初中', '高中'])

    def surefun(self):
        if(self.greadebox.currentText()==""):
            QMessageBox.about(self, "提示", '年级的选项框不能为空!!')
        elif (self.greadebox.currentText()!="小学"):
            QMessageBox.about(self, "提示", '目前只能爬去小学的内容，后续版本会更新该功能!!')
        elif(self.typebox.currentText()==""):
            QMessageBox.about(self, "提示", '学习阶段的选项框不能为空!!')
        elif (self.typebox.currentText()!="课件"):
            QMessageBox.about(self, "提示", '目前只能爬去课件，后续版本会更新该功能!!')
        elif (self.coursebox.currentText()==""):
            QMessageBox.about(self, "提示", '科目的选项框不能为空!!')
        self.close()
        self.dow.clicked1()

    def conclefun(self):
        self.close()
        self.dow.clicked2()

    def gettype(self):
        return self.typebox.currentText()

    def getgrade(self):
        return self.greadebox.currentText()

    def getcourse(self):
        return self.coursebox.currentText()