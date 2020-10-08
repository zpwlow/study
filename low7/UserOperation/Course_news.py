from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

from UserInterface import My_Course_win, Max_widget_win, Practice_widget_win
from UserInterface.Course_news_win import Course_news_win, CuFileQlist, CourseexQlist
from UserOperation import self_cap, self_CAM_NUM
import cv2, sqlite3, os, base64, glob, zipfile, shutil
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import My_Course, Practice_widget, Max_widget


class Course_news:
    def __init__(self, win):
        super(Course_news, self).__init__()
        self.window = win
        self.sign1 = '课件'
        self.sign = 0
        sqlpath = "./datas/database/ControllerSQ" + str(self.window.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                                  Filename,Fileimage where Filename.no = Fileimage.no \
                                   and Cno=(?) ", (self.window.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, self.window.data[2] + " 课件")

    # 识别手指指的操作命令
    def finger_camera(self, image):
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 45 < x < 125 and 60 < y < 130:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" +
                                                   "本次操作为：返回\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, My_Course_win.My_Course_win())

                elif 45 < x < 125 and 190 < y < 260:
                    # 上一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" +
                                                   "本次操作为：上一页\n\t操作成功！！")
                    self.cut_images()
                elif 170 < x < 250 and 190 < y < 260:
                    # 下一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" +
                                                   "本次操作为：下一页\n\t操作成功！！")
                    self.add_images()
                if self.sign1 == "课件":
                    if 170 < x < 250 and 60 < y < 130:
                        # 练习
                        self.window.timer_next.stop()
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：练习\n\t操作成功！！")
                        self.changexfun()
                    elif 45 < x < 125 and 320 < y < 390:
                        # 课件一
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：课件一\n\t操作成功！！")
                        self.clear_cap()
                        self.openfile(0)
                    elif 170 < x < 250 and 320 < y < 390:
                        # 课件二
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：课件二\n\t操作成功！！")
                        sign = self.sign + 2
                        n = len(self.datas)
                        if n > sign:
                            self.clear_cap()
                            self.openfile(1)
                        else:
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "本页没有课件二\n\t请您换一个操作！！")
                    elif 295 < x < 375 and 320 < y < 390:
                        # 课件三
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：课件三\n\t操作成功！！")
                        sign = self.sign + 3
                        n = len(self.datas)
                        if n > sign:
                            self.clear_cap()
                            self.openfile(2)
                        else:
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "本页没有课件三\n\t请您换一个操作！！")
                elif self.sign1 == "练习":
                    if 170 < x < 250 and 60 < y < 130:
                        # 课件
                        self.window.timer_next.stop()
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：课件\n\t操作成功！！")
                        self.changexfun2()
                    elif 45 < x < 125 and 320 < y < 390:
                        # 练习一
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：练习一\n\t操作成功！！")
                        self.clear_cap()
                        self.openfile2(0)
                    elif 170 < x < 250 and 320 < y < 390:
                        # 练习二
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：练习二\n\t操作成功！！")
                        sign = self.sign + 2
                        n = len(self.datas)
                        if n > sign:
                            self.clear_cap()
                            self.openfile2(1)
                        else:
                            self.window.messagelab.setText("提示!\n\t" +
                                                           "本页没有练习二\n\t请您换一个操作！！")
                    elif 295 < x < 375 and 320 < y < 390:
                        # 练习三
                        self.window.messagelab.setText("提示!\n\t" +
                                                       "本次操作为：练习三\n\t操作成功！！")
                        sign = self.sign + 3
                        n = len(self.datas)
                        if n > sign:
                            self.clear_cap()
                            self.openfile2(2)
                        else:
                            self.window.messagelab.setText("提示!\n\t"
                                                           + "本页没有练习三\n\t请您换一个操作！！")

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()

    # 下一页
    def add_images(self):
        self.sign = self.sign + 3
        n = len(self.datas)
        if n > self.sign:
            self.window.qtool.removeItem(0)
            self.window1 = CuFileQlist(self.datas, self.sign)
            self.window.qtool.addItem(self.window1, self.window.data[2] + " 课件")
        else:
            self.sign = self.sign - 3
            self.window.messagelab.setText("抱歉!\n\t" + "这是最后一页了")
        self.window.timer_next.start(200)

    # 上一页
    def cut_images(self):
        self.sign = self.sign - 3
        print(self.sign)
        if self.sign < 0:
            self.sign = 0
        self.window.qtool.removeItem(0)
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, self.window.data[2] + " 课件")
        self.window.timer_next.start(200)

    # 点击练习时换界面按钮
    def changexfun(self):
        self.window.newlab.data[1][4].setText("课件")
        self.window.newlab.data[4][4].setText("练习一")
        self.window.newlab.data[5][4].setText("练习二")
        self.window.newlab.data[6][4].setText("练习三")
        self.sign = 0
        self.sign1 = "练习"
        sqlpath = "./datas/database/ControllerSQ" + str(self.window.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select no,name from Filename2 where Cno=(?) ", (self.window.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window.qtool.removeItem(0)
        self.window1 = CourseexQlist(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, self.window.data[2] + " 　练习")
        self.window.timer_next.start(200)

    # 点击课件时换界面按钮
    def changexfun2(self):
        self.window.newlab.data[1][4].setText("练习")
        self.window.newlab.data[4][4].setText("课件一")
        self.window.newlab.data[5][4].setText("课件二")
        self.window.newlab.data[6][4].setText("课件三")
        self.sign = 0
        self.sign1 = "课件"
        sqlpath = "./datas/database/ControllerSQ" + str(self.window.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                                  Filename,Fileimage where Filename.no = Fileimage.no \
                                   and Cno=(?) ", (self.window.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window.qtool.removeItem(0)
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, self.window.data[2] + " 　课件")
        self.window.timer_next.start(200)

    # 显示课件
    def openfile(self, n):
        da = self.datas[self.sign + n][:2]
        sqlpath = "./datas/database/ControllerSQ" + str(self.window.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Cname,name,total,filename1 from \
                               Filename,Filedate where Filename.no= Filedate.no \
                                and Filename.no=(?)", (da[0],))
        filedata = c.fetchall()[0]
        zip_path = './datas/' + filedata[0]
        if not (os.path.exists(zip_path)):  # 创建文件夹。
            os.makedirs(zip_path)
        zip_path = zip_path + '/' + filedata[1] + filedata[3]
        total = base64.b64decode(filedata[2])
        f = open(zip_path, 'wb')
        f.write(total)
        f.close()
        self.zip_to_files(zip_path)
        self.max = Max_widget_win.Max_widget_win(self, self.window.data[0], filedata[0], da[1])
        self.max.show()

    # 显示练习
    def openfile2(self, n):
        da = self.datas[self.sign + n][:2]
        sqlpath = "./datas/database/ControllerSQ" + str(self.window.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Cname,name,answer,total,filename1 from \
                               Filename2,Filedate2 where Filename2.no= Filedate2.no \
                                and Filename2.no=(?)", (da[0],))
        filedata = c.fetchall()[0]
        zip_path = './datas/' + filedata[0]
        if not (os.path.exists(zip_path)):  # 创建文件夹。
            os.makedirs(zip_path)
        zip_path = zip_path + '/' + filedata[1] + filedata[4]
        total = base64.b64decode(filedata[3])
        f = open(zip_path, 'wb')
        f.write(total)
        f.close()
        self.zip_to_files(zip_path)
        self.practice = Practice_widget_win.Practice_widget_win(self, self.window.data[0], filedata[:3], da[1])
        self.practice.show()

    def changetime(self):
        if not self.window.timer_camera.isActive():  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if not flag:  # flag表示open()成不成功
                self.window.course_news.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.window.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.window.timer_next.start(200)

    # 将zip 文件解压
    def zip_to_files(self, zippath):  # 将压缩包解压
        path = './datas/tupian'
        if os.path.isdir(path):  # 判断文件夹是否存在
            fileNames = glob.glob(path + r'/*')
            if fileNames:
                for fileName in fileNames:  # 将pa 文件夹中的文件删除。
                    os.remove(fileName)
        else:
            os.mkdir(path)
        zf = zipfile.ZipFile(zippath)
        for fn in zf.namelist():  # 循环压缩包中的文件并保存进新文件夹。
            # right_fn = fn.replace('\\\\', '_').replace('\\', '_').replace('//', '_').replace('/', '_')  # 将文件名正确编码
            right_fn = fn.encode('cp437').decode('gbk')  # 将文件名正确编码
            right_fn = path + '/' + right_fn
            with open(right_fn, 'wb') as output_file:  # 创建并打开新文件
                with zf.open(fn, 'r') as origin_file:  # 打开原文件
                    shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
        zf.close()
        os.remove(zippath)
