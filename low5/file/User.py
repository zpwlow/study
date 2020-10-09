"""
作者：钟培望
名称：具体人工智能沉浸式学习系统用户端
时间：2020.4.30
"""

from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, time,re
import subprocess
import glob
import base64
import datetime
import cv2
import sqlite3
import zipfile
import shutil
import tr
import difflib

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

self_cap = cv2.VideoCapture()  # 视频流
self_CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头,为１时表示外置摄像头
close_Mouse_key = []

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

def classify_hist_with_split(image1, image2, size=(256, 256)):
    # RGB每个通道的直方图相似度(计算图片相似度)
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

def close_mouse_and_key():
    command = "xinput list "
    back = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    data = back[0].decode()  # 获取终端的消息．
    datas = re.compile('↳(.*?)\[').findall(data)
    for da in datas:
        da  = da.lower()
        if da.find("virtual core xtest keyboard") >= 0:
            pass
        elif da.find('keyboard') >= 0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            close_Mouse_key.append(d[0])
            os.system(text)  # 禁用键盘
        elif da.find('touchpad') >= 0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            print(text)
            #subprocess.Popen(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            os.system(text)
            close_Mouse_key.append(d[0])
            # 禁用触摸屏
        elif  da.find("mouse") >= 0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            close_Mouse_key.append(d[0])
            os.system(text)  # 禁用鼠标
        elif  da.find("wireless device") >= 0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            close_Mouse_key.append(d[0])
            os.system(text)  # 禁用无线连接
        elif da.find("hotkeys")>=0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            close_Mouse_key.append(d[0])
            os.system(text)  # 禁用热键
        elif da.find("usb")>=0:
            d = re.compile('id=(.*?)\t').findall(da)
            text = 'xinput disable ' + d[0]
            close_Mouse_key.append(d[0])
            os.system(text)  # 禁用usb接口

def open_mouse_and_key():
    for sign in close_Mouse_key:
        text = 'xinput enable ' + sign
        os.system(text)  # 启用

