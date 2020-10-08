"""
作者：钟培望
名称：具体人工智能沉浸式学习系统管理员端
时间：2020.4.30
版本: 1.0
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
import fitz
import sqlite3
import zipfile
import shutil
from PIL import Image
import subprocess



class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """

    def __init__(self):  # 设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None)  # 设置为顶级窗口
        self.setWindowTitle("low_Administrators")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.setMinimumWidth(670)
        self.setMinimumHeight(560)
        self.resize(self.x, self.y)
        self.number = ''
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
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.splitter.addWidget(Record())
        #self.splitter.addWidget(Function())

    def close_win(self):
        rely = QMessageBox.question(self, "提示!", "是否退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if rely == 65536:
            return
        self.close()
        sys.exit()

    def logonquit_fun(self):
        rely = QMessageBox.question(self, "提示!", "是否退出登录？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if rely == 65536:
            return
        self.splitter.widget(0).setParent(None)
        self.splitter.addWidget(Record())


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
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
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
        self.returnBtn.setMaximumSize(80, 40)
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

    def checking2(self):  # 注册时输入的号码检验是否已经让管理员批准
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller2")
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
        conn.execute("INSERT INTO Controller2 VALUES(?,?,?)", (a, b, c))
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
        elif (self.checking2()):
            QMessageBox.about(self, "提示!", "您输入的号码正在等待注册批准通过！\n请您耐心等待！")
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
        elif (self.checking2()):
            QMessageBox.about(self, "提示!", "您输入的号码正在等待注册批准通过！\n请您耐心等待！")
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
            win.number = self.usrLine.text()
            self.save_data()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_informent())
            # 连接主窗口界面。

    def change_record(self):  # 连接用户登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Record())


class Record(QFrame):
    # 用户登录界面
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
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
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

    def checking1(self):  # 登录时检验号码是否没有注册
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    def checking2(self):  # 注册时输入的号码检验是否已经让管理员批准
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller2")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit.text():
                return True
        c.close()
        conn.close()
        return False

    def enterPress1(self):  # 登录回车确定时判断文字框是否有输入
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.usrLineEdit.setFocus()
        elif (self.checking2()):
            QMessageBox.about(self, "提示!", "您输入的号码正在等待注册批准通过！\n请您耐心等待！")
            self.usrLineEdit.setText("")
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
        elif (self.checking2()):
            QMessageBox.about(self, "提示!", "您输入的号码正在等待注册批准通过！\n请您耐心等待！")
            self.usrLineEdit.setText("")
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
            c.execute("select * from Controller")
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


# 用户忘记密码
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
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0);}\
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
        self.returnBtn.setMaximumSize(80, 40)
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
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U',
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
        c.execute("select * from Controller")
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
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0] == self.usrLineEdit2.text():
                win.number = variate[0]
                conn.execute("update Controller set password=(?) where number=(?)",
                             (self.pwdLineEdit2.text(), variate[0],))
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
            win.splitter.insertWidget(0, Function())  # 连接主窗口界面。


# 管理员信息填写
class Controller_informent(QFrame):
    def __init__(self):
        super(Controller_informent, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
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
        conn.execute("insert into Controller_image2 values(?,?,?)", (win.number, total, self.file,))
        conn.commit()
        conn.execute("INSERT INTO Controller_data2 VALUES(?,?,?,?,?)", (win.number, a, b, c, d,))
        conn.commit()
        conn.close()
        sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
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
        try:            # 文件信息表 序号    课程号    课程名      文件名  答案  文件后缀
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
        if len(self.nameEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "姓名框不能为空！！")
            self.nameEdit.setFocus()
        if len(self.schoolEiit.text()) == 0:
            QMessageBox.about(self, "提示!", "学校框不能为空！！")
            self.schoolEiit.setFocus()
        else:
            self.save_data()
            QMessageBox.about(self, "提示!", "等待超级管理员的验证通过后再登录！！\n请您耐心等待！！")
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Record())



class Function(QFrame):  # 超级管理员功能界面
    def __init__(self):
        super(Function, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainbutton1 = QPushButton("班级信息")  # 用户功能界面的控件
        self.mainbutton2 = QPushButton("统计信息")
        self.mainbutton3 = QPushButton("我的")
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
        self.layout.addWidget(self.mainbutton3,0,2)
        self.mainbutton1.setMaximumSize(a, b)
        self.mainbutton2.setMaximumSize(a, b)
        self.mainbutton3.setMaximumSize(a,b)

    def select_fun1(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Class_news())

    def select_fun2(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Statistics_news())

    def select_fun3(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,Controller_myself())


class Class_news(QFrame):
    def __init__(self):
        super(Class_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnbut = QPushButton("返回")
        self.addcourse = QPushButton("添加课程")
        self.lab = QLabel()
        self.add = AddCourse()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window = Coursewindow(self)
        self.qtool.addItem(self.window, '我的课程')
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addcourse.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.addcourse.setMaximumSize(100, 40)
        self.lab.setMaximumSize(200, 40)
        self.returnbut.clicked.connect(self.returnfun)
        self.addcourse.clicked.connect(self.addfun)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.addcourse, 0, 17, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def addfun(self):
        self.add.nameEdit.setText('')
        self.add.image()
        # 接受子窗口传回来的信号  然后调用主界面的函数
        self.add.my_Signal.connect(self.changfun)
        self.add.show()

    def changfun(self):
        self.qtool.removeItem(0)
        self.window = Coursewindow(self)
        self.qtool.addItem(self.window, '我的课程')

    def clicked(self, data):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Course_news(data))


class CustomWidget(QWidget):
    def __init__(self, data):
        super(CustomWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.courselab = QLabel("课程编号:")
        self.numlab = QLabel("人数:")
        self.courselab2 = QLabel(data[0])
        self.numlab2 = QLabel(str(data[2]))
        self.image_path = "../datas/image/image" + data[4]
        total = base64.b64decode(data[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.courselab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.courselab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80, 40)
        self.courselab2.setMaximumSize(100, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.courselab, 1, 8, 1, 1)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.courselab2, 1, 9, 1, 2)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)


class Coursewindow(QListWidget):
    def __init__(self, dow):
        super(Coursewindow, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,name,numble,total,filename \
                  from Course,Course_image,Teacher_Course \
                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                    and number=(?)", (win.number,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CustomWidget(data))

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            rely = QMessageBox.question(self, "提示!", "该操作会删除整个课程的数据\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Course where Cno=(?)",(self.datas[index][0]))
            c.execute("delete from Course_image where Cno=(?)", (self.datas[index][0]))
            c.execute("delete from Teacher_Course where Cno=(?)", (self.datas[index][0]))
            c.execute("delete from Join_Course where Cno=(?)", (self.datas[index][0]))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '课程删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            self.dow.clicked(da)


class Course_news(QFrame):
    def __init__(self, data):
        super(Course_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data
        self.returnbut = QPushButton("返回")
        self.addcufile = QPushButton("添加课件")
        self.addexfile = QPushButton("添加练习")
        self.lab = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window1 = CoursecuQlist(self, self.data)
        self.window2 = CourseexQlist(self, self.data)
        self.qtool.addItem(self.window1, self.data[1]+"　课件")
        self.qtool.addItem(self.window2, self.data[1] + "　练习")
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addcufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addexfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.addcufile.setMaximumSize(100, 40)
        self.addexfile.setMaximumSize(100,40)
        self.lab.setMaximumSize(200, 40)
        self.returnbut.clicked.connect(self.returnfun)
        self.addcufile.clicked.connect(self.addcufun)
        self.addexfile.clicked.connect(self.addexfun)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.addcufile,0,15,1,2)
        self.layout.addWidget(self.addexfile, 0, 17, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Class_news())

    def addcufun(self):
        addcufile = Addcufile(self.data)
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, addcufile)

    def addexfun(self):
        addexfile = Addexfile(self.data)
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, addexfile)


    def clicked(self):
        self.max = max_widget()
        self.max.show()

    def clicked2(self,data,answer):
        self.add =  Addexfilewin2(data,answer)
        self.add.show()

