"""
作者：钟培望
名称：具体人工智能沉浸式学习系统超级管理员端
时间：2020.4.30
"""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from captcha.image import ImageCaptcha
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import os, sys, time, re
import glob
import random
import base64
import datetime
from bs4 import BeautifulSoup
import fitz
import sqlite3
import requests
import zipfile
import shutil
import subprocess



class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """
    def __init__(self):  # 设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None)  # 设置为顶级窗口
        self.setWindowTitle("low_Super_Administrator")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.setMinimumWidth(670)
        self.setMinimumHeight(560)
        self.resize(self.x, self.y)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.bar = self.menuBar()
        file = self.bar.addMenu("文件")
        logonquit = QAction("退出登录", self)
        file.addAction(logonquit)
        quit = QAction("退出", self)
        file.addAction(quit)
        logonquit.triggered.connect(self.logonquit_fun)
        quit.triggered.connect(self.close_win)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.splitter.addWidget(Record())
        #self.splitter.addWidget(Function())

    def close_win(self):
        rely = QMessageBox.question(self, "提示!", "是否退出程序？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if rely == 65536:
            return
        self.close()
        sys.exit()

    def logonquit_fun(self):
        rely = QMessageBox.question(self, "提示!", "是否退出登录？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if rely == 65536:
            return
        self.splitter.widget(0).setParent(None)
        self.splitter.addWidget(Record())

#注册
class Logon(QFrame):
    def __init__(self):
        super(Logon, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.password2 = QLabel("确认密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        self.password2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.codeLineEdit.setMaximumSize(310, 40)
        # self.usrLineEdit2.setText(a)
        self.usrLine.setPlaceholderText("请输入手机号码")
        self.usrnameLine.setPlaceholderText("请输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请输入密码")
        self.pwdLineEdit2.setPlaceholderText("请重新输入密码")
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.codeLineEdit.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLine.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.usrnameLine.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit1.returnPressed.connect(self.enterPress3)
        self.pwdLineEdit2.returnPressed.connect(self.enterPress4)
        self.returnBtn.clicked.connect(self.change_record)  # 点击返回键连接管理员登录界面
        self.okBtn.clicked.connect(self.accept)
        self.change_code.linkActivated.connect(self.renovate_code)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLine, 1, 5, 1, 14)
        self.layout.addWidget(self.usrname, 2, 3, 1, 1)
        self.layout.addWidget(self.usrnameLine, 2, 5, 1, 14)
        self.layout.addWidget(self.password1, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 3, 5, 1, 14)
        self.layout.addWidget(self.password2, 4, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 4, 5, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 5, 5, 1, 5)
        self.layout.addWidget(self.codebel, 5, 10, 1, 6)
        self.layout.addWidget(self.change_code, 5, 12, 1, 1)
        self.layout.addWidget(self.okBtn, 6, 5, 1, 14)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("../datas/wen/code.png")
        self.codebel.setPixmap(QPixmap("../datas/wen/code.png"))
        self.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 注册时输入的号码检验是否已经注册过的
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
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
        conn.execute("INSERT INTO SuperController VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    def enterPress1(self):  # 注册-》用户框回车确定时判断文字框是否有输入
        if (len(self.usrLine.text()) == 0):
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif (len(self.usrLine.text()) != 11):
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您登录！")
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Record())
        else:
            self.usrnameLine.setFocus()

    def enterPress2(self):  # 注册-》用户名框回车确定时判断文字框是否有输入
        if (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        else:
            self.pwdLineEdit1.setFocus()

    def enterPress3(self):  # 注册-》密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit1.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        else:
            self.pwdLineEdit2.setFocus()

    def enterPress4(self):  # 注册-》确认密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit2.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif (self.pwdLineEdit1.text() != self.pwdLineEdit2.text()):
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        else:
            self.codeLineEdit.setFocus()

    def accept(self):  # 注册时将账号密码保存并登录。
        if len(self.usrLine.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif len(self.usrLine.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您登录！")
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Record())
        elif (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        elif len(self.pwdLineEdit1.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        elif len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "确认密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif self.pwdLineEdit1.text() != self.pwdLineEdit2.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.codeLineEdit.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.codeLineEdit.setText("")
            self.codeLineEdit.setFocus()
        else:
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Function())
            # 连接主窗口界面。

    def change_record(self):  # 连接用户登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Record())

#登录
class Record(QFrame):  # 用户登录界面
    def __init__(self):
        super(Record, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr = QLabel("用户:")
        self.password = QLabel("密码:")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("登录")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.forgetbtn = QLabel()
        self.logonbtn = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.password.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.password.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrLineEdit.setPlaceholderText("请输入手机号码")
        self.usrLineEdit.setMaximumSize(420, 40)
        self.usrLineEdit.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(420, 40)
        self.pwdLineEdit.setPlaceholderText("请输入密码")
        self.pwdLineEdit.setFont(QFont("宋体", 16))
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.codeLineEdit.setFont(QFont("宋体", 16))
        self.codeLineEdit.setMaximumSize(310, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.codebel.setMaximumSize(100, 40)
        self.forgetbtn.setText("<A href='www.baidu.com'>忘记密码</a>")
        self.logonbtn.setText("<A href='www.baidu.com'>注册</a>")
        self.forgetbtn.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.logonbtn.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.forgetbtn.setMaximumSize(90, 50)
        self.logonbtn.setMaximumSize(50, 50)

        self.okBtn.clicked.connect(self.accept)
        self.forgetbtn.linkActivated.connect(self.forgetfun)  # 连接管理员忘记密码界面
        self.logonbtn.linkActivated.connect(self.logonfun)  # 连接管理员注册界面
        self.usrLineEdit.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.pwdLineEdit.returnPressed.connect(self.enterPress2)
        self.change_code.linkActivated.connect(self.renovate_code)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 1, 4, 1, 14)
        self.layout.addWidget(self.password, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 2, 4, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 3, 4, 1, 5)
        self.layout.addWidget(self.codebel, 3, 9, 1, 6)
        self.layout.addWidget(self.change_code, 3, 11, 1, 1)
        self.layout.addWidget(self.okBtn, 4, 4, 1, 14)
        self.layout.addWidget(self.forgetbtn, 5, 4, 1, 2)
        self.layout.addWidget(self.logonbtn, 5, 10, 1, 2)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("../datas/wen/code.png")
        self.codebel.setPixmap(QPixmap("../datas/wen/code.png"))
        self.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 登录时检验号码是否没有注册
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    def enterPress1(self):  # 登录回车确定时判断文字框是否有输入
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
        else:
            self.pwdLineEdit.setFocus()

    def enterPress2(self):  # 登录回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit.setFocus()
        else:
            self.codeLineEdit.setFocus()

    def accept(self):  # 登录时判断密码是否正确
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
        elif len(self.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit.setFocus()
        elif self.code.lower() != self.codeLineEdit.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.codeLineEdit.setText("")
            self.codeLineEdit.setFocus()
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from SuperController")
            d = 0
            for variate in c.fetchall():
                if variate[0] == self.usrLineEdit.text() and variate[2] == self.pwdLineEdit.text():
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:  # 连接主界面函数
                win.number = self.usrLineEdit.text()
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Function())
            else:
                QMessageBox.about(self, "提示!", "账号或密码输入错误")

    def forgetfun(self):  # 连接超级管理员忘记密码界面
        win.splitter.widget(0).setParent(None)
        Forget().renovate_code()
        win.splitter.insertWidget(0, Forget())

    def logonfun(self):  # 连接超级管理员注册界面
        win.splitter.widget(0).setParent(None)
        Logon().renovate_code()
        win.splitter.insertWidget(0, Logon())

# 忘记密码
class Forget(QFrame):
    def __init__(self):
        super(Forget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.usr2 = QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.pwd3 = QLabel("确认密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.pwdLineEdit3 = QLineEdit()
        self.codeLineEdit1 = QLineEdit()
        self.okBtn1 = QPushButton("确认")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        self.pwd3.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd3.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit3.setMaximumSize(420, 40)
        self.codeLineEdit1.setMaximumSize(310, 40)
        self.usrLineEdit2.setPlaceholderText("请输入手机号码")
        self.pwdLineEdit2.setPlaceholderText("请输入新的密码")
        self.pwdLineEdit3.setPlaceholderText("请重新输入新的密码")
        self.codeLineEdit1.setPlaceholderText("请输入右侧的验证码")
        self.usrLineEdit2.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.pwdLineEdit3.setFont(QFont("宋体", 12))
        self.codeLineEdit1.setFont(QFont("宋体", 12))
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit3.setEchoMode(QLineEdit.Password)
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn1.setMaximumSize(420, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.okBtn1.clicked.connect(self.accept)
        self.usrLineEdit2.returnPressed.connect(self.enterPress1)  # 用户输入框按回车判断
        self.pwdLineEdit2.returnPressed.connect(self.enterPress2)  # 密码输入框按回车判断
        self.pwdLineEdit3.returnPressed.connect(self.enterPress3)  # 确认密码输入框回车判断
        self.returnBtn.clicked.connect(self.return_record)
        self.change_code.linkActivated.connect(self.renovate_code)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr2, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 1, 5, 1, 14)
        self.layout.addWidget(self.pwd2, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 2, 5, 1, 14)
        self.layout.addWidget(self.pwd3, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit3, 3, 5, 1, 14)
        self.layout.addWidget(self.codeLineEdit1, 4, 5, 1, 5)
        self.layout.addWidget(self.codebel, 4, 10, 1, 6)
        self.layout.addWidget(self.okBtn1, 5, 5, 1, 14)
        self.renovate_code()

    def return_record(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Record())

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("../datas/wen/code.png")
        self.codebel.setPixmap(QPixmap("../datas/wen/code.png"))
        self.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 忘记密码时检验号码是否没有注册
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
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
        c.execute("select * from SuperController")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit2.text():
                win.number = variate[0]
                conn.execute("update SuperController set password=(?) where number=(?)", (self.pwdLineEdit2.text(), variate[0],))
                break
        conn.commit()
        c.close()
        conn.close()

    def enterPress1(self):  # 忘记密码时回车确定时判断文字框是否有输入
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Logon())
        else:
            self.pwdLineEdit2.setFocus()

    def enterPress2(self):  # 忘记密码-》密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit2.setFocus()
        else:
            self.pwdLineEdit3.setFocus()

    def enterPress3(self):  # 忘记密码-》确认密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit3.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        else:
            self.codeLineEdit1.setFocus()

    def accept(self):  # 忘记密码时验证是否可以登录
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLineEdit2.setFocus()
        elif len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif len(self.pwdLineEdit3.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.codeLineEdit1.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.codeLineEdit1.setText("")
            self.codeLineEdit1.setFocus()
        else:
            self.savedate()
            # 设置一个查询用户年级的函数
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Function())

            # 连接主窗口界面。




class Function(QFrame):  # 超级管理员功能界面
    def __init__(self):
        super(Function, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainbutton1 = QPushButton("管理信息")  # 用户功能界面的控件
        self.mainbutton2 = QPushButton("爬虫")
        self.mainbutton3 = QPushButton("添加资料")
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b = self.screenRect.height() * 1.0 / 4
        a = self.screenRect.width() * 1.0 / 5

        self.mainbutton1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")

        self.mainbutton1.clicked.connect(self.select_fun1)
        self.mainbutton2.clicked.connect(self.select_fun2)
        self.mainbutton3.clicked.connect(self.select_fun3)
        self.layout.addWidget(self.mainbutton1, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.mainbutton2, 0, 1)
        self.layout.addWidget(self.mainbutton3, 0, 2)

        self.mainbutton1.setMaximumSize(a, b)
        self.mainbutton2.setMaximumSize(a, b)
        self.mainbutton3.setMaximumSize(a, b)

    def select_fun1(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,Controller_news())

    def select_fun2(self):  # 连接爬虫
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Reptile())

    def select_fun3(self):  # 连接添加资料
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Addfile())


class Controller_news(QFrame):
    def __init__(self):
        super(Controller_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnbut = QPushButton("返回")
        self.addusr = QPushButton("添加用户")
        self.addcontroller = QPushButton("添加管理员")
        self.seeapply = QPushButton("查看申请")
        self.editbut = QPushButton("编辑")
        self.deletebut = QPushButton("删除")
        self.selectbox = QComboBox()
        self.query = QLineEdit()
        self.searchbut = QPushButton("搜索")
        self.table = QTableWidget()
        self.data = []
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
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

        self.table.setStyleSheet("QTableWidget{background-color:rgb(235,235,235);font:13pt '宋体';font-weight:Bold;};")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不能编辑table
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addusr.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addcontroller.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.seeapply.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.editbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.deletebut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.searchbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.query.setPlaceholderText("请输入搜索内容")
        self.query.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.selectbox.addItems(['号码', '姓名','学校'])
        self.selectbox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.editbut.setMaximumSize(100,40)
        self.deletebut.setMaximumSize(100,40)
        self.selectbox.setMaximumSize(100,40)
        self.query.setMaximumSize(240,40)
        self.searchbut.setMaximumSize(100,40)
        self.returnbut.clicked.connect(self.returnfun)
        self.addusr.clicked.connect(self.addusrfun)
        self.addcontroller.clicked.connect(self.addcontrollerfun)
        self.seeapply.clicked.connect(self.seeapplyfun)
        self.editbut.clicked.connect(self.edit_fun)
        self.searchbut.clicked.connect(self.searchfun)
        self.deletebut.clicked.connect(self.deletedata)
        self.win_layout1.addWidget(self.returnbut, 1, 0, 2, 2)
        self.win_layout1.addWidget(self.addusr, 3, 0, 2, 2)
        self.win_layout1.addWidget(self.addcontroller, 5, 0, 2, 2)
        self.win_layout1.addWidget(self.seeapply, 7, 0, 2, 2)
        self.win_layout2.addWidget(self.editbut,1,1,1,2)
        self.win_layout2.addWidget(self.deletebut,1,7,1,2)
        self.win_layout2.addWidget(self.selectbox,1,12,1,2)
        self.win_layout2.addWidget(self.query,1,14,1,4)
        self.win_layout2.addWidget(self.searchbut,1,18,1,2)
        self.win_layout2.addWidget(self.table,2,0,18,20)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def addusrfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_Logon())

    def addcontrollerfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_Logon())

    def seeapplyfun(self):
        self.table.close()
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window = CourseQlist()
        self.qtool.addItem(self.window, "管理员申请注册")
        self.win_layout2.addWidget(self.qtool, 2, 0, 18, 20)
        self.qtool.show()

    def edit_fun(self):
        n =0
        for data in self.data:
            if data[0].isChecked():
                n+=1
        if n != 1:
            QMessageBox.about(self, "提示!", "抱歉，该功能只能选择一个用户进行编辑！！" )
            return
        for data in self.data:
            if data[0].isChecked():
                if data[2]=="用户":
                    win.splitter.widget(0).setParent(None)
                    win.splitter.insertWidget(0, Edit_usr(data[1]))
                elif data[2] == "管理员":
                    win.splitter.widget(0).setParent(None)
                    win.splitter.insertWidget(0, Edit_Controller(data[1]))


    def searchfun(self):
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['选择', '用户', '姓名', '出生年月', '性别', '学校', '身份'])
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        d = self.query.text()
        if (d ==''):
            QMessageBox.about(self, "提示!", "搜索内容不能为空！！！")
            return
        elif (self.selectbox.currentText() == '姓名'):
            c.execute("select * from User_date where name = (?)", (d, ))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where name =(?) ",(d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b+c)>0:
                self.table.setRowCount(b+c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],"用户"])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.table.item(i, 2).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.table.item(i, 2).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有查到任何信息" )
        elif (self.selectbox.currentText() == '号码'):
            c.execute("select * from User_date where number = (?)", (d,))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where number =(?) ", (d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b + c) > 0:
                self.table.setRowCount(b + c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'用户'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.table.item(i, 1).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.table.item(i, 1).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有该用户的任何信息" )
        elif (self.selectbox.currentText() == '学校'):
            c.execute("select * from User_date where school = (?)", (d,))
            data1 = c.fetchall()
            c.execute("select * from Controller_data where school =(?) ", (d,))
            data2 = c.fetchall()
            c.close()
            conn.close()
            b = len(data1)
            c = len(data2)
            i = 0
            if (b + c) > 0:
                self.table.setRowCount(b + c)
                if b > 0:
                    for variate in data1:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'用户'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("用户"))
                        self.table.item(i, 5).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
                if c > 0:
                    for variate in data2:
                        ck = QCheckBox()
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        self.table.setCellWidget(i, 0, w)
                        self.data.append([ck, variate[0],'管理员'])
                        for j in range(5):
                            itemContent = variate[j]
                            self.table.setItem(i, j + 1, QTableWidgetItem(itemContent))
                        self.table.setItem(i, 6, QTableWidgetItem("管理员"))
                        self.table.item(i, 5).setForeground(QBrush(QColor(255, 0, 0)))
                        i = i + 1
            else:
                QMessageBox.about(self, "提示!","没有该用户的任何信息" )
        try:
            self.qtool.close()
            self.qtool.deleteLater()
        except:
            pass
        self.query.setText("")
        self.win_layout2.addWidget(self.table, 2, 0, 18, 20)
        self.table.show()

    def deletedata(self):
        n = 0
        for data in self.data:
            if data[0].isChecked():
                n += 1
        if n == 0:
            QMessageBox.about(self, "提示!", "您没有选择任何用户，请您重新选择！！")
            return
        rely = QMessageBox.question(self, "提示!", "该操作会造成数据无法恢复！！！\n确定删除？？？" , QMessageBox.Yes|QMessageBox.No ,QMessageBox.Yes)
        if rely ==  65536:
            return
        removeline =[]
        for data in self.data:
            if data[0].isChecked():
                row = self.table.rowCount()
                for x in range(row, 0, -1):
                    if data[1] == self.table.item(x ,1).text():
                        self.table.removeRow(x)
                        removeline.append(data)
        if len(removeline)>0:
            for line in removeline:
                self.data.remove(line)
        sqlpath ='../datas/database/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        for line in removeline:
            if line[2]=="用户":
                c.execute("delete from User where number = (?)", (line[1],))
                c.execute("delete from User_image where number = (?)", (line[1],))
                c.execute("delete from User_date where number = (?)", (line[1],))
                c.execute("delete from Student_date where number = (?)", (line[1],))
            elif line[2]=="管理员":
                c.execute("delete from Controller where number = (?)", (line[1],))
                c.execute("delete from Controller_data where number = (?)", (line[1],))
                c.execute("delete from Controller_image where number = (?)", (line[1],))
        conn.commit()
        c.close()
        conn.close()

# 编辑管理员信息
class Edit_Controller(QFrame):
    def __init__(self,number):
        super(Edit_Controller, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.sure = QPushButton("确认")
        self.amend = QPushButton("修改用户密码")
        self.returnBtn = QPushButton("返回")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.devise_ui()

    def devise_ui(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)", (self.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        yearnb = []
        for i in range(1980, 2020):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))

        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(255,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")

        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:26px;color:rgb(0,0,0);}")

        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.school.setMaximumSize(50, 40)
        self.returnBtn.setMaximumSize(60, 40)
        self.amend.setMaximumSize(190, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)

        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)

        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.yearcb.addItems(yearnb)
        self.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.monthcb.addItems(monthmb)
        self.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.nameEdit.setText(self.data[1])
        self.schoolEiit.setText(self.data[4])
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.amend, 0, 10, 1, 1)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 4, 1, 18)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 4, 1, 18)
        self.layout.addWidget(self.year, 3, 3, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 4, 1, 8)
        self.layout.addWidget(self.monthcb, 3, 10, 1, 7)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 4, 1, 18)
        self.layout.addWidget(self.sure, 6, 4, 1, 18)
        self.sure.clicked.connect(self.connect_fun)
        self.returnBtn.clicked.connect(self.return_fun)
        self.amend.clicked.connect(self.connect_fun1)

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_news())

    def save_data(self):
        a = self.nameEdit.text()
        b = self.yearcb.currentText() + '-' + self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("update User_data set name =(?),birthday=(?),sex=(?),school=(?) where number=(?)",
                     (a, b, c, d,self.number))
        conn.commit()
        conn.close()

    def connect_fun(self):
        win.splitter.widget(0).setParent(None)
        self.save_data()
        Controller_news().devise_ui()
        win.splitter.insertWidget(0, Controller_news())

    def connect_fun1(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, chang_Controller_amend(self.number))

# 修改管理员密码
class chang_Controller_amend(QFrame):
    def __init__(self,number):
        super(chang_Controller_amend, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.usrlab = QLabel("账号:")
        self.amendlab1 = QLabel("原密码:")
        self.amendlab2 = QLabel("新密码:")
        self.amendlab3 = QLabel("确认密码:")
        self.amendedit1 = QLineEdit()
        self.amendedit2 = QLineEdit()
        self.amendedit3 = QLineEdit()
        self.sure = QPushButton("确认修改")
        self.returnBtn = QPushButton("返回")
        self.devise_ui()

    def devise_ui(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller where number=(?)", (self.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.usrlab1 = QLabel(self.number)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(350, 0, 0, 0)
        self.usrlab.setMaximumSize(80, 40)
        self.amendlab1.setMaximumSize(80, 40)
        self.amendlab2.setMaximumSize(80, 40)
        self.amendlab3.setMaximumSize(100, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usrlab.setStyleSheet(
            "QLabel{color:rgb(100,100,100,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setStyleSheet(
            "QLabel{color:rgb(100,100,100,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab3.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setMaximumSize(420, 40)
        self.amendedit1.setMaximumSize(420, 40)
        self.amendedit2.setMaximumSize(420, 40)
        self.amendedit3.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.amendedit1.setText(self.data[2])
        self.amendedit2.setPlaceholderText("请输入新密码")
        self.amendedit3.setPlaceholderText("请重新输入密码")
        self.amendedit1.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.amendedit2.setFont(QFont("宋体", 16))
        self.amendedit3.setFont(QFont("宋体", 16))
        self.amendedit1.setEchoMode(QLineEdit.Password)
        self.amendedit2.setEchoMode(QLineEdit.Password)
        self.amendedit3.setEchoMode(QLineEdit.Password)
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.returnBtn.clicked.connect(self.return_fun)
        self.amendedit2.returnPressed.connect(self.enterPress2)
        self.amendedit3.returnPressed.connect(self.accept)
        self.sure.clicked.connect(self.accept)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.usrlab, 1, 3, 1, 1)
        self.layout.addWidget(self.usrlab1, 1, 5, 1, 5)
        self.layout.addWidget(self.amendlab1, 2, 3, 1, 1)
        self.layout.addWidget(self.amendedit1, 2, 5, 1, 5)
        self.layout.addWidget(self.amendlab2, 3, 3, 1, 1)
        self.layout.addWidget(self.amendedit2, 3, 5, 1, 5)
        self.layout.addWidget(self.amendlab3, 4, 3, 1, 1)
        self.layout.addWidget(self.amendedit3, 4, 5, 1, 5)
        self.layout.addWidget(self.sure, 5, 5, 1, 5)

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Edit_usr())

    def enterPress2(self):
        if len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        else:
            self.amendedit3.setFocus()

    def accept(self):
        if len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        elif len(self.amendedit3.text()) == 0:
            QMessageBox.about(self, "提示!", "确认密码框不能为空！")
            self.amendedit3.setFocus()
        elif self.amendedit3.text() != self.amendedit2.text():
            QMessageBox.about(self, "提示!", "前后密码输入不一样！")
            self.amendedit3.setFocus()
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            conn.execute("update Controller set password=(?) where number=(?)", (self.amendedit2.text(), self.number,))
            conn.commit()
            conn.close()
            QMessageBox.about(self, "提示!", "修改密码成功！！！")
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Edit_Controller(self.number))


# 编辑用户信息
class Edit_usr(QFrame):
    def __init__(self,number):
        super(Edit_usr, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.sure = QPushButton("确认")
        self.amend = QPushButton("修改用户密码")
        self.returnBtn = QPushButton("返回")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.grade = QLabel("选择年级")
        self.gradecb = QComboBox()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.devise_ui()

    def devise_ui(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_date where number=(?)", (self.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        yearnb = []
        for i in range(1980, 2020):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        grade = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级',
                 '初一', '初二', '初三',
                 '高一', '高二', '高三']
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(255,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.school.setMaximumSize(50, 40)
        self.returnBtn.setMaximumSize(60, 40)
        self.amend.setMaximumSize(190, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)
        self.grade.setMaximumSize(95, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)
        self.gradecb.setMaximumSize(420, 40)
        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.gradecb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.yearcb.addItems(yearnb)
        self.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.monthcb.addItems(monthmb)
        self.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.gradecb.addItems(grade)
        self.gradecb.setCurrentText(self.data[5])  # 设置文本的默认选项
        self.nameEdit.setText(self.data[1])
        self.schoolEiit.setText(self.data[4])
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.amend, 0, 10, 1, 1)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 4, 1, 18)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 4, 1, 18)
        self.layout.addWidget(self.year, 3, 3, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 4, 1, 8)
        self.layout.addWidget(self.monthcb, 3, 10, 1, 7)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 4, 1, 18)
        self.layout.addWidget(self.grade, 5, 3, 1, 1)
        self.layout.addWidget(self.gradecb, 5, 4, 1, 18)
        self.layout.addWidget(self.sure, 6, 4, 1, 18)
        self.sure.clicked.connect(self.connect_fun)
        self.returnBtn.clicked.connect(self.return_fun)
        self.amend.clicked.connect(self.connect_fun1)

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_news())

    def save_data(self):
        a = self.nameEdit.text()
        b = self.yearcb.currentText() + '-' + self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        e = self.gradecb.currentText()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("update User_date set name =(?),birthday=(?),sex=(?),school=(?),grade=(?) where number=(?)",
                     (a, b, c, d, e, self.number))
        conn.commit()
        conn.close()

    def connect_fun(self):
        win.splitter.widget(0).setParent(None)
        self.save_data()
        Controller_news().devise_ui()
        win.splitter.insertWidget(0, Controller_news())

    def connect_fun1(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, chang_Usr_amend(self.number))

# 修改用户密码
class chang_Usr_amend(QFrame):
    def __init__(self,number):
        super(chang_Usr_amend, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.usrlab = QLabel("账号:")
        self.amendlab1 = QLabel("原密码:")
        self.amendlab2 = QLabel("新密码:")
        self.amendlab3 = QLabel("确认密码:")
        self.amendedit1 = QLineEdit()
        self.amendedit2 = QLineEdit()
        self.amendedit3 = QLineEdit()
        self.sure = QPushButton("确认修改")
        self.returnBtn = QPushButton("返回")
        self.devise_ui()

    def devise_ui(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User where number=(?)", (self.number,))
        for data in c.fetchall():
            self.data = data
        c.close()
        conn.close()
        self.usrlab1 = QLabel(win.numble)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(350, 0, 0, 0)
        self.usrlab.setMaximumSize(80, 40)
        self.amendlab1.setMaximumSize(80, 40)
        self.amendlab2.setMaximumSize(80, 40)
        self.amendlab3.setMaximumSize(100, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usrlab.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setStyleSheet(
            "QLabel{color:rgb(100,100,100);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amendlab3.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrlab1.setMaximumSize(420, 40)
        self.amendedit1.setMaximumSize(420, 40)
        self.amendedit2.setMaximumSize(420, 40)
        self.amendedit3.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.amendedit1.setText(self.data[2])
        self.amendedit2.setPlaceholderText("请输入新密码")
        self.amendedit3.setPlaceholderText("请重新输入密码")
        self.amendedit1.setFont(QFont("宋体", 16))  # 设置QLineEditn 的字体及大小
        self.amendedit2.setFont(QFont("宋体", 16))
        self.amendedit3.setFont(QFont("宋体", 16))
        self.amendedit1.setEchoMode(QLineEdit.Password)
        self.amendedit2.setEchoMode(QLineEdit.Password)
        self.amendedit3.setEchoMode(QLineEdit.Password)
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.returnBtn.clicked.connect(self.return_fun)
        self.amendedit2.returnPressed.connect(self.enterPress2)
        self.amendedit3.returnPressed.connect(self.accept)
        self.sure.clicked.connect(self.accept)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.usrlab, 1, 3, 1, 1)
        self.layout.addWidget(self.usrlab1, 1, 5, 1, 5)
        self.layout.addWidget(self.amendlab1, 2, 3, 1, 1)
        self.layout.addWidget(self.amendedit1, 2, 5, 1, 5)
        self.layout.addWidget(self.amendlab2, 3, 3, 1, 1)
        self.layout.addWidget(self.amendedit2, 3, 5, 1, 5)
        self.layout.addWidget(self.amendlab3, 4, 3, 1, 1)
        self.layout.addWidget(self.amendedit3, 4, 5, 1, 5)
        self.layout.addWidget(self.sure, 5, 5, 1, 5)

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Edit_usr())

    def enterPress2(self):
        if len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        else:
            self.amendedit3.setFocus()

    def accept(self):
        if len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        elif len(self.amendedit3.text()) == 0:
            QMessageBox.about(self, "提示!", "确认密码框不能为空！")
            self.amendedit3.setFocus()
        elif self.amendedit3.text() != self.amendedit2.text():
            QMessageBox.about(self, "提示!", "前后密码输入不一样！")
            self.amendedit3.setFocus()
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            conn.execute("update User set password=(?) where number=(?)", (self.amendedit2.text(), self.number,))
            conn.commit()
            conn.close()
            QMessageBox.about(self, "提示!", "修改密码成功！！！")
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Edit_usr(self.number))


class CourseWidget(QWidget):
    def __init__(self,dow, data):
        super(CourseWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.data = data
        self.dow = dow
        self.imagelab = QLabel()
        self.numberlab1 = QLabel("号码:")
        self.numberlab2 =QLabel(data[0])
        self.namelab1 = QLabel("姓名:")
        self.namelab2 = QLabel(data[3])
        self.yearlab1 = QLabel("出生年月:")
        self.yearlab2 = QLabel(data[4])
        self.sexlab1 = QLabel("性别:")
        self.sexlab2 = QLabel(data[5])
        self.schoollab1 = QLabel("学校:")
        self.schoollab2 = QLabel(data[6])
        self.agreebut = QPushButton("同意")
        self.rejectbut = QPushButton("拒绝")

        self.image_path = "../datas/image/image" + data[8]
        total = base64.b64decode(data[7])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.namelab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.namelab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numberlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numberlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.yearlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.yearlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sexlab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sexlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.schoollab1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.schoollab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.agreebut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(0,255, 0)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.rejectbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(255,0, 0)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab1.setMaximumSize(80, 40)
        self.namelab2.setMaximumSize(100, 40)
        self.numberlab1.setMaximumSize(80, 40)
        self.numberlab2.setMaximumSize(150, 40)
        self.yearlab1.setMaximumSize(80, 40)
        self.yearlab2.setMaximumSize(100, 40)
        self.sexlab1.setMaximumSize(80, 40)
        self.sexlab2.setMaximumSize(80, 40)
        self.schoollab1.setMaximumSize(80, 40)
        self.schoollab2.setMaximumSize(150, 40)
        self.agreebut.setMaximumSize(80,40)
        self.rejectbut.setMaximumSize(80,40)
        self.agreebut.clicked.connect(self.agreefun)
        self.rejectbut.clicked.connect(self.rejectfun)
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab1, 1, 3, 1, 1)
        self.layout.addWidget(self.namelab2,1,4,1,1)
        self.layout.addWidget(self.yearlab1,2,3,1,1)
        self.layout.addWidget(self.yearlab2,2,4,1,1)
        self.layout.addWidget(self.sexlab1,3,3,1,1)
        self.layout.addWidget(self.sexlab2,3,4,1,1)
        self.layout.addWidget(self.numberlab1,1,6,1,1)
        self.layout.addWidget(self.numberlab2,1,7,1,2)
        self.layout.addWidget(self.schoollab1,2,6,1,1)
        self.layout.addWidget(self.schoollab2,2,7,1,2)
        self.layout.addWidget(self.agreebut,3,9,1,1)
        self.layout.addWidget(self.rejectbut,3,10,1,1)

    def agreefun(self):
        sqlpath = "../datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        conn.execute("INSERT INTO Controller VALUES(?,?,?)", (self.data[0], self.data[1], self.data[2],))
        conn.execute("insert into Controller_image values(?,?,?)", (self.data[0], self.data[7], self.data[8],))
        conn.commit()
        conn.execute("INSERT INTO Controller_data VALUES(?,?,?,?,?)",
                     (self.data[0],self.data[3],self.data[4],self.data[5],self.data[6],))
        c.execute("delete from Controller2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_image2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_data2 where number=(?)", (self.data[0],))
        c.close()
        conn.commit()
        conn.close()
        self.dow.deleteitem(self.data[0])
        QMessageBox.about(self, "提示!", "操作成功！！")

    def rejectfun(self):
        sqlpath = "../datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("delete from Controller2 where number=(?)",(self.data[0],))
        c.execute("delete from Controller_image2 where number=(?)", (self.data[0],))
        c.execute("delete from Controller_data2 where number=(?)", (self.data[0],))
        conn.commit()
        c.close()
        conn.close()
        self.dow.deleteitem(self.data[0])
        QMessageBox.about(self, "提示!", "操作成功！！")

class CourseQlist(QListWidget):
    def __init__(self):
        super(CourseQlist, self).__init__()
        sqlpath = "../datas/database/Information.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Controller2.number,usrname,password,name,birthday,sex,school,total,filename from \
                  Controller2,Controller_data2,Controller_image2 where \
                   Controller2.number = Controller_data2.number and \
                    Controller2.number = Controller_image2.number")
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CourseWidget(self,data))

    def deleteitem(self,data):
        x= 0
        for da in self.datas:
            if da[0]==data:
                item = self.takeItem(x)
                # 删除widget
                self.removeItemWidget(item)
                del item
                break
            x= x+1

class Controller_Logon(QFrame):
    def __init__(self):
        super(Controller_Logon, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.password2 = QLabel("确认密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        self.password2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.codeLineEdit.setMaximumSize(310, 40)
        # self.usrLineEdit2.setText(a)
        self.usrLine.setPlaceholderText("请输入手机号码")
        self.usrnameLine.setPlaceholderText("请输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请输入密码")
        self.pwdLineEdit2.setPlaceholderText("请重新输入密码")
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.codeLineEdit.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLine.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.usrnameLine.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit1.returnPressed.connect(self.enterPress3)
        self.pwdLineEdit2.returnPressed.connect(self.enterPress4)
        self.returnBtn.clicked.connect(self.returnfun)  # 返回
        self.okBtn.clicked.connect(self.accept)
        self.change_code.linkActivated.connect(self.renovate_code)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLine, 1, 5, 1, 14)
        self.layout.addWidget(self.usrname, 2, 3, 1, 1)
        self.layout.addWidget(self.usrnameLine, 2, 5, 1, 14)
        self.layout.addWidget(self.password1, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 3, 5, 1, 14)
        self.layout.addWidget(self.password2, 4, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 4, 5, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 5, 5, 1, 5)
        self.layout.addWidget(self.codebel, 5, 10, 1, 6)
        self.layout.addWidget(self.change_code, 5, 12, 1, 1)
        self.layout.addWidget(self.okBtn, 6, 5, 1, 14)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("../datas/wen/code.png")
        self.codebel.setPixmap(QPixmap("../datas/wen/code.png"))
        self.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 注册时输入的号码检验是否已经注册过的
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller")
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
        conn.execute("INSERT INTO Controller VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    def enterPress1(self):  # 注册-》用户框回车确定时判断文字框是否有输入
        if (len(self.usrLine.text()) == 0):
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif (len(self.usrLine.text()) != 11):
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.usrLine.setText("")
        else:
            self.usrnameLine.setFocus()

    def enterPress2(self):  # 注册-》用户名框回车确定时判断文字框是否有输入
        if (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        else:
            self.pwdLineEdit1.setFocus()

    def enterPress3(self):  # 注册-》密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit1.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        else:
            self.pwdLineEdit2.setFocus()

    def enterPress4(self):  # 注册-》确认密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit2.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif (self.pwdLineEdit1.text() != self.pwdLineEdit2.text()):
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        else:
            self.codeLineEdit.setFocus()

    def accept(self):  # 注册时将账号密码保存并登录。
        if len(self.usrLine.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif len(self.usrLine.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.usrLine.setText("")
        elif (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        elif len(self.pwdLineEdit1.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        elif len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "确认密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif self.pwdLineEdit1.text() != self.pwdLineEdit2.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.codeLineEdit.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.codeLineEdit.setText("")
            self.codeLineEdit.setFocus()
        else:
            self.save_data()
            dow = Controller_informent(self.usrLine.text())
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, dow)

    def returnfun(self):  # 连接用户登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_news())

class Controller_informent(QFrame):
    def __init__(self,number):
        super(Controller_informent, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.sure = QPushButton("确认")
        self.chang_image = QPushButton("换头像")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.nameEdit = QLineEdit()
        self.tupian = QLabel()
        self.schoolEiit = QLineEdit()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(100, 0, 0, 0)
        yearnb = []
        for i in range(1960, 2005):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.chang_image.setStyleSheet(
            "QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setPlaceholderText("请输入姓名")
        self.schoolEiit.setPlaceholderText("请输入学校名称")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.chang_image.setMaximumSize(90, 40)
        self.school.setMaximumSize(50, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)
        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.tupian.setMaximumSize(250, 250)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.yearcb.addItems(yearnb)
        self.monthcb.addItems(monthmb)
        self.layout.addWidget(self.tupian, 1, 1, 4, 4)
        self.layout.addWidget(self.chang_image, 4, 2, 1, 2)
        self.layout.addWidget(self.name, 1, 6, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 8, 1, 8)
        self.layout.addWidget(self.sex, 2, 6, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 8, 1, 8)
        self.layout.addWidget(self.year, 3, 6, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 8, 1, 4)
        self.layout.addWidget(self.monthcb, 3, 11, 1, 7)
        self.layout.addWidget(self.school, 4, 6, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 8, 1, 8)
        self.layout.addWidget(self.sure, 6, 8, 1, 8)
        self.image()
        self.sure.clicked.connect(self.connect_fun)
        self.chang_image.clicked.connect(self.chang_fun)

    def image(self):
        self.image_path = "../datas/image/a7.jpeg"
        self.file = os.path.splitext(self.image_path)[1]
        self.tupian.setPixmap(QPixmap(self.image_path))
        self.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.image_path = path
            self.file = os.path.splitext(self.image_path)[1]
            self.tupian.setPixmap(QPixmap(self.image_path))
            self.tupian.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.image()

    def save_data(self):
        a = self.nameEdit.text()
        b = self.yearcb.currentText() + '-' + self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("insert into Controller_image values(?,?,?)", (self.number, total, self.file,))
        conn.commit()
        conn.execute("INSERT INTO Controller_data VALUES(?,?,?,?,?)", (self.number, a, b, c, d,))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/ControllerSQ" + str(self.number) + "L.db"
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
        try:  # 文件信息表 序号    课程号    课程名      文件名    文件后缀
            c.execute('''CREATE TABLE Filename2(no text,Cno text,Cname text,name text,filename1 text)''')
        except:
            pass
        try:
            c.execute('''CREATE TABLE Filedate2(no text,total LONGBLOB )''')
        except:
            pass
        c.close()
        conn.close()

    def connect_fun(self):
        if len(self.nameEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "姓名框不能为空！！")
            self.nameEdit.setFocus()
        if len(self.schoolEiit.text()) == 0:
            QMessageBox.about(self, "提示!", "学校框不能为空！！")
            self.schoolEiit.setFocus()
        else:
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_news())
            QMessageBox.about(self, "提示", '添加管理员成功!!')

class Usr_Logon(QFrame):
    def __init__(self):
        super(Usr_Logon, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.password2 = QLabel("确认密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.codeLineEdit = QLineEdit()
        self.okBtn = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.change_code = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(300, 0, 0, 0)
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        self.password2.setMaximumSize(80, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.codeLineEdit.setMaximumSize(310, 40)
        # self.usrLineEdit2.setText(a)
        self.usrLine.setPlaceholderText("请输入手机号码")
        self.usrnameLine.setPlaceholderText("请输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请输入密码")
        self.pwdLineEdit2.setPlaceholderText("请重新输入密码")
        self.codeLineEdit.setPlaceholderText("请输入右侧的验证码")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.codeLineEdit.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.okBtn.setMaximumSize(420, 40)
        self.change_code.setText("<A href='www.baidu.com'>看不清，换一个</a>")
        self.change_code.setStyleSheet(
            "QLabel{color:rgb(0,0,255);font-size:12px;font-weight:normal;font-family:Arial;}")
        self.change_code.setMaximumSize(120, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLine.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.usrnameLine.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit1.returnPressed.connect(self.enterPress3)
        self.pwdLineEdit2.returnPressed.connect(self.enterPress4)
        self.returnBtn.clicked.connect(self.change_record)  # 点击返回键连接管理员登录界面
        self.okBtn.clicked.connect(self.accept)
        self.change_code.linkActivated.connect(self.renovate_code)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLine, 1, 5, 1, 14)
        self.layout.addWidget(self.usrname, 2, 3, 1, 1)
        self.layout.addWidget(self.usrnameLine, 2, 5, 1, 14)
        self.layout.addWidget(self.password1, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 3, 5, 1, 14)
        self.layout.addWidget(self.password2, 4, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 4, 5, 1, 14)
        self.layout.addWidget(self.codeLineEdit, 5, 5, 1, 5)
        self.layout.addWidget(self.codebel, 5, 10, 1, 6)
        self.layout.addWidget(self.change_code, 5, 12, 1, 1)
        self.layout.addWidget(self.okBtn, 6, 5, 1, 14)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("../datas/wen/code.png")
        self.codebel.setPixmap(QPixmap("../datas/wen/code.png"))
        self.codebel.setScaledContents(True)  # 让图片自适应label大小

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

    def enterPress1(self):  # 注册-》用户框回车确定时判断文字框是否有输入
        if (len(self.usrLine.text()) == 0):
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif (len(self.usrLine.text()) != 11):
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.usrLine.setText("")
        else:
            self.usrnameLine.setFocus()

    def enterPress2(self):  # 注册-》用户名框回车确定时判断文字框是否有输入
        if (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        else:
            self.pwdLineEdit1.setFocus()

    def enterPress3(self):  # 注册-》密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit1.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        else:
            self.pwdLineEdit2.setFocus()

    def enterPress4(self):  # 注册-》确认密码框回车确定时判断文字框是否有输入
        if (len(self.pwdLineEdit2.text()) == 0):
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif (self.pwdLineEdit1.text() != self.pwdLineEdit2.text()):
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        else:
            self.codeLineEdit.setFocus()

    def accept(self):  # 注册时将账号密码保存并登录。
        if len(self.usrLine.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLine.setFocus()
        elif len(self.usrLine.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLine.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.usrLine.setText("")
        elif (len(self.usrnameLine.text()) == 0):
            QMessageBox.about(self, "提示!", "用户名不能为空！")
            self.usrnameLine.setFocus()
        elif len(self.pwdLineEdit1.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.pwdLineEdit1.setFocus()
        elif len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "确认密码不能为空！")
            self.pwdLineEdit2.setFocus()
        elif self.pwdLineEdit1.text() != self.pwdLineEdit2.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.codeLineEdit.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.codeLineEdit.setText("")
            self.codeLineEdit.setFocus()
        else:
            self.save_data()
            dow = Usr_informent(self.usrLine.text())
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0,dow )
            # 连接主窗口界面。

    def change_record(self):  # 连接用户登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_news())

class Usr_informent(QFrame):
    def __init__(self,number):
        super(Usr_informent, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number = number
        self.sure = QPushButton("确认")
        self.chang_image = QPushButton("换头像")
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex = QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.grade = QLabel("选择年级")
        self.gradecb = QComboBox()
        self.nameEdit = QLineEdit()
        self.tupian = QLabel()
        self.schoolEiit = QLineEdit()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(100, 0, 0, 0)
        yearnb = []
        for i in range(1980, 2020):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        grade = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级',
                 '初一', '初二', '初三',
                 '高一', '高二', '高三']
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.chang_image.setStyleSheet(
            "QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setPlaceholderText("请输入姓名")
        self.schoolEiit.setPlaceholderText("请输入学校名称")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.chang_image.setMaximumSize(90, 40)
        self.school.setMaximumSize(50, 40)
        self.year.setMaximumSize(95, 40)
        self.sex.setMaximumSize(50, 40)
        self.grade.setMaximumSize(95, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sure.setMaximumSize(420, 40)
        self.sexcb.setMaximumSize(420, 40)
        self.gradecb.setMaximumSize(420, 40)
        self.yearcb.setMaximumSize(220, 40)
        self.monthcb.setMaximumSize(175, 40)
        self.tupian.setMaximumSize(250, 250)
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.gradecb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sexcb.addItems(['男', '女'])
        self.yearcb.addItems(yearnb)
        self.monthcb.addItems(monthmb)
        self.gradecb.addItems(grade)
        self.layout.addWidget(self.tupian, 1, 1, 4, 4)
        self.layout.addWidget(self.chang_image, 4, 2, 1, 2)
        self.layout.addWidget(self.name, 1, 6, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 8, 1, 8)
        self.layout.addWidget(self.sex, 2, 6, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 8, 1, 8)
        self.layout.addWidget(self.year, 3, 6, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 8, 1, 4)
        self.layout.addWidget(self.monthcb, 3, 11, 1, 7)
        self.layout.addWidget(self.school, 4, 6, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 8, 1, 8)
        self.layout.addWidget(self.grade, 5, 6, 1, 1)
        self.layout.addWidget(self.gradecb, 5, 8, 1, 8)
        self.layout.addWidget(self.sure, 6, 8, 1, 8)
        self.image()
        self.sure.clicked.connect(self.connect_fun)
        self.chang_image.clicked.connect(self.chang_fun)

    def image(self):
        self.image_path = "../datas/image/a7.jpeg"
        self.file = os.path.splitext(self.image_path)[1]
        self.tupian.setPixmap(QPixmap(self.image_path))
        self.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.image_path = path
            self.file = os.path.splitext(self.image_path)[1]
            self.tupian.setPixmap(QPixmap(self.image_path))
            self.tupian.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.image()

    def save_data(self):
        a = self.nameEdit.text()
        b = self.yearcb.currentText() + '-' + self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        e = self.gradecb.currentText()
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab)
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_date VALUES(?,?,?,?,?,?)", (self.number, a, b, c, d, e))
        conn.execute("insert into User_image values(?,?,?)",(self.number, total, self.file,))
        conn.execute("INSERT INTO Student_date VALUES(?,?,?,?,?)", (self.number, theTime, 1, 0.0, theTime))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/SQ" + str(self.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:                                  # 开始时间  ， 课程号，课程名， 文件名 ， 结束时间
            c.execute('''CREATE TABLE User_data(strat_time text,Cno text,Coursename text, filename text,last_time text)''')
        except:
            pass
        c.close()
        conn.close()

    def connect_fun(self):
        if len(self.nameEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "姓名框不能为空！！")
            self.nameEdit.setFocus()
        if len(self.schoolEiit.text()) == 0:
            QMessageBox.about(self, "提示!", "学校框不能为空！！")
            self.schoolEiit.setFocus()
        else:
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_news())
            QMessageBox.about(self, "提示", '添加用户成功!!')

class Reptile(QFrame):
    def __init__(self):
        super(Reptile, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Reptile_child1but1 = QPushButton("返回")
        self.Reptile_child1but2 = QPushButton("开始")
        self.Reptile_child1but3 = QPushButton("暂停")
        self.Reptile_child1but4 = QPushButton("重新选择")
        self.window1tree = QTextEdit()
        self.job = RepliteJob(self)
        self.dow = Select_Reptile(self)
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
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
        self.Reptile_child1but1.clicked.connect(self.return_fun)
        self.Reptile_child1but2.clicked.connect(self.select_fun1)
        self.Reptile_child1but3.clicked.connect(self.select_fun2)
        self.Reptile_child1but4.clicked.connect(self.select_fun3)
        self.win_layout1.addWidget(self.Reptile_child1but1, 1, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but2, 2, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but3, 3, 0, 1, 2)
        self.win_layout1.addWidget(self.Reptile_child1but4, 4, 0, 1, 2)
        self.win_layout2.addWidget(self.window1tree, 0, 0, 20, 20)
        self.dow.show()

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def select_fun3(self):
        self.window1tree.clear()
        self.dow.fun2()
        self.dow.show()

    def clicked1(self):
        self.Reptile_child1but1.setEnabled(True)
        self.Reptile_child1but2.setEnabled(True)
        self.Reptile_child1but4.setEnabled(True)

    def clicked2(self):
        self.Reptile_child1but1.setEnabled(True)
        self.Reptile_child1but4.setEnabled(True)

    def select_fun2(self):
        self.job.stop()
        QMessageBox.about(self, "提示", '暂停成功!!')
        self.Reptile_child1but3.setEnabled(False)
        time.sleep(2)


    def select_fun1(self):
        self.Reptile_child1but2.setEnabled(False)
        self.Reptile_child1but3.setEnabled(True)
        type = self.dow.gettype()
        greade = self.dow.getgrade()
        course = self.dow.getcourse()
        rely = QMessageBox.question(self, "提示!", "爬取过程需要时间比较久\n请问是否继续？", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
        if rely == 65536:
            return
        self.window1tree.setPlainText("爬取课件数据开始\n爬取过程需要时间比较久，请您耐心等待!!\n\n")
        self.job.setdata(type,greade,course)
        self.job.updated.connect(self.settext)
        self.job.start()

    def settext(self,text):
        self.window1tree.append(text)
        QApplication.processEvents()

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
        sqlpath = "../datas/database/Data.db"
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
            file = '../datas/wen/xinwen' + filename
            d = requests.get(url2, timeout=10, headers=self.get_agent())
            with open(file, 'wb')as f:
                # 将网上的文件下载保存进电脑。
                for chunk in d.iter_content(chunk_size=100):
                    f.write(chunk)
            f.close()
            if filename == ".ppt":
                pa = "../datas/tupian"  # 保存图片的路径
                self.ppt_to_pdf("../datas/wen/", file)  # 将ppt转换为图片。
                pdf_path = r"../datas/wen/xinwen.pdf"
                self.pdf_to_image(pdf_path, pa)
                os.remove(pdf_path)
                self.file_to_zip(pa)  # 将文件夹压缩为压缩包。
                filen = pa + ".zip"  # 压缩包的路径
                with open(filen, "rb") as f:
                    total = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                time.sleep(2)
                filen = r"../datas/tupian/image1.jpg"
                with open(filen, "rb") as f:
                    total2 = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                filename1 = '.zip'
                self.savedata(file1, file2, file3, title, total, total2, filename1, ".jpg")
            elif filename == '.zip':
                self.zip_to_files(file)  # 将压缩包解压。
                pa1 = r'../datas/wen/xinwen'  # 解压后的文件名
                fileNames = glob.glob(pa1 + r'/*')  # 读取解压文件夹里的文件。
                for fileName in fileNames:
                    end_file = os.path.splitext(fileName)[1]
                    filena = os.path.split(fileName)[1][:-len(end_file)]
                    if end_file == '.ppt' or end_file == '.pptx':
                        pa = r"../datas/tupian"  # 保存图片的路径
                        self.ppt_to_pdf("../datas/wen/", fileName)  # 将ppt转换为图片。
                        pdf_path = "../datas/wen/" + filena + '.pdf'
                        self.pdf_to_image(pdf_path, pa)
                        os.remove(pdf_path)
                        self.file_to_zip(pa)  # 将文件夹压缩为压缩包。
                        filen = pa + ".zip"  # 压缩包的路径
                        with open(filen, "rb") as f:
                            total = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        time.sleep(2)
                        filen = r"../datas/tupian/image1.jpg"
                        with open(filen, "rb") as f:
                            total2 = base64.b64encode(f.read())  # 将文件转换为字节。
                        f.close()
                        filename1 = ".zip"
                        self.savedata(file1, file2, file3, title, total, total2, filename1, ".jpg")
                        break
            sqlpath = "../datas/database/Data.db"
            conn = sqlite3.connect(sqlpath)
            conn.execute("insert into successfulurl(url,howbyte)values(?,?)", (url, data))
            conn.commit()
            conn.close()
            return (title + "\n爬取成功\n")
        except:
            return ("爬取错误\n")

    def savedata(self,file1,file2,file3,title,total,total2,filename1,filename2):
        sqlpath = "../datas/database/Data.db"
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




class Addfile(QFrame):
    def __init__(self):
        super(Addfile, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dow = Select_location(self)
        self.returnbut = QPushButton("返回")
        self.addfile = QPushButton("添加文件")
        self.addmufile = QPushButton("添加目录")
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b = self.screenRect.height() * 1.0 / 5
        a = self.screenRect.width() * 1.0 / 3

        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addmufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.clicked.connect(self.returnfun)
        self.addfile.clicked.connect(self.select_fun1)
        self.addmufile.clicked.connect(self.select_fun2)
        self.layout.addWidget(self.returnbut, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.addfile, 1, 0)
        self.layout.addWidget(self.addmufile, 2, 0)
        self.returnbut.setMaximumSize(a, b)
        self.addfile.setMaximumSize(a, b)
        self.addmufile.setMaximumSize(a, b)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

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
        file1 = '../datas/tupian'
        fileNames = glob.glob(file1 + r'/*')
        if fileNames:
            for fileName in fileNames:
                # 将pa 文件夹中的文件删除。
                os.remove(fileName)
        if end_file == '.ppt' or end_file == '.pptx':
            Reptile_data().ppt_to_pdf("../datas/wen/", path)
            pdf_path = "../datas/wen/" + file + '.pdf'
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
            Reptile_data().word_to_pdf("../datas/wen/", path)
            pdf_path = "../datas/wen/" + file + '.pdf'
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
        sqlpath = "../datas/database/Data.db"
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

class Select_location(QWidget):
    def __init__(self,dow):
        super(Select_location, self).__init__()
        self.dow = dow
        self.setWindowTitle("选择文件保存位置")
        self.lab = QLabel("请选择文件保存的位置！！！！")
        self.typelab = QLabel("学习阶段")
        self.typebox = QComboBox()
        self.greadelab = QLabel("年级")
        self.greadebox = QComboBox()
        self.courselab = QLabel("科目")
        self.coursebox = QComboBox()
        self.sure = QPushButton("确定")
        self.devise_ui()

    def devise_ui(self):
        self.resize(750, 400)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.lab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.typelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.greadelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.lab.setMaximumSize(400,80)
        self.typelab.setMaximumSize(80,50)
        self.greadelab.setMaximumSize(80,50)
        self.courselab.setMaximumSize(80,50)
        self.typebox.setMaximumSize(160, 50)
        self.greadebox.setMaximumSize(160, 50)
        self.coursebox.setMaximumSize(160, 50)
        self.sure.setMaximumSize(80,50)
        self.typebox.addItems(['','小学','初中','高中'])
        self.typebox.currentIndexChanged.connect(self.fun1)
        self.sure.clicked.connect(self.surefun)
        self.layout.addWidget(self.lab,0,2,1,6)
        self.layout.addWidget(self.typelab,1,0,1,1)
        self.layout.addWidget(self.typebox,1,1,1,2)
        self.layout.addWidget(self.greadelab,1,3,1,1)
        self.layout.addWidget(self.greadebox,1,4,1,2)
        self.layout.addWidget(self.courselab,1,6,1,1)
        self.layout.addWidget(self.coursebox,1,7,1,2)
        self.layout.addWidget(self.sure,2,8,1,1)

    def fun1(self):
        self.greadebox.clear()
        self.coursebox.clear()
        if self.typebox.currentText()=="小学":
            self.greadebox.addItems(['','一年级上册','一年级下册','二年级上册','二年级下册','三年级上册','三年级下册',
                                     '四年级上册','四年级下册','五年级上册','五年级下册','六年级上册','六年级下册'])
            self.coursebox.addItems(['','语文','数学','英语'])
        elif self.typebox.currentText()=="初中":
            self.greadebox.addItems(['','初一上册','初一下册','初二上册','初二下册','初三上册','初三下册',])
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])
        elif self.typebox.currentText()=="高中":
            self.greadebox.addItems(['','必修一','必修二','必修三','必修四','必修五',
                                     '选修一','选修二','选修三','选修四','选修五'])
            self.coursebox.addItems(['','语文','数学','英语','物理','化学','生物','政治','历史','地理'])

    def fun2(self):
        self.greadebox.clear()
        self.coursebox.clear()
        self.typebox.clear()
        self.typebox.addItems(['', '小学', '初中', '高中'])

    def surefun(self):
        if(self.greadebox.currentText()==""):
            QMessageBox.about(self, "提示", '年级的选项框不能为空!!')
        elif(self.typebox.currentText()==""):
            QMessageBox.about(self, "提示", '学习阶段的选项框不能为空!!')
        elif (self.coursebox.currentText()==""):
            QMessageBox.about(self, "提示", '科目的选项框不能为空!!')
        self.close()
        self.dow.clicked()

    def gettype(self):
        return self.typebox.currentText()

    def getgrade(self):
        return self.greadebox.currentText()

    def getcourse(self):
        return self.coursebox.currentText()

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

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
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


# 创建保存用户信息的数据库
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
    try:  # 课程表   课程码        课程名          加课码            人数
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



if __name__ == "__main__":
    found_sql()
    app = QApplication(sys.argv)
    win = QUnFrameWindow()
    win.show()
    sys.exit(app.exec_())