class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """
    def __init__(self):   #设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None) # 设置为顶级窗口
        self.setWindowTitle("low_User")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.desktop = QApplication.desktop() #获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.resize(self.x, self.y)
        self.number = '15812904182'
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.splitter.addWidget(Record())
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
        #close_mouse_and_key()

    def closeEvent(self, event):
        #open_mouse_and_key()
        # 清理一些 自己需要关闭的东西
        event.accept()  # 界面的关闭,但是会有一些时候退出不完全,需要调用 os 的_exit 完全退出
        try:
            os._exit(5)
        except:
            pass


class Logon(QFrame):
    def __init__(self):
        super(Logon, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sign = 1
        self.number = ''
        self.passw = ''
        self.data = []
        self.data1 = []
        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，对题目进行识别．
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.but1 = QPushButton("返回")
        self.but2  = QPushButton("确定")
        self.but3 = QPushButton("上一步")
        self.but4 = QPushButton("注册")
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel("输入区")  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.number = ''
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        # 设置QLabel 的字体颜色，大小，
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{background-color:rgb(230,230, 230)}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLine.setPlaceholderText("请在输入区输入手机号码(一次输入不能超过四位数)")
        self.usrnameLine.setPlaceholderText("请在输入区输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请在输入区输入密码(一次输入不能超过四位数)")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.but1,0,1,2,2)
        self.layout.addWidget(self.but2,0,4,1,2)
        self.layout.addWidget(self.but3,2,1,1,2)
        self.layout.addWidget(self.but4,2,4,1,2)
        self.layout.addWidget(self.messagelab, 0, 11, 4, 10)
        self.layout.addWidget(self.progresslab, 4, 1, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 2, 1, 4)
        self.layout.addWidget(self.newlab, 5, 0, 10, 10)
        self.layout.addWidget(self.usr, 5, 10, 1, 1)
        self.layout.addWidget(self.usrLine, 5, 11, 1, 12)
        self.layout.addWidget(self.usrname, 8, 10, 1, 1)
        self.layout.addWidget(self.usrnameLine, 8, 11, 1, 12)
        self.layout.addWidget(self.password1, 11, 10, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 11, 11, 1, 12)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                time.sleep(2)
                self.equal = 0
                self.timer_next.start(3500)

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer_right(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if len(self.number) < 11:
                if data[1] > 0.6:
                    try:
                        da = data[0].replace('I','1').replace('l','1').replace('b','6').replace('q','9')
                    except:
                        da  = data[0]
                    self.data.append(self.number)
                    self.number = self.number + da
                    self.usrLine.setText(self.number)
                    self.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t" +
                                            "如果输入错误请您在操作区输入＇上一步＇操作！！")
            if len(self.number) != 11:
                pass
            elif (self.checking1()):
                self.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n请您先登录！")
            else:
                self.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入昵称\n\t" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            self.usrnameLine.setText(data[0])
            self.messagelab.setText("提示!\n\t" + "用户名输入成功！请您输入密码(每次输入的数字不能超过四位数)\n\t" +
                                    "如果输入错误请您在操作区输入＇上一步＇操作！！")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.pwdLineEdit1.setText(self.passw)
                self.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()



    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal =1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.getanswer()
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "确定").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "上一步").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "注册").quick_ratio()
                    if (num > num1 and num > num2 and num > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                        self.change_record()
                    elif (num1 > num and num1 > num2 and num1 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num and num2 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                        sign = self.sign
                        if sign == 1:
                            if len(self.data)>0:
                                self.number = self.data[-1]
                                self.usrLine.setText(self.number)
                                self.data = self.data[:-1]
                            else:
                                self.number = ''
                                self.usrLine.setText(self.number)
                                self.data = []
                            self.messagelab.setText("提示!\n\t" +
                                                    "请您把账号分段输入，再输入确定！！")
                        elif sign == 2:
                            self.number = self.data[-1]
                            self.usrLine.setText(self.number)
                            self.data = self.data[:-1]
                            self.sign = 1
                            self.messagelab.setText("提示!\n\t" +
                                                    "请您把账号分段输入，再输入确定！！")
                        elif sign == 3:
                            if len(self.data1)>0:
                                self.passw = self.data1[-1]
                                self.pwdLineEdit1.setText(self.passw)
                                self.data1 = self.data1[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                 "请您把密码输入后，再输入确定！！")
                            else:
                                self.passw = ''
                                self.pwdLineEdit1.setText(self.passw)
                                self.data1 = []
                                self.usrnameLine.setText("")
                                self.sign = 2
                                self.messagelab.setText("提示!\n\t" +
                                                "请您把用户名输入后，再输入确定！！")
                    elif (num3 > num1 and num3 > num and num3 > num2):
                        self.messagelab.setText("提示!\n" + "本次操作为：注册\n操作成功")
                        self.accept()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t本页面没有该操作，请您重新输入！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def checking1(self):  # 注册时输入的号码检验是否已经注册过的
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.usrLine.text():
                return True
        c.close()
        conn.close()
        return False

    def save_data(self):  # 登录时密码在数据库中保存过来
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        a = self.usrLine.text()
        b = self.usrnameLine.text()
        c = self.pwdLineEdit1.text()
        conn.execute("INSERT INTO User VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    def accept(self):  # 注册时将账号密码保存并登录。
        if len(self.usrLine.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.usrLine.text()) != 11:
            self.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif (self.checking1()):
            self.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n\t请您登录！")
            self.sign = 1
        elif (len(self.usrnameLine.text()) == 0):
            self.messagelab.setText("提示!\n\t" + "用户名不能为空！")
            self.sign = 2
        elif len(self.pwdLineEdit1.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            try:
                self.timer_next.stop()
                self.timer_camera.stop()
                self_cap.release()  # 释放视频流
                self.newlab.clear()
            except:
                pass
            win.number = self.usrLine.text()
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Usr_informent())
            # 连接主窗口界面。

    def change_record(self):  # 连接用户登录界面
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Record())

class Record(QFrame):  # 用户登录界面
    def __init__(self):
        super(Record, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sign = 1
        self.number = ''
        self.passw = ''
        self.data = []
        self.data1 = []
        self.usr = QLabel("用户:")
        self.password = QLabel("密码:")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，对题目进行识别．
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("确定")
        self.but2 = QPushButton("登录")
        self.but3 = QPushButton("上一步")
        self.but4 = QPushButton("注册")
        self.but5 = QPushButton("忘记密码")
        self.but6 = QPushButton("退出")
        self.newlab = MyLabel("输入区")  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.password.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.password.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{background-color:rgb(230,230, 230)}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit.setPlaceholderText("请在输入框输入手机号码(一次输入不能超过四位数)")
        self.usrLineEdit.setMaximumSize(420, 40)
        self.usrLineEdit.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(420, 40)
        self.pwdLineEdit.setPlaceholderText("请在输入框输入密码(一次输入不能超过四位数)")
        self.pwdLineEdit.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.but1,0,0,1,2)
        self.layout.addWidget(self.but2,0,3,1,2)
        self.layout.addWidget(self.but3,0,6,1,2)
        self.layout.addWidget(self.but4,2,0,1,2)
        self.layout.addWidget(self.but5,2,3,1,2)
        self.layout.addWidget(self.but6,2,6,1,2)
        self.layout.addWidget(self.messagelab, 0, 12, 4, 9)
        self.layout.addWidget(self.progresslab, 4, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 3, 1, 4)
        self.layout.addWidget(self.newlab, 5, 0, 10, 10)
        self.layout.addWidget(self.usr, 7, 11, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 7, 12, 1, 8)
        self.layout.addWidget(self.password, 9, 11, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 9, 12, 1,8)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)


    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer_right(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if len(self.number) < 11:
                if data[1] > 0.6:
                    try:
                        da = data[0].replace('I','1').replace('l','1').replace('b','6').replace('q','9')
                    except:
                        da  = data[0]
                    self.data.append(self.number)
                    self.number = self.number + da
                    self.usrLineEdit.setText(self.number)
                    self.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t" +
                                            "如果输入错误请您在操作区输入＇上一步＇操作！！")
            if len(self.number)!=11:
                pass
            elif (self.checking1()):
                self.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            else:
                self.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入密码\n\t" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.pwdLineEdit.setText(self.passw)
                self.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")

    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal =1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.getanswer()
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "登录").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "确定").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "上一步").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "注册").quick_ratio()
                    num4 = difflib.SequenceMatcher(None, nexttext[0], "忘记密码").quick_ratio()
                    num5 = difflib.SequenceMatcher(None, nexttext[0], "退出").quick_ratio()
                    if (num > num1 and num > num2 and num > num3 and num > num4 and num > num5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：登录\n\t操作成功")
                        self.accept()
                    elif (num1 > num and num1 > num2 and num1 > num3 and num1 > num4 and num1 > num5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num and num2 > num3 and num2 > num4 and num2 > num5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                        sign = self.sign
                        if sign == 1:
                            if len(self.data)>0:
                                self.number = self.data[-1]
                                self.usrLineEdit.setText(self.number)
                                self.data = self.data[:-1]
                            else:
                                self.number = ''
                                self.usrLineEdit.setText(self.number)
                                self.data = []
                            self.messagelab.setText("提示!\n\t" +
                                                    "请您把账号分段输入，再输入确定！！")
                        elif sign == 2:
                            if len(self.data1)>0:
                                self.passw = self.data1[-1]
                                self.pwdLineEdit.setText(self.passw)
                                self.data1 = self.data1[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请您把密码分段输入，再输入确定！！")
                            else:
                                self.passw = ''
                                self.pwdLineEdit.setText(self.passw)
                                self.data1 = []
                                self.sign = 1
                                self.number = self.data[-1]
                                self.usrLineEdit.setText(self.number)
                                self.data = self.data[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请您把账号分段输入，再输入确定！！")
                    elif (num3 > num1 and num3 > num and num3 > num2 and num3 > num4 and num3 > num5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：注册\n\t操作成功")
                        self.logonfun()
                    elif (num4 > num1 and num4 > num and num4 > num2 and num4 > num3 and num4 > num5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：忘记密码\n\t操作成功")
                        self.forgetfun()
                    elif (num5 > num1 and num5 > num and num5 > num2 and num5 > num3 and num5 > num4):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：退出\n\t操作成功")
                        time.sleep(1)
                        try:
                            self.timer_next.stop()
                            self.timer_camera.stop()
                            self_cap.release()  # 释放视频流
                            self.newlab.clear()
                        except:
                            pass
                        win.close()
                        sys.exit()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def checking1(self):  # 登录时检验号码是否没有注册
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    def accept(self):  # 登录时判断密码是否正确
        if len(self.usrLineEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.usrLineEdit.text()) != 11:
            self.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif (self.checking1()):
            self.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            self.sign = 1
        elif len(self.pwdLineEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            d = 0
            for variate in c.fetchall():
                if variate[0] == self.usrLineEdit.text() and variate[2] == self.pwdLineEdit.text():
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:  # 连接主界面函数
                try:
                    self.timer_next.stop()
                    self.timer_camera.stop()
                    self_cap.release()  # 释放视频流
                    self.newlab.clear()
                except:
                    pass
                win.number = self.usrLineEdit.text()
                self.finddata()
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Function())
            else:
                self.messagelab.setText("提示!\n\t"+ "账号或密码输入错误")

    def forgetfun(self):  # 连接忘记密码界面
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Forget())

    def logonfun(self):  # 连接注册界面
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Logon())

    def finddata(self):
        time1 = datetime.datetime.now()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date")
        for variate in c.fetchall():
            if variate[0] == win.number:
                abcd = '%Y-%m-%d %H:%M:%S'
                b = datetime.datetime.strptime(variate[4], abcd)
                theTime = time1.strftime(abcd)
                if b.year == time1.year and b.month == time1.month and b.day == time1.day:
                    a = variate[2]
                else:
                    a = variate[2] + 1
                c.execute("update Student_date set logonday=(?),lasttime = (?) where number = (?)",
                          (a, theTime, win.number))
                conn.commit()
                break
        c.close()
        conn.close()

# 用户忘记密码
class Forget(QFrame):
    def __init__(self):
        super(Forget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr2 = QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.sign = 1
        self.number = ''
        self.passw = ''
        self.data = []
        self.data1 = []
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，对题目进行识别．
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("确定")
        self.but3 = QPushButton("上一步")
        self.but4 = QPushButton("修改")
        self.newlab = MyLabel("输入区")  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{background-color:rgb(230,230, 230)}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.usrLineEdit2.setPlaceholderText("请在输入区输入手机号码(一次输入不能超过四位数)")
        self.pwdLineEdit2.setPlaceholderText("请在输入区输入新的密码(一次输入不能超过四位数)")
        self.usrLineEdit2.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.but1,0,1,1,2)
        self.layout.addWidget(self.but2,0,6,1,2)
        self.layout.addWidget(self.but3,2,1,1,2)
        self.layout.addWidget(self.but4,2,6,1,2)
        self.layout.addWidget(self.messagelab, 0, 12, 4, 9)
        self.layout.addWidget(self.progresslab, 4, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 3, 1, 4)
        self.layout.addWidget(self.newlab, 5, 0, 10, 10)
        self.layout.addWidget(self.usr2, 7, 11, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 7, 12, 1, 10)
        self.layout.addWidget(self.pwd2, 10, 11, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 10, 12, 1, 10)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" +  "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                time.sleep(2)
                self.equal = 0
                self.timer_next.start(3500)

    def return_record(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Record())

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer_right(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if len(self.number) < 11:
                if data[1] > 0.6:
                    try:
                        da = data[0].replace('I','1').replace('l','1').replace('b','6').replace('q','9')
                    except:
                        da  = data[0]
                    self.data.append(self.number)
                    self.number = self.number + da
                    self.usrLineEdit2.setText(self.number)
                    self.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n" +
                                            "如果输入错误请您在操作区输入＇上一步＇操作")
            if len(self.number) != 11:
                pass
            elif (self.checking1()):
                self.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n请您先注册！")
            else:
                self.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入密码\n" +
                                         "如果输入错误请您在操作区输入＇上一步＇操作")
                self.sign = 2
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.pwdLineEdit2.setText(self.passw)
                self.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作")
        time.sleep(3)
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal =1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.getanswer()
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "确定").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "上一步").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "修改").quick_ratio()
                    if (num > num1 and num > num2 and num > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功!")
                        self.return_record()
                    elif (num1 > num and num1 > num2 and num1 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功!")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num and num2 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功!")
                        sign = self.sign
                        if sign == 1:
                            if len(self.data) > 0:
                                self.number = self.data[-1]
                                self.usrLineEdit2.setText(self.number)
                                self.data = self.data[:-1]
                            else:
                                self.number = ''
                                self.usrLineEdit2.setText(self.number)
                                self.data = []
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把账号分段输入输入区后，再在操作区输入确定！！")
                        elif sign == 2:
                            if len(self.data1) > 0:
                                self.passw = self.data1[-1]
                                self.pwdLineEdit2.setText(self.passw)
                                self.data1 = self.data1[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请把密码分段输入输入区后，再在操作区输入确定！！")
                            else:
                                self.passw = ''
                                self.pwdLineEdit2.setText(self.passw)
                                self.data1 = []
                                self.sign = 1
                                self.number = self.data[-1]
                                self.usrLineEdit2.setText(self.number)
                                self.data = self.data[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请把账号分段输入输入区后，再在操作区输入确定！！")
                    elif (num3 > num1 and num3 > num and num3 > num2):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：修改\n\t操作成功")
                        self.accept()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def checking1(self):  # 忘记密码时检验号码是否没有注册
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit2.text():
                return False
        c.close()
        conn.close()
        return True

    def savedate(self):  # 忘记密码时将新的密码在数据库中修改过来
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit2.text():
                win.number = variate[0]
                conn.execute("update User set password=(?) where number=(?)", (self.pwdLineEdit2.text(), variate[0],))
                break
        conn.commit()
        c.close()
        conn.close()

    def accept(self):  # 忘记密码时验证是否可以登录
        if len(self.usrLineEdit2.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.usrLineEdit2.text()) != 11:
            self.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif (self.checking1()):
            self.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            self.sign = 1
        elif len(self.pwdLineEdit2.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            self.savedate()
            self.finddata()
            try:
                self.timer_next.stop()
                self.timer_camera.stop()
                self_cap.release()  # 释放视频流
                self.newlab.clear()
            except:
                pass
            # 设置一个查询用户年级的函数
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Function())

            # 连接主窗口界面。

    def finddata(self):
        time1 = datetime.datetime.now()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date")
        for variate in c.fetchall():
            if variate[0] == win.number:
                abcd = '%Y-%m-%d %H:%M:%S'
                b = datetime.datetime.strptime(variate[4], abcd)
                theTime = time1.strftime(abcd)
                if b.year == time1.year and b.month == time1.month and b.day == time1.day:
                    a = variate[2]
                else:
                    a = variate[2] + 1
                c.execute("update Student_date set logonday=(?),lasttime = (?) where number = (?)",
                          (a, theTime, win.number))
                conn.commit()
                break
        c.close()
        conn.close()

# 用户信息填写
class Usr_informent(QFrame):
    def __init__(self):
        super(Usr_informent, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sign = 1
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearEdit = QLineEdit()
        self.sex = QLabel("性别:")
        self.sexEdit = QLineEdit()
        self.school = QLabel("学校:")
        self.grade = QLabel("年级")
        self.gradeEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，对题目进行识别．
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("确定")
        self.but2 = QPushButton("上一步")
        self.but3 = QPushButton("完成")
        self.newlab = MyLabel("输入区")  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{background-color:rgb(230,230, 230)}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.nameEdit.setPlaceholderText("请在输入区输入姓名")
        self.yearEdit.setPlaceholderText("请在输入区输入年月如:201912")
        self.sexEdit.setPlaceholderText("请在输入区输入性别")
        self.schoolEiit.setPlaceholderText("请在输入区输入学校名称")
        self.gradeEdit.setPlaceholderText("请在输入区输入年级")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.sexEdit.setFont(QFont("宋体", 14))
        self.yearEdit.setFont(QFont("宋体", 14))
        self.gradeEdit.setFont(QFont("宋体", 14))
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.name.setMaximumSize(100, 40)
        self.school.setMaximumSize(100, 40)
        self.year.setMaximumSize(100, 40)
        self.sex.setMaximumSize(100, 40)
        self.grade.setMaximumSize(100, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sexEdit.setMaximumSize(420, 40)
        self.gradeEdit.setMaximumSize(420, 40)
        self.yearEdit.setMaximumSize(420, 40)
        self.layout.addWidget(self.but1,1,0,1,2)
        self.layout.addWidget(self.but2,1,3,1,2)
        self.layout.addWidget(self.but3,1,6,1,2)
        self.layout.addWidget(self.messagelab, 0, 12, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 11, 10)
        self.layout.addWidget(self.name, 5, 10, 1, 2)
        self.layout.addWidget(self.nameEdit, 5, 12, 1, 8)
        self.layout.addWidget(self.sex, 7, 10, 1, 2)
        self.layout.addWidget(self.sexEdit, 7, 12, 1, 8)
        self.layout.addWidget(self.year, 9, 10, 1, 2)
        self.layout.addWidget(self.yearEdit, 9, 12, 1, 8)
        self.layout.addWidget(self.school, 11, 10, 1, 2)
        self.layout.addWidget(self.schoolEiit, 11, 12, 1, 8)
        self.layout.addWidget(self.grade, 13, 10, 1, 2)
        self.layout.addWidget(self.gradeEdit, 13, 12, 1, 8)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal  = 0
                time.sleep(2)
                self.timer_next.start(3500)


    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer_right(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            self.nameEdit.setText(data[0])
            self.messagelab.setText("提示!\n\t" + "姓名输入成功！请您下一步输入性别\n\t" +
                                    "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 2
        elif self.sign == 2:
            self.sexEdit.setText(data[0])
            self.messagelab.setText("提示!\n\t" + "性别输入成功！请您下一步输入出生年月\n\t" +
                                    "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.yearEdit.setText(da)
                self.messagelab.setText("提示!\n\t" + "出生年月输入成功！请您下一步输入学校" +
                                        "\n\t如果输入错误请您操作区输入＇上一步＇操作")
                self.sign = 4
        elif self.sign == 4:
            self.schoolEiit.setText(data[0])
            self.messagelab.setText("提示!\n\t" + "学校输入成功！请您下一步输入年级" +
                                    "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 5
        elif self.sign == 5:
            self.gradeEdit.setText(data[0])
            self.messagelab.setText("提示!\n\t" + "年级输入成功！" +
                                    "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 6
        time.sleep(3)
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")

    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.getanswer()
        num = difflib.SequenceMatcher(None, nexttext[0], "完成").quick_ratio()
        num1 = difflib.SequenceMatcher(None, nexttext[0], "确定").quick_ratio()
        num2 = difflib.SequenceMatcher(None, nexttext[0], "上一步").quick_ratio()
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    if (num > num1 and num > num2):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：完成\n\t操作成功!")
                        self.connect_fun()
                    elif (num1 > num and num1 > num2):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功!")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功!")
                        sign = self.sign
                        if sign == 1:
                            self.nameEdit.setText("")
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的姓名输入输入区后，再在操作区输入确定！！")
                        elif sign == 2:
                            self.nameEdit.setText("")
                            self.sign = 1
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的姓名输入输入区后，再在操作区输入确定！！")
                        elif sign == 3:
                            self.sexEdit.setText("")
                            self.sign = 2
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的性别输入输入区后，再在操作区＇输入确定！！")
                        elif sign == 4:
                            self.yearEdit.setText("")
                            self.sign = 3
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的出生年月输入输入区后，再在操作区输入确定！！")
                        elif sign == 5:
                            self.schoolEiit.setText("")
                            self.sign = 4
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的学校输入输入区后，再在操作区输入确定！！")
                        elif sign == 6:
                            self.gradeEdit.setText("")
                            self.sign = 5
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把您的年级输入输入区后，再在操作区输入确定！！")
                    else:
                        self.messagelab.setText("提示!\n" + "本次识别的操作为" + nexttext[0] +
                                                "\n该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def connect_fun(self):
        if len(self.nameEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "姓名框不能为空！！")
            self.sign = 1
        elif len(self.sexEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "性别框不能为空！！")
            self.sign = 2
        elif len(self.yearEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "出生年月框不能为空！！")
            self.sign = 3
        elif len(self.schoolEiit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "学校框不能为空！！")
            self.sign = 4
        elif len(self.gradeEdit.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "年级框不能为空！！")
            self.sign = 5
        else:
            try:
                self.timer_next.stop()
                self.timer_camera.stop()
                self_cap.release()  # 释放视频流
                self.newlab.clear()
            except:
                pass
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Function())

    def save_data(self):
        self.image_path = "../datas/image/a7.jpeg"
        a = self.nameEdit.text()
        b = self.yearEdit.text()
        c = self.sexEdit.text()
        d = self.schoolEiit.text()
        e = self.gradeEdit.text()
        print(10)
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        print(0)
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab)
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_date VALUES(?,?,?,?,?,?)", (win.number, a, b, c, d, e))
        conn.execute("insert into User_image values(?,?,?)", (win.number, total, '.jpeg',))
        conn.execute("INSERT INTO Student_date VALUES(?,?,?,?,?)", (win.number, theTime, 1, 0.0, theTime))
        conn.commit()
        conn.close()
        print(101)
        sqlpath = "../datas/database/SQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:  # 开始时间  ， 课程号，课程名， 文件名 ， 结束时间
            c.execute(
                '''CREATE TABLE User_data(strat_time text,Cno text,Coursename text, filename text,last_time text)''')
        except:
            pass
        c.close()
        conn.close()
        print(120)

class MyLabel3(QLabel):
    def __init__(self):
        super(MyLabel3,self).__init__()
        self.x0 = 150
        self.y0 = 250
        self.x1 = 400
        self.y1 = 350
        self.lab1 = QLabel(self)
        self.lab1.setText("操作区")
        self.lab1.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:18px;font-family:Arial;background:transparent;}")
        #self.lab1.setStyleSheet("background:transparent")
        #op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        #op.setOpacity(0.6)
        #self.lab1.setGraphicsEffect(op)
        self.lab1.setMaximumSize(100,100)
        self.lab1.move(150,250)

    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)

class Function(QFrame):  # 用户功能界面
    def __init__(self):
        super(Function, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("查看课程")
        self.but2 = QPushButton("学习记录")
        self.but3 = QPushButton("我的")
        self.but4 = QPushButton("退出")
        self.newlab = MyLabel3()  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 2
        self.width1 = self.screenRect.width() / 2
        self.resize(self.width1 * 2, self.height1 * 2)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1, 90)
        self.newlab.setMaximumSize(600, 550)
        self.layout.addWidget(self.but1, 0, 1, 1, 2)
        self.layout.addWidget(self.but2, 0, 6, 1, 2)
        self.layout.addWidget(self.but3, 2, 1, 1, 2)
        self.layout.addWidget(self.but4, 2, 6, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 10, 4, 9)
        self.layout.addWidget(self.progresslab, 4, 8, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 9, 1, 4)
        self.layout.addWidget(self.newlab, 5, 7, 10, 10)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600,550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal =1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "查看课程").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "学习记录").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "我的").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "退出").quick_ratio()
                    if (num > num1 and num>num2 and num>num3):

                        self.messagelab.setText("提示!\n\t" + "本次操作为：查看课程\n\t操作成功！！")
                        try:
                            self.timer_next.stop()
                            self.timer_camera.stop()
                            self_cap.release()  # 释放视频流
                        except:
                            pass
                        self.newlab.clear()
                        win.splitter.widget(0).setParent(None)
                        win.splitter.insertWidget(0, My_Course())
                    elif (num1 > num and num1>num2 and num1>num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：学习记录\n\t操作成功！！")
                        try:
                            self.timer_next.stop()
                            self.timer_camera.stop()
                            self_cap.release()  # 释放视频流
                        except:
                            pass
                        self.newlab.clear()
                        win.splitter.widget(0).setParent(None)
                        win.splitter.insertWidget(0, Usr_report())
                    elif (num2 > num and num2 > num1 and num2>num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：我的\n\t操作成功！！")
                        try:
                            self.timer_next.stop()
                            self.timer_camera.stop()
                            self_cap.release()  # 释放视频流
                        except:
                            pass
                        self.newlab.clear()
                        win.splitter.widget(0).setParent(None)
                        win.splitter.insertWidget(0,Usr_myself())
                    elif (num3 > num and num3 > num1 and num3>num2):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：退出\n\t操作成功！！")
                        try:
                            self.timer_next.stop()
                            self.timer_camera.stop()
                            self_cap.release()  # 释放视频流
                        except:
                            pass
                        self.newlab.clear()
                        win.splitter.widget(0).setParent(None)
                        win.splitter.insertWidget(0, Record())
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

class My_Course(QFrame):
    def __init__(self):
        super(My_Course, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.sign = 0
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel2()  # 放置视频
        self.qtool = QToolBox()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("添加课程")
        self.but3 = QPushButton("上一页")
        self.but4 = QPushButton("下一页")
        self.but5 = QPushButton("课程一")
        self.but6 = QPushButton("课程二")
        self.but7 = QPushButton("课程三")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.resize(self.width1 * 4, self.height1 * 4)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                          QPushButton{background-color:rgb(170,200, 50)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(400, 450)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                          from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                           where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                            and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                            and Join_Course.number=(?)", (win.number,))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = Coursewindow(self.datas, self.sign)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.qtool.addItem(self.window1, "我的课程")
        self.layout.addWidget(self.but1,0,0,1,2)
        self.layout.addWidget(self.but2,0,3,1,2)
        self.layout.addWidget(self.but3,0,6,1,2)
        self.layout.addWidget(self.but4,0,9,1,2)
        self.layout.addWidget(self.but5, 2, 0, 1, 2)
        self.layout.addWidget(self.but6, 2, 3, 1, 2)
        self.layout.addWidget(self.but7, 2, 6, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 12, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 6, 8)
        self.layout.addWidget(self.qtool, 4, 8, 10, 14)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                time.sleep(2)
                self.equal = 0
                self.timer_next.start(3500)

    def returnfun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (400,450))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def add_images(self):
        self.equal =1
        self.sign = self.sign +3
        n = len(self.datas)
        if n>self.sign:
            self.qtool.removeItem(0)
            self.window1 = Coursewindow(self.datas, self.sign)
            self.qtool.addItem(self.window1, '我的课程')
        else:
            self.sign = self.sign - 3
        self.timer_next.start(3500)

    def cut_images(self):
        self.sign = self.sign - 3
        if self.sign <0:
            self.sign=0
        self.qtool.removeItem(0)
        self.window1 = Coursewindow(self.datas, self.sign)
        self.qtool.addItem(self.window1, '我的课程')
        self.timer_next.start(3500)

    def next_step_fun(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "上一页").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "下一页").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "添加课程").quick_ratio()
                    num4 = difflib.SequenceMatcher(None, nexttext[0], "课程一").quick_ratio()
                    num5 = difflib.SequenceMatcher(None, nexttext[0], "课程二").quick_ratio()
                    num6 = difflib.SequenceMatcher(None, nexttext[0], "课程三").quick_ratio()
                    if (num > 0.5):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                        self.returnfun()
                    elif (num1 > 0.5 and num1 > num2):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                        self.cut_images()
                    elif (num2 > 0.5 and num2 > num1):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                        self.add_images()
                    elif (num3 > 0.5 and num3 > num4 and num3 > num5 and num3 > num6):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：添加课程\n\t操作成功！！")
                        self.addfun()
                    elif (num4 > num5 and num4 > num6):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：课程一\n\t操作成功！！")
                        self.openfile(0)
                    elif (num5 > num4 and num5 > num6):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：课程二\n\t操作成功！！")
                        sign = self.sign + 2
                        n = len(self.datas)
                        if n > sign:
                            self.openfile(1)
                        else:
                            self.messagelab.setText("提示!\n\t" + "本页没有课程二\n\t请您换一个操作！！")
                            self.timer_next.start(3500)
                    elif (num6 > num4 and num6 > num5):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：课程三\n\t操作成功！！")
                        sign = self.sign + 3
                        n = len(self.datas)
                        if n > sign:
                            self.openfile(2)
                        else:
                            self.messagelab.setText("提示!\n\t" + "本页没有课程三\n\t请您换一个操作！！")
                            self.timer_next.start(3500)
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def addfun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        self.add = AddCourse()
        # 接受子窗口传回来的信号  然后调用主界面的函数
        self.add.my_Signal.connect(self.changfun)
        self.add.show()

    def changfun(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(3500)
                self.equal = 0
                self.qtool.removeItem(0)
                conn = sqlite3.connect('../datas/database/Information.db')
                c = conn.cursor()
                c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                         from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                          where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                           and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                           and Join_Course.number=(?)", (win.number,))
                self.datas = c.fetchall()
                c.close()
                conn.close()
                self.window1 = Coursewindow(self.datas, self.sign)
                self.qtool.addItem(self.window1, '我的课程')

    def openfile(self,n):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        data = self.datas[self.sign + n][:3]
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Course_news(data))

class CustomWidget(QWidget):
    def __init__(self, data,y):
        super(CustomWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        if y==0:
            text = "课程一: "
        elif y==1:
            text = "课程二: "
        elif y==2:
            text = "课程三: "
        self.imagelab = QLabel()
        self.namelab = QLabel(text+data[2])
        self.teacherlab = QLabel("老师:")
        self.teacherlab2 = QLabel(str(data[3]))
        self.image_path = "../datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.teacherlab.setMaximumSize(80, 40)
        self.teacherlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.teacherlab, 3, 8, 1, 1)
        self.layout.addWidget(self.teacherlab2, 3, 9, 1, 2)

class Coursewindow(QListWidget):
    def __init__(self, datas,sign):
        super(Coursewindow, self).__init__()
        x = 0
        y = 0
        for data in datas:
            if y==3:
                break
            if x>=sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CustomWidget(data,y))
                y = y + 1
            x = x + 1

class Course_news(QFrame):
    def __init__(self, data):
        super(Course_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data
        self.sign1 = '课件'
        self.sign = 0
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("问问题")
        self.but3 = QPushButton("上一页")
        self.but4 = QPushButton("下一页")
        self.but5 = QPushButton("练习")
        self.but6 = QPushButton("课件一")
        self.but7 = QPushButton("课件二")
        self.but8 = QPushButton("课件三")
        self.newlab = MyLabel2()  # 放置视频
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.resize(self.width1*4, self.height1*4)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.but8.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                                  QPushButton{background-color:rgb(170,200, 50)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(400, 450)
        sqlpath = "../datas/database/ControllerSQ" + str(self.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                          Filename,Fileimage where Filename.no = Fileimage.no \
                           and Cno=(?) ", (self.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.qtool.addItem(self.window1, self.data[2] + " 课件")
        self.layout.addWidget(self.but1, 0, 0, 1, 2)
        self.layout.addWidget(self.but2, 0, 3, 1, 2)
        self.layout.addWidget(self.but3, 0, 6, 1, 2)
        self.layout.addWidget(self.but4, 0, 9, 1, 2)
        self.layout.addWidget(self.but5, 2, 0, 1, 2)
        self.layout.addWidget(self.but6, 2, 3, 1, 2)
        self.layout.addWidget(self.but7, 2, 6, 1, 2)
        self.layout.addWidget(self.but8,2,9,1,2)
        self.layout.addWidget(self.messagelab, 0, 12, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 6, 8)
        self.layout.addWidget(self.qtool, 4, 8, 10, 14)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                time.sleep(2)
                self.equal = 0
                self.timer_next.start(3500)

    def returnfun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, My_Course())

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (400,450))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    if self.sign1 == "课件":
                        num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                        num1 = difflib.SequenceMatcher(None, nexttext[0], "上一页").quick_ratio()
                        num2 = difflib.SequenceMatcher(None, nexttext[0], "下一页").quick_ratio()
                        num3 = difflib.SequenceMatcher(None, nexttext[0], "问问题").quick_ratio()
                        num4 = difflib.SequenceMatcher(None, nexttext[0], "练习").quick_ratio()
                        num5 = difflib.SequenceMatcher(None, nexttext[0], "课件一").quick_ratio()
                        num6 = difflib.SequenceMatcher(None, nexttext[0], "课件二").quick_ratio()
                        num7 = difflib.SequenceMatcher(None, nexttext[0], "课件三").quick_ratio()
                        if (num > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                            self.returnfun()
                        elif (num1 > 0.5 and num1 > num2):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                            self.cut_images()
                        elif (num2 > 0.5 and num2 > num1):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                            self.add_images()
                        elif (num3 > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：问问题\n\t操作成功！！")
                            self.questionfun()
                        elif (num4 > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：练习\n\t操作成功！！")
                            self.changexfun()
                        elif (num5 > num6 and num5 > num7):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：课件一\n\t操作成功！！")
                            self.openfile(0)
                        elif (num6 > num5 and num6 > num7):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：课件二\n\t操作成功！！")
                            sign = self.sign + 2
                            n = len(self.datas)
                            if n > sign:
                                self.openfile(1)
                            else:
                                self.messagelab.setText("提示!\n\t" + "本页没有课件二\n\t请您换一个操作！！")
                        elif (num7 > num6 and num7 > num5):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：课件三\n\t操作成功！！")
                            sign = self.sign + 3
                            n = len(self.datas)
                            if n > sign:
                                self.openfile(2)
                            else:
                                self.messagelab.setText("提示!\n\t" + "本页没有课件三\n\t请您换一个操作！！")
                        else:
                            self.messagelab.setText("提示!\n\t" + "本次识别的操作为"+nexttext[0]+
                                                    "\n\t该页面没有该操作，请您重新操作！！")
                    elif self.sign1 == "练习":
                        num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                        num1 = difflib.SequenceMatcher(None, nexttext[0], "上一页").quick_ratio()
                        num2 = difflib.SequenceMatcher(None, nexttext[0], "下一页").quick_ratio()
                        num3 = difflib.SequenceMatcher(None, nexttext[0], "问问题").quick_ratio()
                        num4 = difflib.SequenceMatcher(None, nexttext[0], "课件").quick_ratio()
                        num5 = difflib.SequenceMatcher(None, nexttext[0], "练习一").quick_ratio()
                        num6 = difflib.SequenceMatcher(None, nexttext[0], "练习二").quick_ratio()
                        num7 = difflib.SequenceMatcher(None, nexttext[0], "练习三").quick_ratio()
                        if (num > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                            self.returnfun()
                        elif (num1 > 0.5 and num1 > num2):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                            self.cut_images2()
                        elif (num2 > 0.5 and num2 > num1):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                            self.add_images2()
                        elif (num3 > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：问问题\n\t操作成功！！")
                            self.questionfun()
                        elif (num4 > 0.5):
                            self.timer_next.stop()
                            self.messagelab.setText("提示!\n\t" + "本次操作为：课件\n\t操作成功！！")
                            self.changexfun2()
                        elif (num5 > num6 and num5 > num7):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：练习一\n\t操作成功！！")
                            self.openfile2(0)
                        elif (num6 > num5 and num6 > num7):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：练习二\n\t操作成功！！")
                            sign = self.sign + 2
                            n = len(self.datas)
                            if n > sign:
                                self.openfile2(1)
                            else:
                                self.messagelab.setText("提示!\n\t" + "本页没有练习二\n\t请您换一个操作！！")
                        elif (num7 > num6 and num7 > num5):
                            self.messagelab.setText("提示!\n\t" + "本次操作为：练习三\n\t操作成功！！")
                            sign = self.sign + 3
                            n = len(self.datas)
                            if n > sign:
                                self.openfile2(2)
                            else:
                                self.messagelab.setText("提示!\n\t" + "本页没有练习三\n\t请您换一个操作！！")
                        else:
                            self.messagelab.setText("提示!\n\t" + "本次识别的操作为"+nexttext[0]+
                                                    "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def add_images(self):
        self.sign = self.sign +3
        n = len(self.datas)
        if n>self.sign:
            self.qtool.removeItem(0)
            self.window1 = CuFileQlist(self.datas, self.sign)
            self.qtool.addItem(self.window1, self.data[2] + " 课件")
        else:
            self.sign = self.sign-3
            self.messagelab.setText("抱歉!\n\t" + "这是最后一页了" )
        self.timer_next.start(3500)

    def cut_images(self):
        self.sign = self.sign - 3
        print(self.sign)
        if self.sign <0:
            self.sign=0
        self.qtool.removeItem(0)
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.qtool.addItem(self.window1, self.data[2] + " 课件")
        self.timer_next.start(3500)

    def add_images2(self):
        self.sign = self.sign + 3
        n = len(self.datas)
        if n > self.sign:
            self.qtool.removeItem(0)
            self.window1 = CourseexQlist(self.datas, self.sign)
            self.qtool.addItem(self.window1, self.data[2] + " 练习")
        else:
            self.sign = self.sign-3
            self.messagelab.setText("抱歉!\n\t" + "这是最后一页了" )
        self.timer_next.start(3500)

    def cut_images2(self):
        self.sign = self.sign - 3
        if self.sign < 0:
            self.sign = 0
        self.qtool.removeItem(0)
        self.window1 = CourseexQlist(self.datas, self.sign)
        self.qtool.addItem(self.window1, self.data[2] + " 练习")
        self.timer_next.start(3500)

    def changexfun(self):
        self.but5.setText("课件")
        self.but6.setText("练习一")
        self.but7.setText("练习二")
        self.but8.setText("练习三")
        self.sign = 0
        self.sign1 = "练习"
        sqlpath = "../datas/database/ControllerSQ" + str(self.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select no,name from Filename2 where Cno=(?) ", (self.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.qtool.removeItem(0)
        self.window1 = CourseexQlist(self.datas, self.sign)
        self.qtool.addItem(self.window1, self.data[2] + " 　练习")
        self.timer_next.start(3500)

    def changexfun2(self):
        self.but5.setText("练习")
        self.but6.setText("课件一")
        self.but7.setText("课件二")
        self.but8.setText("课件三")
        self.sign = 0
        self.sign1 = "课件"
        sqlpath = "../datas/database/ControllerSQ" + str(self.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                                  Filename,Fileimage where Filename.no = Fileimage.no \
                                   and Cno=(?) ", (self.data[0],))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.qtool.removeItem(0)
        self.window1 = CuFileQlist(self.datas, self.sign)
        self.qtool.addItem(self.window1, self.data[2] + " 　课件")
        self.timer_next.start(3500)

    def openfile(self,n):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        da = self.datas[self.sign+n][:2]
        sqlpath = "../datas/database/ControllerSQ" + str(self.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Cname,name,total,filename1 from \
                               Filename,Filedate where Filename.no= Filedate.no \
                                and Filename.no=(?)", (da[0],))
        filedata = c.fetchall()[0]
        zip_path = '../datas/' + filedata[0]
        if (not (os.path.exists(zip_path))):  # 创建文件夹。
            os.makedirs(zip_path)
        zip_path = zip_path + '/' + filedata[1] + filedata[3]
        total = base64.b64decode(filedata[2])
        f = open(zip_path, 'wb')
        f.write(total)
        f.close()
        self.zip_to_files(zip_path)
        self.max = max_widget(self,self.data[0],filedata[0],da[1])
        self.max.show()

    def openfile2(self,n):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        da = self.datas[self.sign+n][:2]
        sqlpath = "../datas/database/ControllerSQ" + str(self.data[1]) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Cname,name,answer,total,filename1 from \
                               Filename2,Filedate2 where Filename2.no= Filedate2.no \
                                and Filename2.no=(?)", (da[0],))
        filedata = c.fetchall()[0]
        zip_path = '../datas/' + filedata[0]
        if (not (os.path.exists(zip_path))):  # 创建文件夹。
            os.makedirs(zip_path)
        zip_path = zip_path + '/' + filedata[1] + filedata[4]
        total = base64.b64decode(filedata[3])
        f = open(zip_path, 'wb')
        f.write(total)
        f.close()
        self.zip_to_files(zip_path)
        self.practice = Practice_widget(self,self.data[0], filedata[:3], da[1])
        self.practice.show()

    def changetime(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(3500)

    def questionfun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Question(self.data))

    def zip_to_files(self, zippath):  # 将压缩包解压
        path = '../datas/tupian'
        if (os.path.isdir(path)):  # 判断文件夹是否存在
            fileNames = glob.glob(path + r'/*')
            if fileNames:
                for fileName in fileNames:  # 将pa 文件夹中的文件删除。
                    os.remove(fileName)
        else:
            os.mkdir(path)
        zf = zipfile.ZipFile(zippath)
        for fn in zf.namelist():  # 循环压缩包中的文件并保存进新文件夹。
            #right_fn = fn.replace('\\\\', '_').replace('\\', '_').replace('//', '_').replace('/', '_')  # 将文件名正确编码
            right_fn = fn.encode('cp437').decode('gbk')  # 将文件名正确编码
            right_fn = path + '/' + right_fn
            with open(right_fn, 'wb') as output_file:  # 创建并打开新文件
                with zf.open(fn, 'r') as origin_file:  # 打开原文件
                    shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
        zf.close()
        os.remove(zippath)

#课件的item 设计
class CuFileWidget(QWidget):
    def __init__(self, data,y):
        super(CuFileWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        if y==0:
            text = "课件一: "
        elif y==1:
            text = "课件二: "
        elif y==2:
            text = "课件三: "
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(text +data[1])
        self.image_path = "../datas/image/image" + data[3]
        total = base64.b64decode(data[2])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(800, 80)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)

#课件的QList
class CuFileQlist(QListWidget):
    def __init__(self,datas,sign):
        super(CuFileQlist, self).__init__()
        self.datas = datas
        x = 0
        y = 0
        for data in self.datas:
            if y==3:
                break
            if x>=sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CuFileWidget(data,y))
                y=y+1
            x=x+1

#练习的item 设计
class CourseexWidget(QWidget):
    def __init__(self, data,y):
        super(CourseexWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        if y==0:
            text = "练习一: "
        elif y==1:
            text = "练习二: "
        elif y==2:
            text = "练习三: "
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.namelab = QLabel(text + data[1])
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.namelab.setMaximumSize(800, 100)
        self.layout.addWidget(self.namelab, 1, 1, 1, 1)

#练习的QList
class CourseexQlist(QListWidget):
    def __init__(self,datas,sign):
        super(CourseexQlist, self).__init__()
        self.datas = datas
        x = 0
        y = 0
        for data in self.datas:
            if y == 3:
                break
            if x >= sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CourseexWidget(data,y))
                y = y + 1
            x = x + 1

class max_widget(QWidget):
    def __init__(self,dow,data1,data2,data3):
        super(max_widget, self).__init__()
        self.pa = '../datas/tupian'
        self.a = 1
        self.dow = dow
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.fileNames = glob.glob(self.pa + r'/*')
        self.startime = datetime.datetime.now()
        self.setWindowTitle(data3)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint
                            | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool |Qt.FramelessWindowHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()/4
        self.width1 = self.screenRect.width()/4
        self.resize(self.width1*4, self.height1*4)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel2()  # 放置视频
        self.but1 = QPushButton("关闭")
        self.but2 = QPushButton("上一页")
        self.but3 = QPushButton("下一页")

        self.lab2 = QtWidgets.QLabel(self)
        self.lab2.resize(self.width1*4, self.height1*4)
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                    QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                    QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                    QPushButton{background-color:rgb(170,200, 50)}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(400, 450)
        pa = self.fileNames[self.a-1]
        pixmap = QPixmap(pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.lab2.setPixmap(pixmap)  # 在label上显示图片
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.layout.addWidget(self.but1, 1, 0, 1, 2)
        self.layout.addWidget(self.but2, 1, 3, 1, 2)
        self.layout.addWidget(self.but3, 1, 6, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 1, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 2, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 6)
        self.layout.addWidget(self.lab2, 4, 7, 10, 15)
        self.messagelab.setText("提示!\n\t" + "请把操作放在操作区！！")
        #self.messagelab2.setText("请将下一步操作放在操作区" + "\n操作有：1.关闭．2.上一页．3．下一页．")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def closewin(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        ab = '%Y-%m-%d %H:%M:%S'
        endtime = datetime.datetime.now()
        b = endtime- self.startime
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)",(win.number,))
        data= c.fetchall()[0]
        da = data[3] + b.seconds
        conn.execute("update Student_date set stude_day =(?) where number=(?)", (da, win.number))
        conn.commit()
        c.execute("select * from Coursetime where number=(?) and Cno=(?)", (win.number,self.data1))
        data = c.fetchall()[0]
        da = data[2] + b.seconds
        conn.execute("update Coursetime set time =(?) where number=(?)and Cno=(?)", (da, win.number,self.data1))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/SQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?)",
                       (self.startime.strftime(ab), self.data1, self.data2, self.data3, endtime.strftime(ab)))
        conn.commit()
        conn.close()
        self.close()
        self.dow.changetime()

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (400,450))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作写在操作区识别.")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal=1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "关闭").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "上一页").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "下一页").quick_ratio()
                    if (num > num1):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n" + "本次操作为：关闭\n操作成功")
                        self.closewin()
                    elif (num1 > num2):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n" + "本次操作为：上一页\n操作成功")
                        self.cut_images()
                    elif (num2 > num1):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n" + "本次操作为：下一页\n操作成功")
                        self.add_images()
                    else:
                        self.messagelab.setText("提示!\n" + "本次识别的操作为" + nexttext[0] +
                                                "\n该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def add_images(self):  # 下一页ppt
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
        except:
            self.a = self.a - 1
            self.messagelab.setText("提示!\n\t" + "这是最后一页")
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.lab2.setPixmap(pixmap)  # 在label上显示图片
        self.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.timer_next.start(3500)

    def cut_images(self):  # 上一页ppt
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.messagelab.setText("提示!\n\t" + "这是第一页")
        else:
            self.timer_next.stop()
            self.pa = self.fileNames[self.a]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.lab2.setPixmap(pixmap)  # 在label上显示图片
            self.lab2.setScaledContents(True)  # 让图片自适应label大小
        self.timer_next.start(3500)

class MyLabel2(QLabel):
    def __init__(self):
        super(MyLabel2,self).__init__()
        self.x0 = 100
        self.y0 = 175
        self.x1 = 300
        self.y1 = 275
        self.lab1 = QLabel(self)
        self.lab1.setText("操作区")
        self.lab1.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:18px;font-family:Arial;background:transparent;}")
        #self.lab1.setStyleSheet("background:transparent")
        #op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        #op.setOpacity(0.6)
        #self.lab1.setGraphicsEffect(op)
        self.lab1.setMaximumSize(100,100)
        self.lab1.move(100,175)

    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)

class MyLabel(QLabel):
    def __init__(self,text):
        super(MyLabel,self).__init__()
        self.x0 = 150
        self.y0 = 120
        self.x1 = 400
        self.y1 = 220
        self.x2 = 150
        self.y2 = 320
        self.x3 = 400
        self.y3 = 420
        self.lab1 = QLabel(self)
        self.lab2 = QLabel(self)
        self.lab1.setText(text)
        self.lab2.setText("操作区")
        self.lab1.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:18px;font-family:Arial;background:transparent;}")
        self.lab2.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:18px;font-family:Arial;background:transparent;}")
        self.lab1.setMaximumSize(100,200)
        self.lab2.setMaximumSize(100,200)
        self.lab1.move(150,120)
        self.lab2.move(150,320)

    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)
        rect1 = QRect(self.x2, self.y2, abs(self.x3 - self.x2), abs(self.y3 - self.y2))
        painter2 = QPainter(self)
        painter2.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter2.drawRect(rect1)

class Practice_widget(QWidget):
    def __init__(self,dow,data1,data2,data3):
        super(Practice_widget, self).__init__()
        self.startime = datetime.datetime.now()
        self.pa = '../datas/tupian'
        self.a = 0
        self.dow = dow
        self.data1 = data1
        self.data2 = data2[0]
        self.data3 = data3

        list3 = data2[2].split("@")
        self.answers = []
        for list in list3:
            da = list.split("#")
            self.answers.append(da)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  #定义定时器，对题目进行识别．
        self.fileNames = glob.glob(self.pa + r'/*')
        self.imagelab = QLabel() #放置问题的图片
        self.messagelab = QLabel() #用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.answerlab  = QLabel()  #放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("关闭")
        self.but2 = QPushButton("上一题")
        self.but3 = QPushButton("下一题")
        self.but4 = QPushButton("验证答案")
        self.newlab = MyLabel("答案区") #放置视频
        self.devise_ui()

    def devise_ui(self):
        self.setWindowTitle(self.data3)
        palette1 = QPalette()
        palette1.setColor(palette1.Background, QColor(245, 245, 245))
        self.setPalette(palette1)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint
                            | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool | Qt.FramelessWindowHint)
        #self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:16px;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:30px;font-weight:Bold;font-family:Arial;}")
        self.answerlab.setAlignment(Qt.AlignCenter)
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.pa = self.fileNames[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.imagelab.setPixmap(pixmap)  # 在label上显示图片
        self.imagelab.setScaledContents (True) # 让图片自适应label大小
        self.setextlab.setMaximumSize(150,40)
        self.progresslab.setMaximumSize(40,40)
        self.imagelab.setMaximumSize(self.width1/2,100)
        self.messagelab.setMaximumSize(self.width1/2,90)
        self.newlab.setMaximumSize(600,550)
        self.answerlab.setMaximumSize(self.width1/2,self.height1-200)
        self.layout.addWidget(self.but1, 0, 2, 1, 2)
        self.layout.addWidget(self.but2, 0, 6, 1, 2)
        self.layout.addWidget(self.but3, 2, 2, 1, 2)
        self.layout.addWidget(self.but4,2,6,1,2)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab,3,3,1,1)
        self.layout.addWidget(self.setextlab,3,4,1,4)
        self.layout.addWidget(self.imagelab,3,11,3,10)
        self.layout.addWidget(self.newlab,4,0,10,10)
        self.layout.addWidget(self.answerlab,6,11,7,10)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "请把答案放置在答案区后在操作区输入验证答案！！")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别题目中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal  = 0
                time.sleep(2)
                self.timer_next.start(3500)


    def closewin(self):
        self.timer_next.stop()
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        try:
            os.remove("../datas/wen/answer.jpg")
        except:
            pass
        ab = '%Y-%m-%d %H:%M:%S'
        endtime = datetime.datetime.now()
        b = endtime - self.startime
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)", (win.number,))
        data = c.fetchall()[0]
        da = data[3] + b.seconds
        conn.execute("update Student_date set stude_day =(?) where number=(?)", (da, win.number))
        conn.commit()
        c.execute("select * from Coursetime where number=(?) and Cno=(?)", (win.number, self.data1))
        data = c.fetchall()[0]
        da = data[2] + b.seconds
        conn.execute("update Coursetime set time =(?) where number=(?)and Cno=(?)", (da, win.number, self.data1))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/SQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?)",
                     (self.startime.strftime(ab), self.data1, self.data2, self.data3, endtime.strftime(ab)))
        conn.commit()
        conn.close()
        self.close()
        self.dow.changetime()

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600,550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]
        gray = cv2.cvtColor(face1, cv2.COLOR_RGB2GRAY)  # 生成的的灰度图是单通道图像
        self.face1 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # 将单通道图像转换为三通道RGB灰度图，因为只有三通道的backface才可以赋给三通道的src
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage


    def contrast_answer_right(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
        if data[1] > 0.85:
            for answer in self.answers:
                if answer[0] == self.filename:
                    if answer[1] == da:
                        self.answerlab.setText("答案：" + answer[1] + "\n解析:\n" + answer[2])
                        self.messagelab.setText("提示!\n\t" + "回答正确！！")
                        x = 1
                        time.sleep(3)
        else:
            self.messagelab.setText("提示!\n\t"+ "请写入答案后再验证答案！！！")
        if x==0:
            self.messagelab.setText("提示!\n\t" + "回答错误\n\t请把正确答案放置在答案区！！")
            self.answerlab.setText("")
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal,imgpath,imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "请把答案放置在答案区后在操作区输入验证答案！！")

    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "下一题").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "上一题").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "关闭").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "验证答案").quick_ratio()
                    if (num > num1 and num > num2 and num > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：下一题\n\t操作成功")
                        self.addfun()
                    elif (num1 > num and num1 > num2 and num1 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一题\n\t操作成功")
                        self.lastfun()
                    elif (num2 > num1 and num2 > num and num2 > num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：关闭\n\t操作成功")
                        self.closewin()
                    elif (num3 > num1 and num3 > num and num3 > num2):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：验证答案\n\t操作成功")
                        self.contrast_answer()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def addfun(self):
        try:
            os.remove("../datas/wen/answer.jpg")
        except:
            pass
        self.timer_next.stop()
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.answerlab.clear()
        except:
            self.a = self.a - 1
            self.pa = self.fileNames[self.a]
            self.messagelab.setText("提示!\n\t"+"这是最后一题")
        self.timer_next.start(3500)

    def lastfun(self):
        try:
            os.remove("../datas/wen/answer.jpg")
        except:
            pass
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.messagelab.setText("提示!\n\t"+"这是第一题")
        else:
            self.timer_next.stop()
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.answerlab.clear()
            self.timer_next.start(3500)

class ContrastJob(QtCore.QThread):
    updated = QtCore.pyqtSignal()
    def __init__(self,path):
        super(ContrastJob, self).__init__()
        self.path = path
        self.answer = ''

    def run(self):
        try:
            self.answer = tr.recognize(self.path)
            print(self.answer)
            self.updated.emit()
        except:
            pass

    def getanswer(self):
        return self.answer

class NextStepJob(QtCore.QThread):
    updated = QtCore.pyqtSignal()
    updated2 = QtCore.pyqtSignal()
    updated3 = QtCore.pyqtSignal()
    def __init__(self,equal,path1,path2):
        super(NextStepJob, self).__init__()
        self.equal = equal
        self.path1 = path1
        self.path2 = path2
        self.answer = ''


    def run(self):
        if self.equal == 1:
            image1 = cv2.imread(self.path1)
            image2 = cv2.imread(self.path2)
            result = classify_hist_with_split(image1, image2)
            if result[0] > 0.75:
                self.updated3.emit()
            else:
                self.updated2.emit()
                try:
                    self.answer = tr.recognize(self.path1)
                    print(self.answer)
                    self.updated.emit()
                except:
                    pass
        else:
            self.updated2.emit()
            try:
                self.answer = tr.recognize(self.path1)
                print(self.answer)
                self.updated.emit()
            except:
                pass


    def getanswer(self):
        return self.answer

class AnswerJob(QtCore.QThread):
    updated = QtCore.pyqtSignal()
    def __init__(self,path):
        super(AnswerJob, self).__init__()
        self.path = path
        self.answer = []
        self.operator_precedence = {
            '(': 0,
            ')': 0,
            '+': 1,
            '-': 1,
            '/': 2,
            '*': 2,
        }

    def run(self):
        try:
            answer = tr.recognize(self.path)
            print(answer)
            answer = answer[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9').replace('x', '*').replace(':', '/')
            postfix = self.postfix_convert(answer)
            da = self.cal_expression_tree(postfix)
        except:
            pass
        self.updated.emit()

    def postfix_convert(self,exp):
        '''
        将表达式字符串，转为后缀表达式
        如exp = "1+2*(3-1)-4"
        转换为：postfix = ['1', '2', '3', '1', '-', '*', '+', '4', '-']
        '''
        stack = []  # 运算符栈，存放运算符
        postfix = []  # 后缀表达式栈
        x = 0
        for char in exp:
            if char not in self.operator_precedence:  # 非符号，直接进栈
                if x == 1:
                    ch = postfix.pop()
                    char = ch + char
                    postfix.append(char)
                else:
                    postfix.append(char)
                x = 1
            else:
                x = 0
                if len(stack) == 0:  # 若是运算符栈啥也没有，直接将运算符进栈
                    stack.append(char)
                else:
                    if char == "(":
                        stack.append(char)
                    elif char == ")":  # 遇到了右括号，运算符出栈到postfix中，并且将左括号出栈
                        while stack[-1] != "(":
                            postfix.append(stack.pop())
                        stack.pop()

                    elif self.operator_precedence[char] > self.operator_precedence[stack[-1]]:
                        # 只要优先级数字大，那么就继续追加
                        stack.append(char)
                    else:
                        while len(stack) != 0:
                            if stack[-1] == "(":  # 运算符栈一直出栈，直到遇到了左括号或者长度为0
                                break
                            postfix.append(stack.pop())  # 将运算符栈的运算符，依次出栈放到表达式栈里面
                        stack.append(char)  # 并且将当前符号追放到符号栈里面

        while len(stack) != 0:  # 如果符号站里面还有元素，就直接将其出栈到表达式栈里面
            postfix.append(stack.pop())
        return postfix

    def calculate(self,num1, op, num2):
        if not num1.isdigit() and not num2.isdigit():
            raise ("num error")
        else:
            num1 = int(num1)
            num2 = int(num2)
        if op == "+":
            return num1 + num2
        elif op == "-":
            return num1 - num2
        elif op == "*":
            return num1 * num2
        elif op == "/":
            if num2 == 0:
                raise ("zeros error")
            else:
                return num1 / num2
        else:
            raise ("op error")

    def returnchar(self,num1, op, num2):
        if not num1.isdigit() and not num2.isdigit():
            raise ("num error")
        if op == "+":
            return num1 + '+' + num2
        elif op == "-":
            return num1 + '-' + num2
        elif op == "*":
            if num1.find('+') >= 0 or num1.find("-") >= 0:
                num1 = '(' + num1 + ')'
            if num2.find('+') >= 0 or num2.find("-") >= 0:
                num2 = '(' + num2 + ')'
            return num1 + '×' + num2
        elif op == "/":
            if num2 == 0:
                raise ("zeros error")
            else:
                if num1.find('+') >= 0 or num1.find("-") >= 0:
                    num1 = '(' + num1 + ')'
                if num2.find('+') >= 0 or num2.find("-") >= 0:
                    num2 = '(' + num2 + ')'
                return num1 + '÷' + num2
        else:
            raise ("op error")

    def cal_expression_tree(self,postfix):
        stack = []
        x = 1
        self.getmath(postfix)
        for char in postfix:
            stack.append(char)
            if char in "+-*/":
                op = stack.pop()
                num2 = stack.pop()
                num1 = stack.pop()
                value = self.calculate(num1, op, num2)
                value = str(value)  # 计算结果是数值类型，将其化为字符串类型
                stack.append(value)
                data = []
                for s in stack:
                    data.append(s)
                for p in postfix[x:]:
                    data.append(p)
                self.getmath(data)
            x = x + 1
        return stack[0]

    def getmath(self,data):
        ch = []
        for da in data:
            ch.append(da)
            if da in "+-*/":
                op = ch.pop()
                num2 = ch.pop()
                num1 = ch.pop()
                value = self.returnchar(num1, op, num2)
                ch.append(value)
        self.answer.append(ch[0])

    def getanswer(self):
        print(self.answer)
        return self.answer


class Question(QFrame):
    def __init__(self,data):
        super(Question, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("查看答案")
        self.newlab = MyLabel("问题区")  # 放置视频
        self.devise_ui()

    def devise_ui(self):
        palette1 = QPalette()
        palette1.setColor(palette1.Background, QColor(245, 245, 245))
        self.setPalette(palette1)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        #self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                    QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                    QPushButton{background-color:rgb(170,200, 50)}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:30px;font-weight:Bold;font-family:Arial;}")
        self.answerlab.setAlignment(Qt.AlignCenter)
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600,550)
        self.answerlab.setMaximumSize(self.width1 / 2, self.height1 - 100)
        self.layout.addWidget(self.but1, 1, 2, 1, 2)
        self.layout.addWidget(self.but2, 1, 6, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 3, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 4, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.answerlab, 4, 11, 10, 10)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "请把问题放置在问题区后在操作区输入查看答案！！")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def returnfun(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Course_news(self.data))

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600,550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]
        # 将单通道图像转换为三通道RGB灰度图，因为只有三通道的backface才可以赋给三通道的src
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        #self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "请把答案放置在问题区后在操作区输入查看答案！！")

    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "查看答案").quick_ratio()
                    if (num > num1):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                        self.returnfun()
                    elif (num1 > num):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：查看答案\n\t操作成功")
                        self.contrast_answer()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        time.sleep(1)
        cv2.imwrite(imgpath, self.face1)
        self.answerjob = AnswerJob(imgpath)
        self.answerjob.updated.connect(self.right_answer)
        self.answerjob.start()

    def right_answer(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        answers = self.answerjob.getanswer()
        data = ''
        x = 0
        for answer in answers:
            if x==0:
                data =answer
            else:
                data = data + '\n='+answer
            x=1
        self.answerlab.setText(data)
        self.timer_next.start(3500)

class AddCourse(QWidget):
    def __init__(self):
        super(AddCourse, self).__init__()
        self.setWindowTitle("添加课程")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.but1 = QPushButton("关闭")
        self.but2 = QPushButton("搜索")
        self.but3 = QPushButton("加入")
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel("课程号")  # 放置视频
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1 , self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                            QPushButton{background-color:rgb(170,200, 50)}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1/2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.qtool.setMaximumSize(self.width1/2, self.height1-100)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.but1, 1, 0, 1, 2)
        self.layout.addWidget(self.but2, 1, 3, 1, 2)
        self.layout.addWidget(self.but3, 1, 6, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 11, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.qtool, 4, 11, 10, 10)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "请把课程号写在输入区后！再进行搜索！")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)


    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.chang_fun)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "请把课程号写在输入区后！再进行搜索！")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal =1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.6:
                    num = difflib.SequenceMatcher(None, nexttext[0], "关闭").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "搜索").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "加入").quick_ratio()
                    if (num > num1 and num > num2 ):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：关闭\n\t操作成功")
                        self.conclefun()
                    elif (num1 > num and num1 > num2 ):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：搜索\n\t操作成功")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：加入\n\t操作成功")
                        self.joinfun()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def conclefun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
            self.timer_next.stop()
        except:
            pass
        self.close()

    def chang_fun(self):
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        if data[1] > 0.6:
            x = 1
            try:
                da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
            except:
                da = data[0]

            self.messagelab.setText("提示!\n\t" + "本次搜索内容为：" + da)
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Course.Cno,Course.name,Controller_data.name,numble,total,filename \
                                                  from Course,Controller_data,Course_image,Teacher_Course \
                                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                                   and Teacher_Course.number=Controller_data.number and \
                                                    Course.Cno=(?)", (da,))
            self.datas = c.fetchall()
            if len(self.datas) > 0:
                self.data = self.datas[0]
                print(self.data[:4])
                self.coursewin = CourseQlist(self.data)
                self.qtool.removeItem(0)
                self.qtool.addItem(self.coursewin, '查找的课程')
                self.qtool.setStyleSheet("QToolBox{background:rgb(240,240,240);font-weight:Bold;color:rgb(0,0,0);}")
            else:
                try:
                    self.qtool.removeItem(0)
                except:
                    pass
                self.messagelab.setText("提示!\n\t" + "没有找到课程号为:'" + da + "'的信息!!!")
        if x==0:
            self.messagelab.setText("提示!\n\t" + "没有找到课程" + "的任何信息!!!")
            try:
                self.qtool.removeItem(0)
            except:
                pass
        self.timer_next.start(3500)


    def joinfun(self):
        if len(self.data)>0:
            ab = '%Y-%m-%d %H:%M:%S'
            theTime = datetime.datetime.now().strftime(ab)
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where number=(?) and Cno=(?)", (win.number, self.data[0],))
            n = len(c.fetchall())
            if n > 0:
                c.close()
                conn.close()
                self.messagelab.setText("提示!\n\t" + "您已经加入此课程了!\n\t不用重复加入!!")
            else:
                c.execute("insert into Join_Course values(?,?,?)", (win.number, self.data[0], theTime,))
                c.execute("insert into Coursetime values(?,?,?)", (win.number, self.data[0], 0.0,))
                c.execute("update Course set numble=(?) where Cno=(?)", (self.data[3] + 1, self.data[0],))
                conn.commit()
                c.close()
                conn.close()
                self.messagelab.setText("提示!\n\t" + "加入成功!!!")
        else:
            self.messagelab.setText("提示!\n\t" + "您没有搜索出任何课程，请重新搜索!!!")

class CourseWidget(QWidget):
    def __init__(self, data):
        super(CourseWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.data = data
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.numlab = QLabel("课程号:")
        self.numlab2 = QLabel(data[0])
        self.namelab = QLabel("课程名:")
        self.namelab2 = QLabel(data[1])
        self.teacherlab = QLabel("教师:")
        self.teacherlab2 = QLabel(data[2])
        self.image_path = "../datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.namelab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(200, 200)
        self.namelab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80,40)
        self.teacherlab.setMaximumSize(80,40)
        self.namelab2.setMaximumSize(200, 40)
        self.numlab2.setMaximumSize(200, 40)
        self.teacherlab2.setMaximumSize(200, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 5, 3)
        self.layout.addWidget(self.numlab, 0, 3, 1, 1)
        self.layout.addWidget(self.namelab, 1, 3, 1, 1)
        self.layout.addWidget(self.teacherlab,2,3,1,1)
        self.layout.addWidget(self.numlab2, 0, 4, 1, 3)
        self.layout.addWidget(self.namelab2, 1, 4, 1, 3)
        self.layout.addWidget(self.teacherlab2, 2, 4, 1, 3)

class CourseQlist(QListWidget):
    def __init__(self,  datas):
        super(CourseQlist, self).__init__()
        item = QListWidgetItem(self)
        item.setSizeHint(QSize(800, 200))
        item.setBackground(QColor(240, 240, 240))
        self.setItemWidget(item, CourseWidget(datas))

# 用户我的界面
class Usr_myself(QFrame):  # 增加一个编辑资料的按钮
    def __init__(self):
        super(Usr_myself, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.name = QLabel("姓名:")
        self.sex = QLabel("性别:")
        self.number = QLabel("手机号:")
        self.year = QLabel("出生年月:")
        self.school = QLabel("学校:")
        self.grade = QLabel("年级:")
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率

        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("修改密码")
        self.newlab = MyLabel3()  # 放置视频
        self.devise_ui()

    def devise_ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)

        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_date where number=(?)",(win.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.name1 = QLabel(self.data[1])  # 读取数据库中的信息，将信息输出label中
        self.sex1 = QLabel(self.data[3])
        self.number1 = QLabel(self.data[0])
        self.year1 = QLabel(self.data[2][0:4] + "年 " + self.data[2][5:] + ' 月')
        self.school1 = QLabel(self.data[4])
        self.grade1 = QLabel(self.data[5])
        self.name.setMaximumSize(70, 40)
        self.sex.setMaximumSize(70, 40)
        self.number.setMaximumSize(70, 40)
        self.school.setMaximumSize(70, 40)
        self.year.setMaximumSize(100, 40)
        self.grade.setMaximumSize(70, 40)
        self.name1.setMaximumSize(350, 40)
        self.sex1.setMaximumSize(350, 40)
        self.number1.setMaximumSize(350, 40)
        self.school1.setMaximumSize(350, 40)
        self.grade1.setMaximumSize(350, 40)
        self.year1.setMaximumSize(350, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                QPushButton{background-color:rgb(170,200, 50)}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.name1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.layout.addWidget(self.but1, 1, 0, 1, 2)
        self.layout.addWidget(self.but2, 1, 4, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 9, 3, 8)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 8)
        self.layout.addWidget(self.name, 3, 9, 1, 2)
        self.layout.addWidget(self.name1, 3, 10, 1, 6)
        self.layout.addWidget(self.year, 4, 9, 1, 2)
        self.layout.addWidget(self.year1, 4, 11, 1, 6)
        self.layout.addWidget(self.sex, 5, 9, 1, 2)
        self.layout.addWidget(self.sex1, 5, 11, 1, 6)
        self.layout.addWidget(self.number, 6, 9, 1, 2)
        self.layout.addWidget(self.number1, 6, 11, 1, 6)
        self.layout.addWidget(self.school, 7, 9, 1, 2)
        self.layout.addWidget(self.school1, 7, 11, 1, 6)
        self.layout.addWidget(self.grade, 8, 9, 1, 2)
        self.layout.addWidget(self.grade1, 8, 11, 1, 6)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "操作时，请把操作命令放置在操作框")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机与电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600,550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请把操作命令放置在操作框")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "修改密码").quick_ratio()
                    if (num > num1 and num > 0.5):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                        self.returnfun()
                    elif (num1 > 0.5 and num1 > num):
                        self.timer_next.stop()
                        self.messagelab.setText("提示!\n\t" + "本次操作为：修改密码\n\t操作成功！！")
                        self.amend_fun()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass


    def amend_fun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_amend())


    def returnfun(self):
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

# 用户修改密码
class Usr_amend(QFrame):
    def __init__(self):
        super(Usr_amend, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sign = 1
        self.passw1 = ''
        self.passw2 = ''
        self.data = []
        self.data1 = []
        self.usrlab = QLabel("账号:")
        self.amendlab1 = QLabel("原密码:")
        self.amendlab2 = QLabel("新密码:")
        self.amendedit1 = QLineEdit()
        self.amendedit2 = QLineEdit()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.but2 = QPushButton("确定")
        self.but3 = QPushButton("上一步")
        self.but4 = QPushButton("下一步")
        self.but5 = QPushButton("修改")
        self.newlab = MyLabel("输入区")  # 放置视频
        self.devise_Ui()

    def devise_Ui(self):
        self.usrlab1 = QLabel(win.number)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.usrlab.setMaximumSize(80, 40)
        self.amendlab1.setMaximumSize(80, 40)
        self.amendlab2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usrlab.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setMaximumSize(420, 40)
        self.amendedit1.setMaximumSize(420, 40)
        self.amendedit2.setMaximumSize(420, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1*2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.amendedit1.setPlaceholderText("请在输入区输入原密码")
        self.amendedit2.setPlaceholderText("请在输入区输入新密码")
        self.amendedit1.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.amendedit2.setFont(QFont("宋体", 16))
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                QPushButton{background-color:rgb(170,200, 50)}")
        self.but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                        QPushButton{background-color:rgb(170,200, 50)}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.layout.addWidget(self.but1, 0, 0, 1, 2)
        self.layout.addWidget(self.but2, 0, 3, 1, 2)
        self.layout.addWidget(self.but3, 0, 6, 1, 2)
        self.layout.addWidget(self.but4, 3, 0, 1, 2)
        self.layout.addWidget(self.but5, 3, 3, 1, 2)
        self.layout.addWidget(self.messagelab, 0, 10, 3, 7)
        self.layout.addWidget(self.progresslab, 4, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 3, 1, 6)
        self.layout.addWidget(self.newlab, 5, 0, 6, 9)
        self.layout.addWidget(self.usrlab, 5, 9, 1, 1)
        self.layout.addWidget(self.usrlab1, 5, 10, 1, 7)
        self.layout.addWidget(self.amendlab1, 7, 9, 1, 1)
        self.layout.addWidget(self.amendedit1, 7, 10, 1, 7)
        self.layout.addWidget(self.amendlab2, 9, 9, 1, 1)
        self.layout.addWidget(self.amendedit2, 9, 10, 1, 7)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入确定！")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal  = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face1 = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象
        self.face = show[self.newlab.y2:self.newlab.y3, self.newlab.x2:self.newlab.x3]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    def contrast_answer_right(self):
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.amendedit1.setText(self.passw)
                self.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                        "如果输入错误请您在操作区输入上一步操作！\n\t输入完整后可输入下一步")
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.amendedit1.setText(self.passw)
                self.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                        "如果输入错误请您在操作区输入上一步操作!\n\t输入完整后可输入登录")
        time.sleep(3)
        self.timer_next.start(3500)

    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "../datas/wen/test1.jpg"
        self.setextlab.setText("正在识别输入中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        cv2.imwrite(imgpath, self.face1)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入确定！")


    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.getanswer()
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    num1 = difflib.SequenceMatcher(None, nexttext[0], "确定").quick_ratio()
                    num2 = difflib.SequenceMatcher(None, nexttext[0], "上一步").quick_ratio()
                    num3 = difflib.SequenceMatcher(None, nexttext[0], "下一步").quick_ratio()
                    num4 = difflib.SequenceMatcher(None, nexttext[0], "修改").quick_ratio()
                    if (num > num1 and num > num2 and num > num3 and num>num4):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                        self.return_fun()
                    elif (num1 > num and num1 > num2 and num1 > num3 and num1>num4):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                        self.contrast_answer()
                    elif (num2 > num1 and num2 > num and num2 > num3 and num2>num4):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                        sign = self.sign
                        if sign == 1:
                            if len(self.data) > 0:
                                self.passw1 = self.data[-1]
                                self.amendedit1.setText(self.passw1)
                                self.data = self.data[:-1]
                            else:
                                self.passw1 = ''
                                self.amendedit1.setText(self.passw1)
                                self.data = []
                            self.messagelab.setText("提示!\n\t" +
                                                    "请把原密码分段输入输入区后，再在操作区输入确定！！")
                        elif sign == 2:
                            if len(self.data1) > 0:
                                self.passw2 = self.data1[-1]
                                self.amendedit2.setText(self.passw2)
                                self.data1 = self.data1[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请把新密码分段输入输入区后，再在操作区输入确定！！")
                            else:
                                self.passw2 = ''
                                self.amendedit2.setText(self.passw2)
                                self.data1 = []
                                self.sign = 1
                                self.passw1 = self.data[-1]
                                self.amendedit1.setText(self.passw1)
                                self.data = self.data[:-1]
                                self.messagelab.setText("提示!\n\t" +
                                                        "请把原密码分段输入输入区后，再在操作区输入确定！！")
                    elif (num3 > num1 and num3 > num and num3 > num2 and num3>num4):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：下一步\n\t操作成功")
                        sign = self.sign
                        if sign==1:
                            self.sign = 2
                        elif sign == 2:
                            self.accept()
                    elif (num4 > num1 and num4 > num and num4 > num2 and num4>num3):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：修改\n\t操作成功")
                        self.accept()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def return_fun(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_myself())


    def accept(self):
        if len(self.amendedit1.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "原密码没有填写")
        elif len(self.amendedit2.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif len(self.amendedit3.text()) == 0:
            self.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif self.amendedit3.text() != self.amendedit2.text():
            self.messagelab.setText("提示!\n\t" +"前后密码输入不一样！")
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            sign = 0
            for variate in c.fetchall():
                if variate[0] == win.number and variate[2] == self.amendedit1.text():
                    conn.execute("update User set password=(?) where number=(?)", (self.amendedit2.text(), variate[0],))
                    conn.commit()
                    sign = 1
                    break
            c.close()
            conn.close()
            if sign == 0:
                self.messagelab.setText("提示!\n\t" + "原密码输入错误！！")
                self.sign = 1
            else:
                self.messagelab.setText("提示!\n\t" + "修改成功！！")
                try:
                    self.timer_next.stop()
                    self.timer_camera.stop()
                    self_cap.release()  # 释放视频流
                    self.newlab.clear()
                except:
                    pass
                time.sleep(1)
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Usr_myself())

# 用户学习报告的界面
class Usr_report(QFrame):
    def __init__(self):
        super(Usr_report, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.day = QLabel("学习天数:")
        self.learntime = QLabel("学习总时长:")
        self.avglearn = QLabel("日均学习:")
        self.table = QTableWidget()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.but1 = QPushButton("返回")
        self.newlab = MyLabel2()  # 放置视频
        self.devise_Ui()
        self.information()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);} \
                                                        QPushButton{background-color:rgb(170,200, 50)}")
        self.day.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learntime.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1, 90)
        self.newlab.setMaximumSize(400,450)
        self.day.setMaximumSize(120, 40)
        self.learntime.setMaximumSize(130, 40)
        self.avglearn.setMaximumSize(120, 40)
        self.layout.addWidget(self.day, 1, 7, 1, 1)
        self.layout.addWidget(self.learntime, 1, 10, 1, 1)
        self.layout.addWidget(self.avglearn, 1, 13, 1, 1)
        self.layout.addWidget(self.but1,0,1,1,2)
        self.layout.addWidget(self.messagelab, 1, 0, 2, 5)
        self.layout.addWidget(self.progresslab, 3, 0, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 1, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 5, 5)
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.next_step)
        self.messagelab.setText("提示！\n\t"+"操作时，请您把操作输入操作区!")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.equal = 0
                time.sleep(2)
                self.timer_next.start(3500)

    def information(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)", (win.number,))
        self.data1 = c.fetchall()[0]
        c.close()
        conn.close()
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(self.data1[1], abcd)
        a = (new - a1).days + 1
        self.join = QLabel("已加入" + str(a) + "天")
        self.day1 = QLabel(str(self.data1[2]) + "天")
        ab = self.data1[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.learntime1 = QLabel(ac)
        ad = ab / self.data1[2]
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.avglearn1 = QLabel(ae)
        self.join.setStyleSheet("QLabel{color:rgb(0,200,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.day1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.learntime1.setStyleSheet(
            "QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.table.setStyleSheet("QTableWidget{background-color:rgb(255,255,255);font:13pt '宋体';font-weight:Bold;};");
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        sqlpath = "../datas/database/SQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_data")
        data = c.fetchall()
        if len(data)>15:
            data = data[-15:]
            self.table.setRowCount(15)
        else:
            b = len(data)
            self.table.setRowCount(b)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['开始学习时间', '文件类型', '文件名', '结束时间', '学习时长'])
        i = 0
        for variate in data:
            self.table.setItem(i, 0, QTableWidgetItem(variate[0]))
            self.table.setItem(i, 1, QTableWidgetItem(variate[2]))
            self.table.setItem(i, 2, QTableWidgetItem(variate[3]))
            self.table.setItem(i, 3, QTableWidgetItem(variate[4]))
            min = (datetime.datetime.strptime(variate[4], abcd) - datetime.datetime.strptime(variate[0], abcd)).seconds
            if (min / 3600) > 1:
                ac = str(int(min / 3600)) + '时' + str(round((min / 3600 - int(min / 3600)) * 60, 2)) + "分"
            else:
                ac = str(round(min / 60, 2)) + "分"
            self.table.setItem(i, 4, QTableWidgetItem(ac))
            i += 1
        self.join.setMaximumSize(300, 40)
        self.day1.setMaximumSize(150, 40)
        self.learntime1.setMaximumSize(150, 40)
        self.avglearn1.setMaximumSize(150, 40)
        self.layout.addWidget(self.day1, 1, 8, 1, 1)
        self.layout.addWidget(self.join, 1, 5, 1, 1)
        self.layout.addWidget(self.learntime1, 1, 11, 1, 1)
        self.layout.addWidget(self.avglearn1, 1, 14, 1, 1)
        self.layout.addWidget(self.table, 3,5,7, 15)

    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (400,450))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)
        self.face = show[self.newlab.y0:self.newlab.y1, self.newlab.x0:self.newlab.x1]
        # 选择self.newlab.y0:self.newlab.y1行、self.newlab.x0:self.newlab.x1列区域作为截取对象

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                 QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def next_step(self):
        imgpath = "../datas/wen/test.jpg"
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath, self.face)
        self.nextstepjob = NextStepJob(self.equal, imgpath, imgpath2)
        self.nextstepjob.updated.connect(self.next_step_fun)
        self.nextstepjob.updated2.connect(self.opmovie)
        self.nextstepjob.updated3.connect(self.opentext)
        self.nextstepjob.start()

    def opentext(self):
        self.messagelab.setText("提示!\n\t" + "操作时，请您把操作输入操作区!")

    def opmovie(self):
        imgpath2 = "../datas/wen/lasttest.jpg"
        cv2.imwrite(imgpath2, self.face)
        self.progresslab.clear()
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()

    def next_step_fun(self):
        self.equal = 1
        self.movie.stop()
        self.progresslab.clear()
        self.progresslab.setPixmap(QPixmap("../datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        nexttext = self.nextstepjob.answer
        try:
            if nexttext[0] != '':
                if nexttext[1] > 0.4:
                    num = difflib.SequenceMatcher(None, nexttext[0], "返回").quick_ratio()
                    if (num > 0.5):
                        self.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                        self.returnfun()
                    else:
                        self.messagelab.setText("提示!\n\t" + "本次识别的操作为" + nexttext[0] +
                                                "\n\t该页面没有该操作，请您重新操作！！")
                else:
                    self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                            "\n\t请您把操作放置在操作区识别！！")
            else:
                self.messagelab.setText("抱歉!\n\t" + "没有识别出有效操作" +
                                        "\n\t请您把操作放置在操作区识别！！")
        except:
            time.sleep(2)
            pass

    def returnfun(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())


def found_sql():
    filepath = '../datas/database'
    if (not (os.path.exists(filepath))):  # 创建文件夹。
        os.makedirs(filepath)
    filepath = '../datas/tupian'
    if (not (os.path.exists(filepath))):  # 创建文件夹。
        os.makedirs(filepath)
    filepath = '../datas/wen'
    if (not (os.path.exists(filepath))):  # 创建文件夹。
        os.makedirs(filepath)
    sqlpath = '../datas/database/Information.db'
    conn = sqlite3.connect(sqlpath)
    c = conn.cursor()
    try:  # 超级管理员账号密码表     号码            用户名                  密码
        c.execute('''CREATE TABLE SuperController(number text,usrname text,password text)''')
    except:
        pass
    try:  # 管理员账号密码表    号码            用户名                  密码
        c.execute('''CREATE TABLE Controller(number text,usrname text,password text)''')
    except:
        pass
    try:  # 管理员信息表         号码        姓名        出生年月       性别        学校
        c.execute('''CREATE TABLE Controller_data(number text,name text,birthday text,sex text,school text)''')
    except:
        pass
    try:  # 管理员头像表        号码             头像        文件后缀
        c.execute('''CREATE TABLE Controller_image(number text,total LONGBLOB,filename text)''')
    except:
        pass

    try:  # 管理员账号密码表    号码            用户名                  密码
        c.execute('''CREATE TABLE Controller2(number text,usrname text,password text)''')
    except:
        pass
    try:  # 管理员信息表         号码        姓名        出生年月       性别        学校
        c.execute('''CREATE TABLE Controller_data2(number text,name text,birthday text,sex text,school text)''')
    except:
        pass
    try:  # 管理员头像表        号码             头像        文件后缀
        c.execute('''CREATE TABLE Controller_image2(number text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 用户账号密码表     号码            用户名                  密码
        c.execute('''CREATE TABLE User(number text,usrname text,password text)''')
    except:
        pass
    try:  # 用户头像表          号码              头像              文件后缀
        c.execute('''CREATE TABLE User_image(number text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 用户信息表   号码        姓名       出生年月        性别         学校                     年级
        c.execute('''CREATE TABLE User_date(number text,name text,birthday text,sex text,school text, grade text)''')
    except:
        pass
    try:  # 用户学习表     号码          注册时间    已注册天数       学习总时间                上一次登录时间
        c.execute('''CREATE TABLE Student_date(number text,time text,logonday int,stude_day double,lasttime text)''')
    except:
        pass
    try:                        # 课程学习表   号码　　　　 课程码     　学习时间
        c.execute('''CREATE TABLE Coursetime(number text,Cno text,time double)''')
    except:
        pass
    try:                  # 课程表   课程码        课程名         人数
        c.execute('''CREATE TABLE Course(Cno text,name text,numble int)''')
    except:
        pass
    try:  # 课程头像表     课程码              图片                           文件后缀
        c.execute('''CREATE TABLE Course_image(Cno text,total LONGBLOB,filename text )''')
    except:
        pass
    try:  # 教师课程表      号码                       课程码
        c.execute('''CREATE TABLE Teacher_Course(number text, Cno text)''')
    except:
        pass
    try:  # 加课表       号码                   课程码                加入时间
        c.execute('''CREATE TABLE Join_Course(number text, Cno text, jointime text)''')
    except:
        pass
    c.close()
    conn.close()
    sqlpath = "../datas/database/Data.db"
    conn = sqlite3.connect(sqlpath)
    c = conn.cursor()
    try:  # 一年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE First_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 一年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE First_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 一年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE First_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 二年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Second_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 二年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Second_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 二年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Second_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 三年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Three_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 三年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Three_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 三年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Three_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 四年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Fourth_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 四年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Fourth_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 四年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Fourth_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 五年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Fifth_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 五年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Fifth_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 五年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Fifth_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 六年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Six_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 六年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Six_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 六年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Six_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 七年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Seven_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 七年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Seven_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 七年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Seven_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 八年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Eight_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 八年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Eight_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 八年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Eight_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass
    try:  # 九年级文件信息表  序号，      学习阶段              年级，      科目                 文件名          文件格式
        c.execute('''CREATE TABLE Nine_Grade(no text,level1 text,level2 text,level3 text,name text,filename text)''')
    except:
        pass
    try:  # 九年级文件数据表     序号，文件内容
        c.execute('''CREATE TABLE Nine_Grade_data(no text,total LONGBLOB)''')
    except:
        pass
    try:  # 九年级文件图片数据表     序号，文件内容
        c.execute('''CREATE TABLE Nine_Grade_image(no text,total LONGBLOB,filename text)''')
    except:
        pass

    # 高中的数据库再设计
    try:  # 网址，  网址内容字节
        c.execute('''CREATE TABLE successfulurl(url text,howbyte integer)''')
    except:
        pass
    c.close()
    conn.close()



#主函数
if __name__ == "__main__":
    found_sql()
    app = QApplication(sys.argv)
    win = QUnFrameWindow()
    win.show()
    sys.exit(app.exec_())