#课件的item 设计
class CoursecuWidget(QWidget):
    def __init__(self, data):
        super(CoursecuWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
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
class CoursecuQlist(QListWidget):
    def __init__(self, dow, data):
        super(CoursecuQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select Filename.no,name,total,filename2 from \
                  Filename,Fileimage where Filename.no = Fileimage.no \
                   and Cno=(?) ", (data[0],))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CoursecuWidget(data))

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            rely = QMessageBox.question(self, "提示!", "该操作会造成数据完全删除无法恢复\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Filename where no=(?)",(self.datas[index][0],))
            c.execute("delete from Fileimage where no=(?)", (self.datas[index][0],))
            c.execute("delete from Filedate where no=(?)", (self.datas[index][0],))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '文件删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Cname,name,total,filename1 from \
                       Filename,Filedate where Filename.no= Filedate.no \
                        and Filename.no=(?)",(da[0],))
            filedata = c.fetchall()[0]
            zip_path = '../datas/'+filedata[0]
            if (not (os.path.exists(zip_path))):  # 创建文件夹。
                os.makedirs(zip_path)
            zip_path = zip_path +'/'+filedata[1]+filedata[3]
            total = base64.b64decode(filedata[2])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            self.zip_to_files(zip_path)
            self.dow.clicked()

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

#管理员播放课件　
class max_widget(QWidget):
    def __init__(self):
        super(max_widget, self).__init__()
        self.pa = '../datas/tupian'
        self.fileNames = glob.glob(self.pa + r'/*')
        self.a = 1
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.lab2 = QtWidgets.QLabel(self)
        self.lab2.resize(self.width1, self.height1)
        #self.MaximumButton1 = QPushButton(self)
        #self.MaximumButton1.resize(10, 10)
        #self.MaximumButton1.setStyleSheet("QPushButton{background-color:rgb(255,255, 255)}\
        #                   QPushButton:hover{background-color:rgb(50, 10, 50)} ")
        #self.MaximumButton1.move(24, 24)
        #self.MaximumButton1.clicked.connect(self.closewin)
        self.lab2.setMouseTracking(True)  # 设置widget鼠标跟踪
        pa1 = self.fileNames[self.a-1]
        pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
        img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
        out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
        out.save(pa2, 'jpeg')
        pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.lab2.setPixmap(pixmap)  # 在label上显示图片
        # self.lab2.setScaledContents (True) # 让图片自适应label大小



    def mousePressEvent(self, event):  # 重写鼠标点击的事件
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        if (event.button() == Qt.LeftButton) and (event.pos().x() < self.x / 2):
            self.cut_images()
        if (event.button() == Qt.LeftButton) and (event.pos().x() > self.x / 2):
            self.add_images()

    def add_images(self):  # 下一页ppt
        self.a = self.a + 1
        try:
            pa1 = self.fileNames[self.a-1]
            pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
            img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
            out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
            out.save(pa2, 'jpeg')
            pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.lab2.setPixmap(pixmap)
        except:
            self.a = self.a - 1
            QMessageBox.about(self, "提示!", "这是最后一页")


    def cut_images(self):  # 上一页ppt
        self.a = self.a - 1
        pa1 = self.fileNames[self.a-1]
        pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
        if self.a == 0:
            self.a = self.a + 1
            QMessageBox.about(self, "提示!", "这是第一页")
        else:
            img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
            out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
            out.save(pa2, 'jpeg')
            pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.lab2.setPixmap(pixmap)

#练习的item 设计
class CourseexWidget(QWidget):
    def __init__(self, data):
        super(CourseexWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.namelab = QLabel(data[1])
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.namelab.setMaximumSize(800, 60)
        self.layout.addWidget(self.namelab, 1, 1, 1, 1)

#练习的QList
class CourseexQlist(QListWidget):
    def __init__(self, dow, data):
        super(CourseexQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select no,name from Filename2 where Cno=(?) ", (data[0],))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 80))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, CourseexWidget(data))

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            rely = QMessageBox.question(self, "提示!", "该操作会造成数据完全删除无法恢复\n请问是否继续？",
                                        QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if rely == 65536:
                return
            sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("delete from Filename2 where no=(?)",(self.datas[index][0],))
            c.execute("delete from Filedate2 where no=(?)", (self.datas[index][0],))
            conn.commit()
            c.close()
            conn.close()
            item = self.takeItem(index)
            # 删除widget
            self.removeItemWidget(item)
            del item
            QMessageBox.about(self, "提示", '文件删除成功!!')

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Cname,name,answer,total,filename1 from \
                       Filename2,Filedate2 where Filename2.no= Filedate2.no \
                        and Filename2.no=(?)",(da[0],))
            filedata = c.fetchall()[0]
            zip_path = '../datas/'+filedata[0]
            if (not (os.path.exists(zip_path))):  # 创建文件夹。
                os.makedirs(zip_path)
            zip_path = zip_path +'/'+filedata[1]+filedata[4]
            total = base64.b64decode(filedata[3])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            self.zip_to_files(zip_path)
            self.dow.clicked2(da[0],filedata[2])

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

#添加课件
class Addcufile(QFrame):
    def __init__(self, data):
        super(Addcufile, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data
        self.returnbut = QPushButton("返回")
        self.addfile = QPushButton("添加文件")
        self.addmufile = QPushButton("添加目录")
        self.addsystem = QPushButton("从系统添加")
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
        b = self.screenRect.height() * 1.0 / 4
        a = self.screenRect.width() * 1.0 / 5

        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addmufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addsystem.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.clicked.connect(self.returnfun)
        self.addfile.clicked.connect(self.select_fun1)
        self.addmufile.clicked.connect(self.select_fun2)
        self.addsystem.clicked.connect(self.select_fun3)
        self.layout.addWidget(self.returnbut, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.addfile,0 , 1)
        self.layout.addWidget(self.addmufile, 1, 0)
        self.layout.addWidget(self.addsystem,1,1)
        self.returnbut.setMaximumSize(a, b)
        self.addfile.setMaximumSize(a, b)
        self.addmufile.setMaximumSize(a, b)
        self.addsystem.setMaximumSize(a,b)

    def returnfun(self):
        dow = Course_news(self.data)
        #dow.changfun()
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,dow)

    def select_fun1(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'ppt(*.ppt *.pptx);;)')
        if not path:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')
            return
        end_file = os.path.splitext(path)[1]
        file = os.path.split(path)[1][:-len(end_file)]
        file1 = '../datas/tupian'
        fileNames = glob.glob(file1 + r'/*')
        if fileNames:
            for fileName in fileNames:
                os.remove(fileName)# 将pa 文件夹中的文件删除。
        if end_file == '.ppt' or end_file == '.pptx':
            self.ppt_to_pdf("../datas/wen/", path)
            pdf_path = "../datas/wen/" + file + '.pdf'
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
                    file1 = '../datas/tupian'
                    fileNames = glob.glob(file1 + r'/*')
                    if fileNames:
                        for fileName in fileNames:
                            # 将pa 文件夹中的文件删除。
                            os.remove(fileName)
                    if end_file == '.ppt' or end_file == '.pptx':
                        self.ppt_to_pdf("../datas/wen/", path)
                        pdf_path = "../datas/wen/" + file + '.pdf'
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
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,Add_System(self.data) )


    def save_date(self,data,file,total,total2,filename1,filename2):
        sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Filename")
        no = len(c.fetchall())
        c.execute("insert into Filename VALUES(?,?,?,?,?,?)",('C'+str(no),data[0],data[1],file,filename1,filename2))
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
            imageFormat = QtGui.QImage.Format_RGB888
            # 生成 QImage 对象
            pageQImage = QtGui.QImage(pagePixmap.samples, pagePixmap.width, pagePixmap.height, pagePixmap.stride,
                                      imageFormat)
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
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        re.search('-> (.*?) using filter', process.stdout.decode())

    def word_to_pdf(self, outfile, infile, timeout=None):
        """将ppt 转换为pdf
        函数说明:将路径为infile的ppt文件转换为pdf,保存进路径为outfile的pdf文件.
        参数: outfile(str):保存文件pdf 的路径.
        参数: infile(str):ppt文件的路径.
        参数: timeout:转换文件时的时间延迟.
        """
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', outfile, infile]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
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

#添加系统课件
class Add_System(QFrame):
    def __init__(self, data):
        super(Add_System, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data
        self.location = Select_location(self)
        self.returnbut = QPushButton("返回")
        self.doubleselect = QPushButton("重新选择")
        self.lab = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")

        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.doubleselect.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setMaximumSize(100, 40)
        self.doubleselect.setMaximumSize(100,40)
        self.lab.setMaximumSize(200, 40)
        self.returnbut.clicked.connect(self.returnfun)
        self.doubleselect.clicked.connect(self.doublefun)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.doubleselect,0,17,1,2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 1, 8, 17)
        self.location.show()

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,Addcufile(self.data))

    def surefun(self):
        self.qtool.removeItem(0)
        greade  = self.location.getgrade()
        course  = self.location.getcourse()
        self.window = AddsystemQlist(self, self.data,greade,course)
        self.qtool.addItem(self.window, "系统文件")

    def doublefun(self):
        self.location.fun2()
        self.location.show()

    def clicked(self):
        self.max = max_widget()
        self.max.show()

#添加系统课件的item 设计
class AddsystemWidget(QWidget):
    def __init__(self,dow,data,da):
        super(AddsystemWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.dow = dow
        self.data = data
        self.da = da
        self.imagelab = QLabel()
        self.addbut = QPushButton("添加")
        self.namelab = QLabel(da[0])
        self.image_path = "../datas/image/image" + da[4]
        total = base64.b64decode(da[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.addbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(800, 80)
        self.addbut.setMaximumSize(80,40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.addbut.clicked.connect(self.addfile)
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.addbut,3,8,1,1)

    def addfile(self):
        sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Filename")
        no = len(c.fetchall())
        c.execute("insert into Filename VALUES(?,?,?,?,?,?)",
                  ('C' + str(no), self.data[0], self.data[1], self.da[0], self.da[2], self.da[4]))
        c.execute("insert into Fileimage values(?,?)", ('C' + str(no), self.da[3]))
        c.execute("insert into Filedate values(?,?)", ('C' + str(no), self.da[1]))
        conn.commit()
        c.close()
        conn.close()
        QMessageBox.about(self, "提示", '添加成功!!')


#添加系统课件的QList
class AddsystemQlist(QListWidget):
    def __init__(self, dow, data,greade,course):
        super(AddsystemQlist, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        sqlpath = "../datas/database/Data.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        if greade[:3]=="一年级":
            c.execute("select name,First_Grade_data.total,First_Grade.filename, \
                            First_Grade_image.total,First_Grade_image.filename from \
                            First_Grade,First_Grade_data,First_Grade_image  where \
                            First_Grade.no = First_Grade_data.no and First_Grade.no =First_Grade_image.no \
                            and level2=(?) and level3=(?)",(greade,course))
        else:
            QMessageBox.about(self, "提示", '其他功能暂未实现!!')
        self.datas = c.fetchall()
        for da in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, AddsystemWidget(self,data,da))




    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index]
            zip_path = "../datas/wen/xinwen.zip"
            total = base64.b64decode(da[1])
            f = open(zip_path, 'wb')
            f.write(total)
            f.close()
            self.zip_to_files(zip_path)
            self.dow.clicked()

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

#选择添加系统课件的内容
class Select_location(QWidget):
    def __init__(self,dow):
        super(Select_location, self).__init__()
        self.dow = dow
        self.setWindowTitle("选择添加系统文件的内容")
        self.lab = QLabel("请选择添加系统文件的内容！！！！")
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
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
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
            return
        elif(self.typebox.currentText()==""):
            QMessageBox.about(self, "提示", '学习阶段的选项框不能为空!!')
            return
        elif (self.coursebox.currentText()==""):
            QMessageBox.about(self, "提示", '科目的选项框不能为空!!')
            return
        elif (self.greadebox.currentText()[:3]!="一年级"):
            QMessageBox.about(self, "抱歉", '目前只能添加小学一年级的课件!!')
            return
        else:
            self.close()
            self.dow.surefun()


    def gettype(self):
        return self.typebox.currentText()

    def getgrade(self):
        return self.greadebox.currentText()

    def getcourse(self):
        return self.coursebox.currentText()

#添加练习
class Addexfile(QFrame):
    def __init__(self, data):
        super(Addexfile, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data = data

        self.returnbut = QPushButton("返回")
        self.addfile = QPushButton("添加文件")
        self.addmufile = QPushButton("添加目录")
        self.addsystem = QPushButton("从系统添加")
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
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addfile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addmufile.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addsystem.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.clicked.connect(self.returnfun)
        self.addfile.clicked.connect(self.select_fun1)
        self.addmufile.clicked.connect(self.select_fun2)
        self.addsystem.clicked.connect(self.select_fun3)
        self.layout.addWidget(self.returnbut, 0, 0)  # 往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.addfile,0 , 1)
        self.layout.addWidget(self.addmufile, 1, 0)
        self.layout.addWidget(self.addsystem,1,1)
        self.returnbut.setMaximumSize(a, b)
        self.addfile.setMaximumSize(a, b)
        self.addmufile.setMaximumSize(a, b)
        self.addsystem.setMaximumSize(a,b)

    def returnfun(self):
        dow = Course_news(self.data)
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, dow)

    def select_fun1(self):
        QMessageBox.about(self, "提示", '抱歉！！\n该功能暂时未实现!!')


    def select_fun2(self):
        fname = QFileDialog.getExistingDirectory(self, 'open file', '/')
        if fname:
            try:
                files = glob.glob(fname + r'/*')
                pa = files[0]
                self.dow = Addexfilewin(self.data, fname)
                self.dow.show()
            except:
                QMessageBox.about(self, "提示", '您选择的文件夹没有任何文件!!')
        else:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')

    def select_fun3(self):
        QMessageBox.about(self, "提示", '抱歉！！\n该功能暂时未实现!!')


class Addexfilewin2(QWidget):
    def __init__(self,data,answer):
        super(Addexfilewin2, self).__init__()
        self.sure = QPushButton("保存")
        self.concle = QPushButton("取消")
        self.cutimage = QPushButton("上一题")
        self.addimage = QPushButton("下一题")
        self.imagelab = QLabel()
        self.answerlab = QLabel("答案")
        self.answerEdit = QLineEdit()
        self.analysislab = QLabel("解析")
        self.analysisEdit = QTextEdit()
        self.data = data
        lists = answer.split("@")
        self.answers = []
        for list in lists:
            da = list.split("#")
            self.answers.append(da)
        self.a = 0
        self.fname = '../datas/tupian'
        self.files = glob.glob(self.fname + r'/*')
        self.answer = []
        self.devise_Ui()



    def devise_Ui(self):
        self.resize(800, 500)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #窗口置顶

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.analysislab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.concle.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addimage.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.cutimage.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.answerEdit.setFont(QFont("宋体", 14))
        self.analysisEdit.setFont(QFont("宋体", 14))
        self.imagelab.setMaximumSize(400,250)
        self.cutimage.setMaximumSize(80,40)
        self.addimage.setMaximumSize(80,40)
        self.answerlab.setMaximumSize(80,40)
        self.analysislab.setMaximumSize(80,40)
        self.answerEdit.setMaximumSize(250,40)
        self.analysisEdit.setMaximumSize(250,180)
        self.pa = self.files[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.imagelab.setPixmap(pixmap)  # 在label上显示图片
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        for answer in self.answers:
            if answer[0]==self.filename:
                self.answerEdit.setText(answer[1])
                self.analysisEdit.setText(answer[2])
                self.answers.remove(answer)
        self.layout.addWidget(self.cutimage,0,1,1,1)
        self.layout.addWidget(self.addimage,0,9,1,1)
        self.layout.addWidget(self.answerlab,2,1,2,1)
        self.layout.addWidget(self.answerEdit,2,2,2,3)
        self.layout.addWidget(self.analysislab,4,1,2,1)
        self.layout.addWidget(self.analysisEdit,4,2,4,3)
        self.layout.addWidget(self.imagelab,3,6,4,4)
        self.layout.addWidget(self.sure, 11, 8, 1, 1)
        self.layout.addWidget(self.concle, 11, 9, 1, 1)
        self.addimage.clicked.connect(self.addfun)
        self.cutimage.clicked.connect(self.cutfun)
        self.concle.clicked.connect(self.conclefun)
        self.sure.clicked.connect(self.surefun)

    def addfun(self):
        text1 = self.answerEdit.text()
        text2 = self.analysisEdit.toPlainText()
        if len(text1)==0:
            QMessageBox.about(self, "提示", '您没有填写答案！！')
        elif len(text2)==0:
            QMessageBox.about(self, "提示", '您没有填写答案！！')
        else:
            self.a = self.a + 1
            try:
                self.pa = self.files[self.a]
                self.answer.append([self.filename,text1,text2])
                self.filename = os.path.split(self.pa)[1]
                b = 0
                for answer in self.answers:
                    if answer[0]==self.filename:
                        self.answerEdit.setText(answer[1])
                        self.analysisEdit.setText(answer[2])
                        self.answers.remove(answer)
                        b=1
                        break
                for answer in self.answer:
                    if answer[0]==self.filename:
                        self.answerEdit.setText(answer[1])
                        self.analysisEdit.setText(answer[2])
                        self.answer.remove(answer)
                        b=1
                        break
                if b==0:
                    self.answerEdit.setText("")
                    self.analysisEdit.setText("")
                pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
                self.imagelab.setPixmap(pixmap)  # 在label上显示图片
                self.imagelab.setScaledContents(True)  # 让图片自适应label大小
            except:
                self.a = self.a - 1
                QMessageBox.about(self, "提示", '这是最后一题了!!')

    def cutfun(self):
        text1 = self.answerEdit.text()
        text2 = self.analysisEdit.toPlainText()
        self.a = self.a - 1
        if self.a<0:
            self.a = self.a + 1
            QMessageBox.about(self, "提示", '这是第一题了!!')
        else:
            self.answer.append([self.filename, text1, text2])
            self.pa = self.files[self.a]
            self.filename = os.path.split(self.pa)[1]
            for answer in self.answer:
                if answer[0] == self.filename:
                    self.answerEdit.setText(answer[1])
                    self.analysisEdit.setText(answer[2])
                    self.answer.remove(answer)
                    break
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.imagelab.setScaledContents(True)  # 让图片自适应label大小

    def surefun(self):
        a = self.a + 1
        try:
            pa = self.files[a]
            QMessageBox.about(self, "提示", '请您把所有题目设置答案后才可以保存！！')
        except:
            text1 = self.answerEdit.text()
            text2 = self.analysisEdit.toPlainText()
            if len(text1) == 0:
                QMessageBox.about(self, "提示", '您没有填写答案！！')
            elif len(text2) == 0:
                QMessageBox.about(self, "提示", '您没有填写答案！！')
            else:
                self.answer.append([self.filename, text1, text2])
                sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
                conn = sqlite3.connect(sqlpath)
                c = conn.cursor()
                ab = []
                for da in self.answer:
                    str5 = "#".join(da)
                    ab.append(str5)
                str5 = "@".join(ab)
                c.execute("update Filename2 set answer=(?) where Cno=(?)",
                          (str5,self.data,))
                conn.commit()
                c.close()
                conn.close()
                self.close()

    def conclefun(self):
        self.close()


    def file_to_zip(self, path):  # 将文件夹压缩为压缩包。
        filepath ='../datas/tupian' + '.zip'
        if os.path.exists(filepath):
            os.remove(filepath)
        z = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()



class Addexfilewin(QWidget):
    def __init__(self,data,fname):
        super(Addexfilewin, self).__init__()
        self.sure = QPushButton("保存")
        self.concle = QPushButton("取消")
        self.cutimage = QPushButton("上一题")
        self.addimage = QPushButton("下一题")
        self.imagelab = QLabel()
        self.answerlab = QLabel("答案")
        self.answerEdit = QLineEdit()
        self.analysislab = QLabel("解析")
        self.analysisEdit = QTextEdit()
        self.data = data
        self.a = 0
        self.fname = fname
        self.files = glob.glob(fname + r'/*')
        self.filemu = os.path.split(fname)[1]
        self.answer = []
        self.devise_Ui()

    def devise_Ui(self):
        self.resize(800, 500)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #窗口置顶

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.analysislab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.concle.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.addimage.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.cutimage.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.answerEdit.setFont(QFont("宋体", 14))
        self.analysisEdit.setFont(QFont("宋体", 14))
        self.imagelab.setMaximumSize(400,250)
        self.cutimage.setMaximumSize(80,40)
        self.addimage.setMaximumSize(80,40)
        self.answerlab.setMaximumSize(80,40)
        self.analysislab.setMaximumSize(80,40)
        self.answerEdit.setMaximumSize(250,40)
        self.analysisEdit.setMaximumSize(250,180)
        self.pa = self.files[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.imagelab.setPixmap(pixmap)  # 在label上显示图片
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.cutimage,0,1,1,1)
        self.layout.addWidget(self.addimage,0,9,1,1)
        self.layout.addWidget(self.answerlab,2,1,2,1)
        self.layout.addWidget(self.answerEdit,2,2,2,3)
        self.layout.addWidget(self.analysislab,4,1,2,1)
        self.layout.addWidget(self.analysisEdit,4,2,4,3)
        self.layout.addWidget(self.imagelab,3,6,4,4)
        self.layout.addWidget(self.sure, 11, 8, 1, 1)
        self.layout.addWidget(self.concle, 11, 9, 1, 1)
        self.addimage.clicked.connect(self.addfun)
        self.cutimage.clicked.connect(self.cutfun)
        self.concle.clicked.connect(self.conclefun)
        self.sure.clicked.connect(self.surefun)

    def addfun(self):
        text1 = self.answerEdit.text()
        text2 = self.analysisEdit.toPlainText()
        if len(text1)==0:
            QMessageBox.about(self, "提示", '您没有填写答案！！')
        elif len(text2)==0:
            QMessageBox.about(self, "提示", '您没有填写答案！！')
        else:
            self.a = self.a + 1
            try:
                self.pa = self.files[self.a]
                self.answer.append([self.filename,text1,text2])
                self.filename = os.path.split(self.pa)[1]
                b = 0
                for answer in self.answer:
                    if answer[0]==self.filename:
                        self.answerEdit.setText(answer[1])
                        self.analysisEdit.setText(answer[2])
                        self.answer.remove(answer)
                        b=1
                        break
                if b==0:
                    self.answerEdit.setText("")
                    self.analysisEdit.setText("")
                pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
                self.imagelab.setPixmap(pixmap)  # 在label上显示图片
                self.imagelab.setScaledContents(True)  # 让图片自适应label大小
            except:
                self.a = self.a - 1
                QMessageBox.about(self, "提示", '这是最后一题了!!')

    def cutfun(self):
        text1 = self.answerEdit.text()
        text2 = self.analysisEdit.toPlainText()
        self.a = self.a - 1
        if self.a<0:
            self.a = self.a + 1
            QMessageBox.about(self, "提示", '这是第一题了!!')
        else:
            self.answer.append([self.filename, text1, text2])
            self.pa = self.files[self.a]
            self.filename = os.path.split(self.pa)[1]
            for answer in self.answer:
                if answer[0] == self.filename:
                    self.answerEdit.setText(answer[1])
                    self.analysisEdit.setText(answer[2])
                    self.answer.remove(answer)
                    break
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.imagelab.setScaledContents(True)  # 让图片自适应label大小

    def surefun(self):
        a = self.a + 1
        try:
            pa = self.files[a]
            QMessageBox.about(self, "提示", '请您把所有题目设置答案后才可以保存！！')
        except:
            text1 = self.answerEdit.text()
            text2 = self.analysisEdit.toPlainText()
            if len(text1) == 0:
                QMessageBox.about(self, "提示", '您没有填写答案！！')
            elif len(text2) == 0:
                QMessageBox.about(self, "提示", '您没有填写答案！！')
            else:
                self.answer.append([self.filename, text1, text2])
                self.file_to_zip(self.fname)
                filepath = '../datas/tupian' + '.zip'
                with open(filepath, "rb") as f:
                    total = base64.b64encode(f.read())  # 将文件转换为字节。
                f.close()
                filename1 = '.zip'
                sqlpath = "../datas/database/ControllerSQ" + str(win.number) + "L.db"
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
                          ('C' + str(no), self.data[0], self.data[1], self.filemu, str5, filename1,))
                c.execute("insert into Filedate2 values(?,?)", ('C' + str(no), total))
                conn.commit()
                c.close()
                conn.close()
                self.close()

    def conclefun(self):
        self.close()


    def file_to_zip(self, path):  # 将文件夹压缩为压缩包。
        filepath ='../datas/tupian' + '.zip'
        if os.path.exists(filepath):
            os.remove(filepath)
        z = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()






#添加课程
class AddCourse(QWidget):
    def __init__(self):
        super(AddCourse, self).__init__()
        self.sure = QPushButton("确认")
        self.concle = QPushButton("取消")
        self.courselab = QLabel("课程码:")
        self.namelab = QLabel("课程名:")
        self.chang_image = QPushButton("换一张")
        self.courselab2 = QLabel()
        self.tupian = QLabel()
        self.nameEdit = QLineEdit()
        self.devise_Ui()

    def devise_Ui(self):
        self.resize(800, 500)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #窗口置顶

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 0, 0, 0)
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.concle.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.chang_image.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.nameEdit.setPlaceholderText("请输入课程名")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.chang_image.setMaximumSize(70, 40)
        self.sure.setMaximumSize(60, 40)
        self.concle.setMaximumSize(60, 40)
        self.courselab.setMaximumSize(100, 40)

        self.namelab.setMaximumSize(100, 40)
        self.nameEdit.setMaximumSize(200, 40)
        self.tupian.setMaximumSize(250, 250)

        self.courselab2.setMaximumSize(200, 40)
        self.courselab2.setStyleSheet(
            "QLabel{color:rgb(125,175,250);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.layout.addWidget(self.tupian, 0, 0, 5, 5)
        self.layout.addWidget(self.chang_image, 5, 1, 1, 1)
        self.layout.addWidget(self.courselab, 1, 6, 1, 1)
        self.layout.addWidget(self.courselab2, 1, 7, 1, 3)
        self.layout.addWidget(self.namelab, 3, 6, 1, 1)
        self.layout.addWidget(self.nameEdit, 3, 7, 1, 3)
        self.layout.addWidget(self.sure, 6, 8, 1, 1)
        self.layout.addWidget(self.concle, 6, 9, 1, 1)
        self.image()
        self.sure.clicked.connect(self.sure_fun)
        self.chang_image.clicked.connect(self.chang_fun)
        self.concle.clicked.connect(self.conclefun)

    def image(self):
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select * from Course")
        b = len(c.fetchall())
        year = datetime.date.today().year
        self.Cno = str(year) + str(b)
        self.courselab2.setText(self.Cno)
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

    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def conclefun(self):
        self.close()

    def save_data(self):
        name = self.nameEdit.text()
        filename = os.path.splitext(self.image_path)[1]
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO Course VALUES(?,?,?)", (self.Cno, name, 0,))
        conn.execute("INSERT INTO Course_image VALUES(?,?,?)", (self.Cno, total, filename,))
        conn.execute("INSERT INTO Teacher_Course VALUES(?,?)", (win.number, self.Cno,))
        conn.commit()
        conn.close()


    def sure_fun(self):
        if len(self.nameEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "课程名不能为空！！")
            self.nameEdit.setFocus()
        else:
            self.save_data()
            self.close()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Class_news())

#统计信息
class Statistics_news(QFrame):
    def __init__(self):
        super(Statistics_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnbut = QPushButton("返回")
        self.lab = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window = Statisticswindow(self)
        self.qtool.addItem(self.window, '我的课程')

        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")

        self.returnbut.setMaximumSize(100, 40)

        self.lab.setMaximumSize(200, 40)
        self.returnbut.clicked.connect(self.returnfun)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 0, 8, 19)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def clicked(self, data):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Statistics_class(data))

class StatisticsWidget(QWidget):
    def __init__(self, data):
        super(StatisticsWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.numlab = QLabel("人数:")
        self.numlab2 = QLabel(str(data[2]))
        self.image_path = "../datas/image/image" + data[4]
        total = base64.b64decode(data[3])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.numlab.setMaximumSize(80, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)

class Statisticswindow(QListWidget):
    def __init__(self, dow):
        super(Statisticswindow, self).__init__()
        self.dow = dow
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,name,numble,total,filename \
                  from Course,Course_image,Teacher_Course \
                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                    and number=(?)", (win.number,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, StatisticsWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:2]
            self.dow.clicked(da)

class Statistics_class(QFrame):
    def __init__(self,data):
        super(Statistics_class, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnbut = QPushButton("返回")
        self.select_query = QComboBox()
        self.query = QLineEdit()
        self.search = QPushButton("搜索")
        self.data = data
        self.lab = QLabel()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.qtool = QToolBox()
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.window = classwindow(self,self.data[0])
        self.qtool.addItem(self.window, "学生学习信息")
        self.select_query.addItems(['号码','姓名'])
        self.select_query.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.search.setStyleSheet("QPushButton{ font-family:'宋体';font-size:20px;color:rgb(0,0,0);}\
                                         QPushButton{background-color:rgb(170,200, 50)}\
                                         QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnbut.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.query.setPlaceholderText("请输入搜索内容")
        self.query.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.returnbut.setMaximumSize(100, 40)
        self.select_query.setMaximumSize(80, 40)
        self.query.setMaximumSize(350, 40)
        self.search.setMaximumSize(80, 40)
        self.lab.setMaximumSize(200, 40)
        self.returnbut.clicked.connect(self.returnfun)
        self.search.clicked.connect(self.chang_fun)
        self.layout.addWidget(self.select_query, 0, 10, 1, 1)
        self.layout.addWidget(self.query, 0, 11, 1, 5)
        self.layout.addWidget(self.search, 0, 16, 1, 1)
        self.layout.addWidget(self.returnbut, 0, 0, 1, 2)
        self.layout.addWidget(self.lab, 1, 1, 1, 7)
        self.layout.addWidget(self.qtool, 2, 0, 8, 19)

    def returnfun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Statistics_news())


    def clicked(self, data1,data2):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_report(data1,data2))

    def chang_fun(self):
        if (self.select_query.currentText() == '号码'):
            no = self.query.text()
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where Cno=(?) and number=(?)",(self.data[0],no,))
            self.datas = c.fetchall()
            if len(self.datas)>0:
                self.qtool.removeItem(0)
                self.coursewin = classwindow2(self,self.data[0],no)
                self.qtool.addItem(self.coursewin, '查找的学生')
                self.query.setText("")
            else:
                QMessageBox.about(self, "抱歉!", "没有找到号码为:'"+no+"'的信息!!!")
        elif (self.select_query.currentText() == '姓名'):
            no = self.query.text()
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course,User_date where\
                 Join_Course.number=User_date.number and Cno=(?) and name like (?)", (self.data[0],'%'+no+'%',))
            self.datas = c.fetchall()
            if len(self.datas)>0:
                self.qtool.removeItem(0)
                self.coursewin = classwindow3(self,self.data[0],'%'+no+'%')
                self.qtool.addItem(self.coursewin, '查找的学生')
                self.query.setText("")
            else:
                QMessageBox.about(self, "抱歉!", "没有找到号码为:'"+no+"'的信息!!!")

class classWidget(QWidget):
    def __init__(self, data):
        super(classWidget, self).__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.namelab = QLabel(data[1])
        self.courselab = QLabel("加课天数:")
        self.joinlab = QLabel("学习用时:")
        self.numlab = QLabel("平均学习:")
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(data[2], abcd)
        a = (new - a1).days + 1
        self.courselab2 = QLabel(str(a)+"　天")
        ab = data[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.joinlab2 = QLabel(ac)
        ad = ab / a
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.numlab2 = QLabel(ae)
        self.image_path = "../datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.joinlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.courselab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.joinlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.courselab.setMaximumSize(80, 40)
        self.joinlab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80, 40)
        self.courselab2.setMaximumSize(100, 40)
        self.joinlab2.setMaximumSize(100, 40)
        self.numlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.courselab, 1, 8, 1, 1)
        self.layout.addWidget(self.joinlab, 2, 8, 1, 1)
        self.layout.addWidget(self.numlab, 3, 8, 1, 1)
        self.layout.addWidget(self.courselab2, 1, 9, 1, 2)
        self.layout.addWidget(self.joinlab2, 2, 9, 1, 2)
        self.layout.addWidget(self.numlab2, 3, 9, 1, 2)

class classwindow(QListWidget):
    def __init__(self, dow,data1):
        super(classwindow, self).__init__()
        self.dow = dow
        self.data = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?)", (data1,data1,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data)

class classwindow2(QListWidget):
    def __init__(self, dow,data1,data2):
        super(classwindow2, self).__init__()
        self.dow = dow
        self.data1 = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?) \
                     and Join_Course.number=(?)", (data1,data1,data2,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data1)

class classwindow3(QListWidget):
    def __init__(self, dow,data1,data2):
        super(classwindow3, self).__init__()
        self.dow = dow
        self.data1 = data1
        self.doubleClicked.connect(self.opencourse)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Coursetime.number,name,jointime,time,total,filename \
                  from Coursetime,Join_Course,User_date,User_image \
                   where Join_Course.number=Coursetime.number and \
                    Coursetime.number=User_date.number and Coursetime.number=User_image.number \
                    and Coursetime.Cno=(?) and Join_Course.Cno=(?) \
                     and User_date.name like (?)", (data1,data1,data2,))
        self.datas = c.fetchall()
        for data in self.datas:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(800, 150))
            item.setBackground(QColor(240, 240, 240))
            self.setItemWidget(item, classWidget(data))

    def opencourse(self):
        index = self.currentIndex().row()
        if index > -1:
            da = self.datas[index][:4]
            self.dow.clicked(da,self.data1)

class Usr_report(QFrame):
    def __init__(self,data1,data2):
        super(Usr_report, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.da1 = data1
        self.da2 = data2
        self.returnBtn = QPushButton("返回")
        self.day = QLabel("学习天数:")
        self.learntime = QLabel("学习总时长:")
        self.avglearn = QLabel("日均学习:")
        self.table = QTableWidget()
        self.devise_Ui()
        self.information()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        #        self.layout.setContentsMargins (300, 0, 0, 0)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                         QPushButton{background-color:rgb(170,200, 50)}\
                                         QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.day.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learntime.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.returnBtn.setMaximumSize(60, 40)
        self.day.setMaximumSize(120, 40)
        self.learntime.setMaximumSize(130, 40)
        self.avglearn.setMaximumSize(120, 40)
        self.returnBtn.clicked.connect(self.return_fun)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.day, 0, 3, 1, 1)
        self.layout.addWidget(self.learntime, 0, 6, 1, 1)
        self.layout.addWidget(self.avglearn, 0, 9, 1, 1)

    def information(self):
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(self.da1[2], abcd)
        a = (new - a1).days + 1
        self.day1 = QLabel(str(a) + "天")
        ab = self.da1[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.learntime1 = QLabel(ac)
        ad = ab / a
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.avglearn1 = QLabel(ae)
        self.day1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.learntime1.setStyleSheet(
            "QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.table.setStyleSheet("QTableWidget{background-color:rgb(255,255,255);font:13pt '宋体';font-weight:Bold;};");
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        sqlpath = "../datas/database/SQ" + self.da1[0] + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_data where Cno=(?)",(self.da2,))
        data = c.fetchall()
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
        self.day1.setMaximumSize(150, 40)
        self.learntime1.setMaximumSize(150, 40)
        self.avglearn1.setMaximumSize(150, 40)
        self.layout.addWidget(self.day1, 0, 4, 1, 1)
        self.layout.addWidget(self.learntime1, 0, 7, 1, 1)
        self.layout.addWidget(self.avglearn1, 0, 10, 1, 1)
        self.layout.addWidget(self.table, 3, 0, 1, 12)

    def return_fun(self):
        da = [self.da2,self.da1[1]]
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Statistics_class(da))

# 管理员我的界面
class Controller_myself(QFrame):  # 增加一个编辑资料的按钮
    def __init__(self):
        super(Controller_myself, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnBtn = QPushButton("返回")
        self.ExditBtn = QPushButton("编辑")
        self.chang_image = QPushButton("换头像")
        self.name = QLabel("姓名:")
        self.sex = QLabel("性别:")
        self.number = QLabel("手机号:")
        self.year = QLabel("出生年月:")
        self.school = QLabel("学校:")
        self.amend = QPushButton("修改密码")
        self.withdraw = QPushButton('退出')
        self.tupian = QLabel()
        self.devise_ui()

    def devise_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.layout.setContentsMargins(100, 0, 0, 0)

        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)",(win.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.name1 = QLabel(self.data[1])  # 读取数据库中的信息，将信息输出label中
        self.sex1 = QLabel(self.data[3])
        self.number1 = QLabel(self.data[0])
        self.year1 = QLabel(self.data[2][0:4] + "年 " + self.data[2][5:] + ' 月')
        self.school1 = QLabel(self.data[4])
        self.returnBtn.setMaximumSize(60, 40)
        self.ExditBtn.setMaximumSize(60, 40)
        self.name.setMaximumSize(70, 40)
        self.sex.setMaximumSize(70, 40)
        self.number.setMaximumSize(70, 40)
        self.school.setMaximumSize(70, 40)
        self.year.setMaximumSize(100, 40)
        self.name1.setMaximumSize(350, 40)
        self.sex1.setMaximumSize(350, 40)
        self.number1.setMaximumSize(350, 40)
        self.school1.setMaximumSize(350, 40)
        self.year1.setMaximumSize(350, 40)
        self.amend.setMaximumSize(500, 40)
        self.withdraw.setMaximumSize(500, 40)
        self.chang_image.setMaximumSize(90, 40)
        self.tupian.setMaximumSize(250, 250)
        self.chang_image.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.withdraw.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.ExditBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.name1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.year1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school1.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.withdraw.clicked.connect(self.return_win)
        self.returnBtn.clicked.connect(self.return_fun)
        self.ExditBtn.clicked.connect(self.edit_fun)
        self.chang_image.clicked.connect(self.chang_fun)
        self.amend.clicked.connect(self.amend_fun)
        self.layout.addWidget(self.tupian, 1, 1, 4, 4)
        self.layout.addWidget(self.chang_image, 5, 2, 1, 2)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.ExditBtn, 0, 10, 1, 1)
        self.layout.addWidget(self.name, 1, 6, 1, 1)
        self.layout.addWidget(self.name1, 1, 8, 1, 6)
        self.layout.addWidget(self.year, 2, 6, 1, 1)
        self.layout.addWidget(self.year1, 2, 8, 1, 6)
        self.layout.addWidget(self.sex, 3, 6, 1, 1)
        self.layout.addWidget(self.sex1, 3, 8, 1, 6)
        self.layout.addWidget(self.number, 4, 6, 1, 1)
        self.layout.addWidget(self.number1, 4, 8, 1, 6)
        self.layout.addWidget(self.school, 5, 6, 1, 1)
        self.layout.addWidget(self.school1, 5, 8, 1, 6)
        self.layout.addWidget(self.amend, 7, 6, 1, 6)
        self.layout.addWidget(self.withdraw, 8, 6, 1, 6)
        self.image()

    def image(self):
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_image where number=(?)", (win.number,))
        data = c.fetchall()[0]
        c.close()
        conn.close()
        self.image_path = "../datas/image/image" + data[2]
        total = base64.b64decode(data[1])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.tupian.setPixmap(QPixmap(self.image_path))
        self.tupian.setScaledContents(True)  # 让图片自适应label大小
        QApplication.processEvents()

    def chang_fun(self):
        path, _ = QFileDialog.getOpenFileName(self, '请选择文件',
                                              '/', 'image(*.jpg)')
        if path:
            self.file = os.path.splitext(path)[1]
            self.tupian.setPixmap(QPixmap(path))
            self.tupian.setScaledContents(True)  # 让图片自适应label大小
            with open(path, "rb") as f:
                total = base64.b64encode(f.read())  # 将文件转换为字节。
            f.close()
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            conn.execute("update Controller_image set total = (?),filename = (?) where number = (?)",
                         (total, self.file, win.number))
            conn.commit()
            conn.close()
        else:
            self.image()


    def amend_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_amend())

    def return_win(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Logon())

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Function())

    def edit_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_informent1())

# 管理员修改密码

class Controller_amend(QFrame):
    def __init__(self):
        super(Controller_amend, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.usrlab1 = QLabel(win.number)
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
        self.amendedit1.setPlaceholderText("请输入原密码")
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
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.returnBtn.setMaximumSize(60, 40)
        self.returnBtn.clicked.connect(self.return_fun)
        self.amendedit1.returnPressed.connect(self.enterPress1)
        self.amendedit2.returnPressed.connect(self.enterPress2)
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
        win.splitter.insertWidget(0, Controller_myself())

    def enterPress1(self):
        if len(self.amendedit1.text()) == 0:
            QMessageBox.about(self, "提示!", "原密码没有填写")
            self.amendedit1.setFocus()
        else:
            self.amendedit2.setFocus()

    def enterPress2(self):
        if len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        else:
            self.amendedit3.setFocus()

    def accept(self):
        if len(self.amendedit1.text()) == 0:
            QMessageBox.about(self, "提示!", "原密码没有填写")
            self.amendedit1.setFocus()
        elif len(self.amendedit2.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit2.setFocus()
        elif len(self.amendedit3.text()) == 0:
            QMessageBox.about(self, "提示!", "新密码框不能为空！")
            self.amendedit3.setFocus()
        elif self.amendedit3.text() != self.amendedit2.text():
            QMessageBox.about(self, "提示!", "前后密码输入不一样！")
            self.amendedit3.setFocus()
        else:
            sqlpath = '../datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Controller")
            sign = 0
            for variate in c.fetchall():
                if variate[0] == win.number and variate[2] == self.amendedit1.text():
                    conn.execute("update Controller set password=(?) where number=(?)", (self.amendedit2.text(), variate[0],))
                    conn.commit()
                    sign = 1
                    break
            c.close()
            conn.close()
            if sign == 0:
                QMessageBox.about(self, "提示!", "原密码输入错误！！")
                self.amendedit1.setFocus()
            else:
                QMessageBox.about(self, "提示!", "修改成功！！")
                time.sleep(1)
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Controller_myself())

# 管理员我的编辑信息
class Controller_informent1(QFrame):
    def __init__(self):
        super(Controller_informent1, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sure = QPushButton("确认")
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
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:26px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")

        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
        self.school.setMaximumSize(50, 40)
        self.returnBtn.setMaximumSize(60, 40)
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
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller_data where number=(?)", (win.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()
        self.sexcb.setCurrentText(self.data[3])  # 设置文本的默认选项
        self.yearcb.addItems(yearnb)
        self.yearcb.setCurrentText(self.data[2][0:4])  # 设置文本的默认选项
        self.monthcb.addItems(monthmb)
        self.monthcb.setCurrentText(self.data[2][5:7])  # 设置文本的默认选项
        self.nameEdit.setText(self.data[1])
        self.schoolEiit.setText(self.data[4])
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 4, 1, 18)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 4, 1, 18)
        self.layout.addWidget(self.year, 3, 3, 1, 1)
        self.layout.addWidget(self.yearcb, 3, 4, 1, 8)
        self.layout.addWidget(self.monthcb, 3, 9, 1, 7)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 4, 1, 18)
        self.layout.addWidget(self.sure, 5, 4, 1, 18)
        self.sure.clicked.connect(self.connect_fun)
        self.returnBtn.clicked.connect(self.return_fun)

    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_myself())

    def save_data(self):
        a = self.nameEdit.text()
        b = self.yearcb.currentText() + '-' + self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        sqlpath = '../datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("update Controller_data set name =(?),birthday=(?),sex=(?),school=(?) where number=(?)",
                     (a, b, c, d, win.number))
        conn.commit()
        conn.close()

    def connect_fun(self):
        win.splitter.widget(0).setParent(None)
        self.save_data()
        Controller_myself().devise_ui()
        win.splitter.insertWidget(0, Controller_myself())

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



# 主函数
if __name__ == "__main__":
    found_sql()
    app = QApplication(sys.argv)
    win = QUnFrameWindow()
    win.show()
    sys.exit(app.exec_())


