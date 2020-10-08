from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5 import QtCore, QAxContainer, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os,sys, time
import glob
import random
import base64
#from datetime import  datetime, timedelta
import  datetime
from bs4 import BeautifulSoup
from docx import Document
from win32com import client
import fitz
import sqlite3
import requests
import zipfile
import shutil
from PIL import Image
from docx.shared import Pt
from PIL import ImageFont, ImageDraw


class QTitleLabel(QLabel):
    """
    新建标题栏标签类
    """
    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setFixedHeight(30)

class QTitleButton(QPushButton):
    """
    新建标题栏按钮类
    """
    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFont(QFont("Webdings")) # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFixedWidth(40)

class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """
    def __init__(self):   #设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None, Qt.FramelessWindowHint) # 设置为顶级窗口，无边框
        self._padding = 5 # 设置边界宽度为5
        self.initTitleLabel() # 安放标题栏标签
        self.setWindowTitle = self._setTitleText(self.setWindowTitle) # 用装饰器将设置WindowTitle名字函数共享到标题栏标签上
        self.setWindowTitle("low(**_**)")
        self.initLayout() # 设置框架布局
        self.desktop = QApplication.desktop() #获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.setMinimumWidth(670)
        self.setMinimumHeight(560)
        self.resize(self.x, self.y)
        self.setMouseTracking(True) # 设置widget鼠标跟踪
        self.initDrag() # 设置鼠标跟踪判断默认值
        self.grade = ''    #保存用户年级
        self.numble = ''  #保存用户密码
        self.data = []   #保存用户我的信息
        self.data1=[]   #保存用户学习报告信息
        self.time1 = [] #保存用户登录时间
        self.time2 = [] 
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins (10,40, 10, 10)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.resize(self.x-20, self.y-60)
        self.splitter.move(10, 50)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.choice_status = Choice_status()   #选择身份界面 
        self.splitter.addWidget(self.choice_status) 
        


    
    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def initTitleLabel(self):  # 安放标题栏标签
        
        self._TitleLabel = QTitleLabel(self)
        self._TitleLabel.setMouseTracking(True) # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self._TitleLabel.setIndent(10) # 设置标题栏文本缩进
        self._TitleLabel.move(0, 0) # 标题栏安放到左上角

    def initLayout(self):    # 设置框架布局
        # 设置框架布局
        self._MainLayout = QVBoxLayout()
        self._MainLayout.setSpacing(0)
        self._MainLayout.addWidget(QLabel(), Qt.AlignLeft) # 顶一个QLabel在竖放框架第一行，以免正常内容挤占到标题范围里
        self._MainLayout.addStretch()
        self.setLayout(self._MainLayout)

    def addLayout(self, QLayout):
        # 给widget定义一个addLayout函数，以实现往竖放框架的正确内容区内嵌套Layout框架
        self._MainLayout.addLayout(QLayout)

    def _setTitleText(self, func):  # 设置标题栏标签的装饰器函数
        # 设置标题栏标签的装饰器函数
        def wrapper(*args):
            self._TitleLabel.setText(*args)
            return func(*args)
        return wrapper

    def setTitleAlignment(self, alignment):
        # 给widget定义一个setTitleAlignment函数，以实现标题栏标签的对齐方式设定
        self._TitleLabel.setAlignment(alignment | Qt.AlignVCenter)

    def setCloseButton(self, bool):  # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setToolTip("关闭窗口")
            self._CloseButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.closemainwin) # 按钮信号连接到关闭窗口的槽函数
    
    def closemainwin(self):  #关闭程序
        self.close()
        sys.exit()

    def setMinMaxButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setToolTip("最小化")
            self._MinimumButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized) # 按钮信号连接到最小化窗口的槽函数
            self._MaximumButton = QTitleButton(b'\xef\x80\xb1'.decode("utf-8"), self)
            self._MaximumButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MaximumButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._MaximumButton.clicked.connect(self._changeNormalButton) # 按钮信号连接切换到恢复窗口大小按钮函数

    def _changeNormalButton(self):    # 切换到恢复窗口大小按钮
        # 切换到恢复窗口大小按钮
        try:
            self.showMaximized() # 先实现窗口最大化
            self._MaximumButton.setText(b'\xef\x80\xb2'.decode("utf-8")) # 更改按钮文本
            self._MaximumButton.setToolTip("恢复") # 更改按钮提示
            self._MaximumButton.disconnect() # 断开原本的信号槽连接
            self._MaximumButton.clicked.connect(self._changeMaxButton) # 重新连接信号和槽
        except:
            pass

    def _changeMaxButton(self):    # 切换到最大化按钮
        # 切换到最大化按钮
        try:
            self.showNormal()
            self._MaximumButton.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.disconnect()
            self._MaximumButton.clicked.connect(self._changeNormalButton)
        except:
            pass

    def resizeEvent(self, QResizeEvent):  # 自定义窗口调整大小事件
        # 自定义窗口调整大小事件
        self._TitleLabel.setFixedWidth(self.width()) # 将标题标签始终设为窗口宽度
        # 分别移动三个按钮到正确的位置
        try:
            self._CloseButton.move(self.width() - self._CloseButton.width(), 0)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 3 + 1, 0)
        except:
            pass
        try:
            self._MaximumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 + 1, 0)
        except:
            pass
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                           for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                         for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                    for y in range(self.height() - self._padding, self.height() + 1)]
        
        
    def mousePressEvent(self, event):   # 重写鼠标点击的事件
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self._TitleLabel.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()
       

    def mouseMoveEvent(self, QMouseEvent):  # 判断鼠标位置切换鼠标手势
        # 判断鼠标位置切换鼠标手势
        if QMouseEvent.pos() in self._corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标释放后，各扳机复位
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

  

 

 
#选择身份界面 
class Choice_status(QFrame):
    def __init__(self):
        super(Choice_status, self).__init__()
        #self.setStyleSheet("background-color:white;")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.prompt = QLabel("\t   请  选  择  身  份  登  录")
        self.Controller = QPushButton("管理员")
        self.user  = QPushButton("用户")
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.prompt.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:28px;font-weight:Bold;font-family:Arial;}")
        self.prompt.setMaximumSize(700, 70)
        self.Controller.setStyleSheet("QPushButton{ font-family:'宋体';font-size:26px;color:rgb(0,0,0,255);}")
        self.Controller.setMaximumSize(700, 70)
        self.user.setStyleSheet("QPushButton{ font-family:'宋体';font-size:26px;color:rgb(0,0,0,255);}")
        self.user.setMaximumSize(700, 70)
        self.Controller.clicked.connect(self.change_choice_status1)  #连接管理员登录界面
        self.user.clicked.connect(self.change_choice_status2)      #连接用户登录界面
        self.layout.addWidget(self.prompt, 0, 0)
        self.layout.addWidget(self.Controller, 1, 0)
        self.layout.addWidget(self.user, 2, 0)
    
    def change_choice_status1(self):   #连接管理员登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_record())
        
    def change_choice_status2(self):    #连接用户登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_record())
    



#管理员注册界面
class Controller_logon(QFrame):
    def __init__(self):
        super(Controller_logon, self).__init__()
        #a = Usr_record().usrLineEdit.text()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.usr2 =  QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.pwd3 = QLabel("确认密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.pwdLineEdit3 = QLineEdit()
        self.codeLineEdit1 = QLineEdit()
        self.okBtn1 = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        self.pwd3.setMaximumSize(80, 40)
        #设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.pwd3.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit3.setMaximumSize(420, 40)
        self.codeLineEdit1.setMaximumSize(310, 40)
        #self.usrLineEdit2.setText(a)
        self.usrLineEdit2.setPlaceholderText("请输入手机号码")
        self.pwdLineEdit2.setPlaceholderText("请输入密码")
        self.pwdLineEdit3.setPlaceholderText("请重新输入密码")
        self.codeLineEdit1.setPlaceholderText("请输入右侧的验证码")
        self.usrLineEdit2.setFont(QFont("宋体" , 12))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体" , 12))
        self.pwdLineEdit3.setFont(QFont("宋体" , 12))
        self.codeLineEdit1.setFont(QFont("宋体" , 12))
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit3.setEchoMode(QLineEdit.Password)
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn1.setMaximumSize(420, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLineEdit2.returnPressed.connect(self.enterPress1)  #输入结束后按回车键跳到下一个控件
        self.pwdLineEdit2.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit3.returnPressed.connect(self.enterPress3)
        self.returnBtn.clicked.connect(self.change_choice_status1)  #点击返回键连接管理员登录界面
        self.codeLineEdit1.returnPressed.connect(self.accept)   #管理员忘记密码登录
        self.okBtn1.clicked.connect(self.accept)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr2, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 1, 5, 1, 14)
        self.layout.addWidget(self.pwd2, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 2, 5, 1, 14)
        self.layout.addWidget(self.pwd3, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit3, 3, 5,1, 14 )
        self.layout.addWidget(self.codeLineEdit1, 4, 5, 1, 5)
        self.layout.addWidget(self.codebel, 4, 10, 1, 6)
        self.layout.addWidget(self.okBtn1, 5, 5, 1, 14)
        self.renovate_code()
     
    def renovate_code(self):
        self.code = ''
        for num in range(1,7):
            self.code = self.code + str(random.randint(0, 9))
        im = Image.new("RGB", (100, 40), (255, 255, 255))     #将验证码转换为图片
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "E:/python/Qt/MSYH.ttf"), 18)  
        dr.text((10, 5), self.code, font=font, fill="#000000")
        im.save("E:/python/Qt/t.png")
        self.codebel.setPixmap(QPixmap("E:/python/Qt/t.png"))
    
    def checking1(self):  #注册时输入的号码检验是否已经注册过的
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                return True
        c.close()
        conn.close()
        return False
    
    def checking2(self):  #登录时密码在数据库中保存过来
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        a = self.usrLineEdit2.text()
        b = self.pwdLineEdit2.text()
        self.sql = c
        conn.execute("INSERT INTO Controller VALUES(?,?)",(a, b))
        conn.commit()	
        conn.close()
        


    def enterPress1(self):  #注册-》用户框回车确定时判断文字框是否有输入
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您登录！" )
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_record())
        else:
            self.pwdLineEdit2.setFocus()
    
    def enterPress2(self):  #注册-》密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        else:
            self.pwdLineEdit3.setFocus()
     
    def enterPress3(self):   #注册-》确认密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        else:
            self.codeLineEdit1.setFocus()
    

    
    def accept(self):#注册时将账号密码保存并登录。
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        elif len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        elif self.code !=self.codeLineEdit1.text():
            QMessageBox.about(self, "提示!", "验证码输入错误" )
            self.codeLineEdit1.setFocus()
        else:
            self.checking2()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_function())
            #连接主窗口界面。

    def change_choice_status1(self):   #连接管理员登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_record())


#管理员登录界面
class Controller_record(QFrame):
    def __init__(self):
        super(Controller_record, self).__init__()
        #self.setStyleSheet("background-color:white;")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr1 = QLabel("用户：")
        self.pwd1 = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.okBtn = QPushButton("登录")
        self.returnBtn = QPushButton("返回")
        self.forgetbtn = QLabel( )
        self.logonbtn = QLabel()
        self.devise_Ui()
        self.found_sql()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (350, 0, 0, 0)
        
        self.usr1.setMaximumSize(60, 60)
        #设置QLabel 的字体颜色，大小，
        self.usr1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.pwd1.setMaximumSize(60, 60)
        #设置QLabel 的字体颜色，大小，
        self.pwd1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrLineEdit.setPlaceholderText("请输入手机号码")
        self.usrLineEdit.setMaximumSize(400, 40)
        self.usrLineEdit.setFont(QFont("宋体" , 16))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(400, 40)
        self.pwdLineEdit.setPlaceholderText("请输入密码") 
        self.pwdLineEdit.setFont(QFont("宋体" , 16))
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn.setMaximumSize(400, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.forgetbtn.setText("<A href='www.baidu.com'>忘记密码</a>")
        self.logonbtn.setText("<A href='www.baidu.com'>注册</a>")
        self.forgetbtn.setStyleSheet("QLabel{color:rgb(0,0,255,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.logonbtn.setStyleSheet("QLabel{color:rgb(0,0,255,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.forgetbtn.setMaximumSize(90, 50)
        self.logonbtn.setMaximumSize(50, 50)
        self.pwdLineEdit.returnPressed.connect(self.accept)    #管理员登录
        self.okBtn.clicked.connect(self.accept)  
        self.forgetbtn.linkActivated.connect(self.controller_forgetbtn1)   #连接管理员忘记密码界面
        self.logonbtn.linkActivated.connect(self.controller_logonbtn1)   #连接管理员注册界面
        self.returnBtn.clicked.connect(self.change_controller_record1)  #点击返回键连接选择身份界面
        self.usrLineEdit.returnPressed.connect(self.enterPress1)  #输入结束后按回车键跳到下一个控件
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr1, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 1, 4, 1, 19)
        self.layout.addWidget(self.pwd1, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 2, 4, 1, 19)
        self.layout.addWidget(self.okBtn, 3, 4, 1, 19)
        self.layout.addWidget(self.forgetbtn, 4, 4, 1, 2)
        self.layout.addWidget(self.logonbtn, 4, 12, 1, 2)

    def change_controller_record1(self):   #点击返回键连接选择身份界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Choice_status())            
    
    def controller_forgetbtn1(self):   #连接管理员忘记密码界面
        win.splitter.widget(0).setParent(None)
        Controller_forget().renovate_code()
        win.splitter.insertWidget(0, Controller_forget())
    
    def controller_logonbtn1(self):    #连接管理员注册界面
        win.splitter.widget(0).setParent(None)
        Controller_logon().renovate_code()
        win.splitter.insertWidget(0, Controller_logon())
    

    
    
    def found_sql(self):   #创建保存用户信息的数据库
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        try:
            c.execute('''CREATE TABLE Controller(numble text,password text)''')	
        except:
            pass
        c.close()
        conn.close()
    
    def checking1(self):  #登录时检验号码是否没有注册
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit.text() :
                return False
        c.close()
        conn.close()
        return True
    def enterPress1(self):  #登录回车确定时判断文字框是否有输入
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！" )
        else:
            self.pwdLineEdit.setFocus()
            
    def accept(self):         #登录时判断密码是否正确
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit.setFocus()
        elif len(self.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit.setFocus()
        else:
            sqlpath ='D:/项目数据库/数据库/Information.db'
            conn=sqlite3.connect(sqlpath)
            c=conn.cursor()
            c.execute("select * from Controller")
            d =0
            for variate in c.fetchall():
                if variate[0]==self.usrLineEdit.text() and variate[1]== self.pwdLineEdit.text():
                    self.sql = variate[2]
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Controller_function())
                
            #连接主界面函数

#管理员忘记密码
class Controller_forget(QFrame):
    def __init__(self):
        super(Controller_forget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr2 =  QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.pwd3 = QLabel("确认密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.pwdLineEdit3 = QLineEdit()
        self.codeLineEdit1 = QLineEdit()
        self.okBtn1 = QPushButton("确认")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        self.pwd3.setMaximumSize(80, 40)
        #设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.pwd3.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit3.setMaximumSize(420, 40)
        self.codeLineEdit1.setMaximumSize(310, 40)
        #self.usrLineEdit2.setText(a)
        self.usrLineEdit2.setPlaceholderText("请输入手机号码")
        self.pwdLineEdit2.setPlaceholderText("请输入新的密码")
        self.pwdLineEdit3.setPlaceholderText("请重新输入新的密码")
        self.codeLineEdit1.setPlaceholderText("请输入右侧的验证码")
        self.usrLineEdit2.setFont(QFont("宋体" , 12))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体" , 12))
        self.pwdLineEdit3.setFont(QFont("宋体" , 12))
        self.codeLineEdit1.setFont(QFont("宋体" , 12))
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit3.setEchoMode(QLineEdit.Password)
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn1.setMaximumSize(420, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLineEdit2.returnPressed.connect(self.enterPress1)  #输入结束后按回车键跳到下一个控件
        self.pwdLineEdit2.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit3.returnPressed.connect(self.enterPress3)
        self.returnBtn.clicked.connect(self.change_choice_status1)  #点击返回键连接管理员登录界面
        self.codeLineEdit1.returnPressed.connect(self.accept)   #管理员忘记密码登录
        self.okBtn1.clicked.connect(self.accept)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr2, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 1, 5, 1, 14)
        self.layout.addWidget(self.pwd2, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 2, 5, 1, 14)
        self.layout.addWidget(self.pwd3, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit3, 3, 5,1, 14)
        self.layout.addWidget(self.codeLineEdit1, 4, 5, 1, 5)
        self.layout.addWidget(self.codebel, 4, 10, 1, 6)
        self.layout.addWidget(self.okBtn1, 5, 5, 1, 14)
        self.renovate_code()
      
    def renovate_code(self):  
        self.code = ''
        for num in range(1,7):
            self.code = self.code + str(random.randint(0, 9))
        im = Image.new("RGB", (100, 40), (255, 255, 255))     #将验证码转换为图片
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "E:/python/Qt/MSYH.ttf"), 18)  
        dr.text((10, 5), self.code, font=font, fill="#000000")
        im.save("E:/python/Qt/t.png")
        self.codebel.setPixmap(QPixmap("E:/python/Qt/t.png"))

        


    def checking1(self):  #输入的号码检验是否已经注册过的
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                return True
        c.close()
        conn.close()
        return False
    
    def checking2(self):  #忘记密码时密码在数据库中修改过来
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        conn.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                conn.execute("update Controller set password=(?) where numble=(?)",(self.pwdLineEdit2.text(),variate[0],))
                self.sql = variate[2]
                break
        conn.commit()	
        conn.close()
        


    def enterPress1(self):  #忘记密码-》用户框回车确定时判断文字框是否有输入
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您登录！" )
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Controller_logon())
        else:
            self.pwdLineEdit2.setFocus()
    
    def enterPress2(self):  #忘记密码-》密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        else:
            self.pwdLineEdit3.setFocus()
     
    def enterPress3(self):   #注册-》确认密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        else:
            self.codeLineEdit1.setFocus()
    

    
    def accept(self):#忘记密码时将账号密码修改保存并登录。
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        elif len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        elif self.code !=self.codeLineEdit1.text():
            QMessageBox.about(self, "提示!", "验证码输入错误" )
            self.codeLineEdit1.setFocus()
        else:
            self.checking2()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0,Controller_function())
            #连接主窗口界面。




   
    def change_choice_status1(self):   #连接管理员登录界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Controller_record())
        
    
#管理员功能界面
class Controller_function(QFrame):
    def __init__(self):
        super(Controller_function, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainbutton1 = QPushButton("用户信息")  #用户功能界面的控件
        self.mainbutton2 = QPushButton("爬虫")
        self.mainbutton3 = QPushButton("添加资料")
        self.mainbutton4 = QPushButton("统计")
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.desktop = QApplication.desktop() #获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b= self.screenRect.height()  *1.0/5  
        a = self.screenRect.width() *1.0/5 
       
        self.mainbutton1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                QPushButton:hover{background-color:rgb(50, 170, 200)}")  
        self.layout.addWidget(self.mainbutton1, 0, 0)#往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.mainbutton2, 0, 1)
        self.layout.addWidget(self.mainbutton3, 1, 0)
        self.layout.addWidget(self.mainbutton4, 1, 1)
        self.mainbutton1.setMaximumSize(a, b)
        self.mainbutton2.setMaximumSize(a, b)
        self.mainbutton3.setMaximumSize(a, b)
        self.mainbutton4.setMaximumSize(a, b)




#管理员用户信息界面
class Controller_news(QFrame):
    def __init__(self):
        super(Controller_news, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.select_query = QComboBox()
        self.query = QLineEdit()
        self.search = QPushButton("搜索")
        self.returnBtn = QPushButton("返回")
        self.usrs = QLabel("总用户数:")
        self.table = QTableWidget()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.usrs1 = QLabel(str(159))  #读取用户人数
        self.select_query.addItems(['姓名', '号码', '学校', '年级'])
        self.usrs.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrs1.setStyleSheet("QLabel{color:rgb(0,0,240,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.select_query.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.search.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.query.setFont(QFont("宋体" , 12))
        self.select_query.setMaximumSize(70, 30)
        self.search.setMaximumSize(50, 30)
        self.returnBtn.setMaximumSize(60, 30)
        self.usrs.setMaximumSize(120, 30)
        self.usrs1.setMaximumSize(50, 30)
        self.query.setMaximumSize(150, 30)
        self.table.setRowCount(180)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['用户', '姓名', '性别', '学校', '年级'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.usrs, 0, 5, 1, 1)
        self.layout.addWidget(self.usrs1, 0, 6, 1, 1)
        self.layout.addWidget(self.select_query, 0, 16, 1, 1)
        self.layout.addWidget(self.query, 0, 17, 1, 1)
        self.layout.addWidget(self.search, 0, 18, 1, 1)
        self.layout.addWidget(self.table, 1, 0, 15, 19)
        
        


#管理员统计界面
class Controller_census(QFrame):
    def __init__(self):
        super(Controller_census, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnBtn = QPushButton("返回")
        self.sex = QLabel("男女比例:")  #后期改成QPushButton 按钮，点击出现图片，男女比例图，曲线图
        self.age = QLabel("年龄分布:")
        self.usrs = QLabel("总用户数:")
        self.censustab = QTableWidget()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.usrs1 = QLabel(str(159))  #读取用户人数
        self.sex1 = QLabel("15:2")
        self.age1 = QLabel("18-25")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.usrs.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrs1.setStyleSheet("QLabel{color:rgb(0,0,240,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(0,0,240,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.age.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.age1.setStyleSheet("QLabel{color:rgb(0,0,240,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.returnBtn.setMaximumSize(50, 30) 
        self.usrs.setMaximumSize(120, 30)
        self.usrs1.setMaximumSize(50, 30)
        self.sex.setMaximumSize(80, 30)
        self.sex1.setMaximumSize(80, 30)
        self.age.setMaximumSize(80, 30)
        self.age1.setMaximumSize(50, 30)
        self.censustab.setRowCount(180)
        self.censustab.setColumnCount(7)
        self.censustab.setHorizontalHeaderLabels(['用户', '加入天数', '学习天数', '学习时长', '学习课件', '学习练习', '日均时间'])
        self.censustab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.censustab.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.usrs, 0, 3, 1, 1)
        self.layout.addWidget(self.usrs1, 0, 4, 1, 1)
        self.layout.addWidget(self.sex, 0, 8, 1, 1)
        self.layout.addWidget(self.sex1, 0, 9, 1, 1)
        self.layout.addWidget(self.age, 0, 15, 1, 1)
        self.layout.addWidget(self.age1, 0, 16, 1, 1)
        self.layout.addWidget(self.censustab, 1, 0, 15, 19)
        
        
        
        
        
        

#用户注册界面
class Usr_logon(QFrame):
    def __init__(self):
        super(Usr_logon, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.usr2 =  QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.pwd3 = QLabel("确认密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.pwdLineEdit3 = QLineEdit()
        self.codeLineEdit1 = QLineEdit()
        self.okBtn1 = QPushButton("注册")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        self.pwd3.setMaximumSize(80, 40)
        #设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.pwd3.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit3.setMaximumSize(420, 40)
        self.codeLineEdit1.setMaximumSize(310, 40)
        #self.usrLineEdit2.setText(a)
        self.usrLineEdit2.setPlaceholderText("请输入手机号码")
        self.pwdLineEdit2.setPlaceholderText("请输入密码")
        self.pwdLineEdit3.setPlaceholderText("请重新输入密码")
        self.codeLineEdit1.setPlaceholderText("请输入右侧的验证码")
        self.usrLineEdit2.setFont(QFont("宋体" , 12))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体" , 12))
        self.pwdLineEdit3.setFont(QFont("宋体" , 12))
        self.codeLineEdit1.setFont(QFont("宋体" , 12))
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit3.setEchoMode(QLineEdit.Password)
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn1.setMaximumSize(420, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLineEdit2.returnPressed.connect(self.enterPress1)  #输入结束后按回车键跳到下一个控件
        self.pwdLineEdit2.returnPressed.connect(self.enterPress2)
        self.pwdLineEdit3.returnPressed.connect(self.enterPress3)
        self.codeLineEdit1.returnPressed.connect(self.accept) #验证码输入后回车直接验证是否可以登录
        self.okBtn1.clicked.connect(self.accept)
        self.returnBtn.clicked.connect(self.return_record)   #点击返回键返回登录界面
        self.layout.addWidget(self.returnBtn, 0,1 , 1, 1)
        self.layout.addWidget(self.usr2, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 1, 5, 1, 14)
        self.layout.addWidget(self.pwd2, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 2, 5, 1, 14)
        self.layout.addWidget(self.pwd3, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit3, 3, 5,1, 14 )
        self.layout.addWidget(self.codeLineEdit1, 4, 5, 1, 5)
        self.layout.addWidget(self.codebel, 4, 10, 1, 6)
        self.layout.addWidget(self.okBtn1, 5, 5, 1, 14)
        self.renovate_code()
    
    def renovate_code(self):
        self.code = ''
        for num in range(1,7):
            self.code = self.code + str(random.randint(0, 9))
        im = Image.new("RGB", (100, 40), (255, 255, 255))     #将验证码转换为图片
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "E:/python/Qt/MSYH.ttf"), 18)  
        dr.text((10, 5), self.code, font=font, fill="#000000")
        im.save("E:/python/Qt/t.png")
        self.codebel.setPixmap(QPixmap("E:/python/Qt/t.png"))

    def return_record(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_record())
    
    def checking1(self):  #注册时输入的号码检验是否已经注册过的
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                return True
        c.close()
        conn.close()
        return False
    
    def checking2(self):  #注册时密码在数据库中保存过来
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        a = self.usrLineEdit2.text()
        b = self.pwdLineEdit2.text()
        conn.execute("INSERT INTO User VALUES(?,?)",(a, b))
        conn.commit()	
        conn.close()
        
    def enterPress1(self):  #注册-》用户框回车确定时判断文字框是否有输入
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "您输入的号码已注册！\n请您登录！" )
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Usr_record())
        else:
            self.pwdLineEdit2.setFocus()
    
    def enterPress2(self):  #注册-》密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        else:
            self.pwdLineEdit3.setFocus()
     
    def enterPress3(self):   #注册-》确认密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        else:
            self.codeLineEdit1.setFocus()
    

    def accept(self):#注册时将账号密码保存并登录。
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text()) !=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        elif len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        elif self.code !=self.codeLineEdit1.text():
            QMessageBox.about(self, "提示!", "验证码输入错误" )
            self.codeLineEdit1.setFocus()
        else:
            win.numble = self.usrLineEdit2.text()
            self.checking2()
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Usr_informent())
      



    
#用户登录界面
class Usr_record(QFrame):
    def __init__(self):
        super(Usr_record, self).__init__()
        #self.setStyleSheet("background-color:white;")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr1 = QLabel("用户：")
        self.pwd1 = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.okBtn = QPushButton("登录")
        self.returnBtn = QPushButton("返回")
        self.forgetbtn = QLabel( )
        self.logonbtn = QLabel()
        self.found_sql()
        self.devise_Ui()

    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (350, 0, 0, 0)
        
        self.usr1.setMaximumSize(60, 60)
        #设置QLabel 的字体颜色，大小，
        self.usr1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.pwd1.setMaximumSize(60, 60)
        #设置QLabel 的字体颜色，大小，
        self.pwd1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.usrLineEdit.setPlaceholderText("请输入手机号码")
        self.usrLineEdit.setMaximumSize(400, 40)
        self.usrLineEdit.setFont(QFont("宋体" , 16))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(400, 40)
        self.pwdLineEdit.setPlaceholderText("请输入密码") 
        self.pwdLineEdit.setFont(QFont("宋体" , 16))
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)
        self.okBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn.setMaximumSize(400, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.forgetbtn.setText("<A href='www.baidu.com'>忘记密码</a>")
        self.logonbtn.setText("<A href='www.baidu.com'>注册</a>")
        self.forgetbtn.setStyleSheet("QLabel{color:rgb(0,0,255,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.logonbtn.setStyleSheet("QLabel{color:rgb(0,0,255,255);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.forgetbtn.setMaximumSize(90, 50)
        self.logonbtn.setMaximumSize(50, 50)
        self.usrLineEdit.returnPressed.connect(self.enterPress1)  #输入结束后按回车键跳到下一个控件
        self.pwdLineEdit.returnPressed.connect(self.accept) #密码填写号回车登录
        self.okBtn.clicked.connect(self.accept)  #登录按钮点击判断能否登录
        self.returnBtn.clicked.connect(self.change_usr_record2)        #点击返回键连接选择身份界面
        self.forgetbtn.linkActivated.connect(self.usr_forgetbtn1)   #连接用户忘记密码界面
        self.logonbtn.linkActivated.connect(self.usr_logonbtn1)   #连接用户注册界面
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr1, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 1, 4, 1, 19)
        self.layout.addWidget(self.pwd1, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 2, 4, 1, 19)
        self.layout.addWidget(self.okBtn, 3, 4, 1, 19)
        self.layout.addWidget(self.forgetbtn, 4, 4, 1, 2)
        self.layout.addWidget(self.logonbtn, 4, 12, 1, 2)
    def found_sql(self):   #创建保存用户信息的数据库
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        try:
            c.execute('''CREATE TABLE User(numble text,password text)''')	
        except:
            pass
        try:
            c.execute('''CREATE TABLE User_data(numble text,name text,birthday text,sex text,school text, grade text)''')	
        except:
            pass
        try:
            c.execute('''CREATE TABLE User_data1(numble text,time text,logonday int,stude1_day double, stude2_day double)''')	
        except:
            pass
        c.close()
        conn.close()
    
    

    
    def usr_forgetbtn1(self):   #连接用户忘记密码界面
        win.splitter.widget(0).setParent(None)
        Usr_forget().renovate_code()
        win.splitter.insertWidget(0, Usr_forget)
    
    def usr_logonbtn1(self):    #连接用户注册界面
        win.splitter.widget(0).setParent(None)
        Usr_logon().renovate_code()
        win.splitter.insertWidget(0, Usr_logon())

    def change_usr_record2(self):    #点击返回键连接选择身份界面
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Choice_status())
    
    def checking1(self):  #登录时检验号码是否没有注册
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit.text() :
                return False
        c.close()
        conn.close()
        return True
    def enterPress1(self):  #登录回车确定时判断文字框是否有输入
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！" )
        else:
            self.pwdLineEdit.setFocus()
            
    def accept(self):         #登录时判断密码是否正确
        if len(self.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit.setFocus()
        elif len(self.usrLineEdit.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit.setFocus()
        elif len(self.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit.setFocus()
        else:
            sqlpath ='D:/项目数据库/数据库/Information.db'
            conn=sqlite3.connect(sqlpath)
            c=conn.cursor()
            c.execute("select * from User")
            d =0
            for variate in c.fetchall():
                if variate[0]==self.usrLineEdit.text() and variate[1]== self.pwdLineEdit.text():
                    win.numble = self.usrLineEdit.text()
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:
                #设置一个查询用户的年级
                win.splitter.widget(0).setParent(None)
                win.splitter.insertWidget(0, Usr_function())
                theTime = datetime.datetime.now()
                win.time1 = theTime
                self.finddata()
            #连接主界面函数
            
    def finddata(self):
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User_data")
        for variate in c.fetchall():
            if variate[0]== win.numble :
                win.grade = variate[5]
                win.data.append(variate[0])
                win.data.append(variate[1])
                win.data.append(variate[2])
                win.data.append(variate[3])
                win.data.append(variate[4])
                win.data.append(variate[5])
                break
        c.execute("select * from User_data1")
        for variate in c.fetchall():
            if variate[0]== win.numble :
                win.data1.append(variate[0])
                win.data1.append(variate[1])
                win.data1.append(variate[2])
                win.data1.append(variate[3])
                win.data1.append(variate[4])
                break
        c.close()
        conn.close()
    
#用户忘记密码
class Usr_forget(QFrame):
    def __init__(self):
        super(Usr_forget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.usr2 =  QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.pwd3 = QLabel("确认密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.pwdLineEdit3 = QLineEdit()
        self.codeLineEdit1 = QLineEdit()
        self.okBtn1 = QPushButton("确认")
        self.returnBtn = QPushButton("返回")
        self.codebel = QLabel()
        self.devise_Ui()
        
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        self.pwd3.setMaximumSize(80, 40)
        #设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.pwd3.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:18px;font-weight:Bold;font-family:Arial;}")      
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit3.setMaximumSize(420, 40)
        self.codeLineEdit1.setMaximumSize(310, 40)
        self.usrLineEdit2.setPlaceholderText("请输入手机号码")
        self.pwdLineEdit2.setPlaceholderText("请输入新的密码")
        self.pwdLineEdit3.setPlaceholderText("请重新输入新的密码")
        self.codeLineEdit1.setPlaceholderText("请输入右侧的验证码")
        self.usrLineEdit2.setFont(QFont("宋体" , 12))  #设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体" , 12))
        self.pwdLineEdit3.setFont(QFont("宋体" , 12))
        self.codeLineEdit1.setFont(QFont("宋体" , 12))
        self.pwdLineEdit2.setEchoMode(QLineEdit.Password)
        self.pwdLineEdit3.setEchoMode(QLineEdit.Password)
        self.okBtn1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.okBtn1.setMaximumSize(420, 40)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:24px;color:rgb(0,0,0,255);}")
        self.returnBtn.setMaximumSize(60, 40)
        self.codebel.setMaximumSize(100, 40)
        self.usrLineEdit2.returnPressed.connect(self.enterPress1)  #用户输入框按回车判断
        self.pwdLineEdit2.returnPressed.connect(self.enterPress2) #密码输入框按回车判断
        self.pwdLineEdit3.returnPressed.connect(self.enterPress3) #确认密码输入框回车判断
        self.codeLineEdit1.returnPressed.connect(self.accept)   #验证码输入框回车判断是否可登录
        self.returnBtn.clicked.connect(self.return_record)
        self.layout.addWidget(self.returnBtn, 0, 1, 1, 1)
        self.layout.addWidget(self.usr2, 1, 3, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 1, 5, 1, 14)
        self.layout.addWidget(self.pwd2, 2, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 2, 5, 1, 14)
        self.layout.addWidget(self.pwd3, 3, 3, 1, 1)
        self.layout.addWidget(self.pwdLineEdit3, 3, 5,1, 14 )
        self.layout.addWidget(self.codeLineEdit1, 4, 5, 1, 5)
        self.layout.addWidget(self.codebel, 4, 10, 1, 6)
        self.layout.addWidget(self.okBtn1, 5, 5, 1, 14)
        self.renovate_code()
   
    def return_record(self): 
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_record())
    def renovate_code(self):   
        self.code = ''
        for num in range(1,7):
            self.code = self.code + str(random.randint(0, 9))
        im = Image.new("RGB", (100, 40), (255, 255, 255))     #将验证码转换为图片
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "E:/python/Qt/MSYH.ttf"), 18)  
        dr.text((10, 5), self.code, font=font, fill="#000000")
        im.save("E:/python/Qt/t.png")
        self.codebel.setPixmap(QPixmap("E:/python/Qt/t.png"))

        
        








    
    def checking1(self):  #忘记密码时检验号码是否没有注册
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                return False
        c.close()
        conn.close()
        return True
    

    
    
    def checking4(self):  #忘记密码时将新的密码在数据库中修改过来
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0]==self.usrLineEdit2.text() :
                conn.execute("update User set password=(?) where numble=(?)",(self.pwdLineEdit2.text(),variate[0],))
                break
        conn.commit()	
        c.close()
        conn.close()
    
    

    
    def enterPress1(self):  #忘记密码时回车确定时判断文字框是否有输入
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！" )
            time.sleep(2)
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Usr_logon())
        else:
            self.pwdLineEdit2.setFocus()
    
    def enterPress2(self):  #忘记密码-》密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit2.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        else:
            self.pwdLineEdit3.setFocus()
    
    def enterPress3(self):  #忘记密码-》确认密码框回车确定时判断文字框是否有输入
        if len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        else:
            self.codeLineEdit1.setFocus()
    

    
    
    
    
    def accept1(self):  #忘记密码时验证是否可以登录
        if len(self.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！" )
            self.usrLineEdit2.setFocus()
        elif len(self.usrLineEdit2.text())!=11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入" )
            self.usrLineEdit2.setFocus()
        elif len(self.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit2.setFocus()
        elif len(self.pwdLineEdit3.text())==0:
            QMessageBox.about(self, "提示!", "密码不能为空！" )
            self.pwdLineEdit3.setFocus()
        elif self.pwdLineEdit2.text() != self.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！" )
        elif self.code !=self.codeLineEdit1.text():
            QMessageBox.about(self, "提示!", "验证码输入错误" )
            self.codeLineEdit1.setFocus()
        else:
            win.numble = self.usrLineEdit2.text()
            self.checking4()
            #设置一个查询用户年级的函数
            win.splitter.widget(0).setParent(None)
            win.splitter.insertWidget(0, Usr_function())
            theTime = datetime.datetime.now()
            win.time1 = theTime
            self.finddata()
            #连接主窗口界面。
            
    
    def finddata(self):
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        c=conn.cursor()
        c.execute("select * from User_data")
        for variate in c.fetchall():
            if variate[0]== win.numble :
                win.data.append(variate[0])
                win.data.append(variate[1])
                win.data.append(variate[2])
                win.data.append(variate[3])
                win.data.append(variate[4])
                win.data.append(variate[5])
                break
        c.execute("select * from User_data1")
        for variate in c.fetchall():
            if variate[0]== win.numble :
                win.data1.append(variate[0])
                win.data1.append(variate[1])
                win.data1.append(variate[2])
                win.data1.append(variate[3])
                win.data1.append(variate[4])
                break
        c.close()
        conn.close()
    
    
#用户信息填写
class Usr_informent(QFrame):
    def __init__(self):
        super(Usr_informent, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sure = QPushButton("确认")
        self.name =  QLabel("姓名:")
        self.year  = QLabel("出生年月")
        self.yearcb = QComboBox()
        self.monthcb = QComboBox()
        self.sex =  QLabel("性别:")
        self.sexcb = QComboBox()
        self.school = QLabel("学校:")
        self.grade = QLabel("选择年级")
        self.gradecb = QComboBox()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.devise_Ui()
     
   
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        yearnb = []
        for  i in range(1980, 2020):
            yearnb.append(str(i))
        monthmb = []
        for i in range(1, 13):
            monthmb.append(str(i))
        grade = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', 
                     '初一', '初二', '初三', 
                     '高一', '高二', '高三']
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:26px;color:rgb(0,0,0,255);}")
        self.nameEdit.setPlaceholderText("请输入姓名")
        self.schoolEiit.setPlaceholderText("请输入学校名称")
        self.nameEdit.setFont(QFont("宋体" , 14))  #设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体" , 14))  #设置QLineEditn 的字体及大小
        self.name.setMaximumSize(50, 40)
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
        self.sexcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.yearcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.monthcb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.gradecb.setStyleSheet("QComboBox{font-family:'宋体';font-size: 22px;}")
        self.sexcb.addItems(['男', '女'])
        self.yearcb.addItems(yearnb)
        self.monthcb.addItems(monthmb)
        self.gradecb.addItems(grade)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 4, 1, 18)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sexcb, 2, 4, 1, 18)
        self.layout.addWidget(self.year, 3, 3, 1, 1)
        self.layout.addWidget(self.yearcb,3, 4, 1, 8 )
        self.layout.addWidget(self.monthcb, 3, 9, 1, 7)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.schoolEiit, 4, 4, 1, 18)
        self.layout.addWidget(self.grade, 5, 3, 1, 1)
        self.layout.addWidget(self.gradecb, 5, 4, 1, 18)
        self.layout.addWidget(self.sure, 6, 4, 1, 18)
        self.sure.clicked.connect(self.connect_fun)
    
    
    def save_data(self):
        a =  self.nameEdit.text()
        b = self.yearcb.currentText() +'-' +self.monthcb.currentText()
        c = self.sexcb.currentText()
        d = self.schoolEiit.text()
        e = self.gradecb.currentText()
        win.grade = e
        win.data = [win.numble, a, b, c, d, e]
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab) 
        win.time1 = datetime.datetime.now()
        print(theTime)
        sqlpath ='D:/项目数据库/数据库/Information.db'
        conn=sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?,?)",(win.numble, a, b, c, d, e))
        conn.execute("INSERT INTO User_data1 VALUES(?,?,?,?,?)",(win.numble, theTime , 1,0.0,0.0))
        win.data1 = [win.numble, theTime , 1, 0.0,0.0 ]
        print(win.data1)
        conn.commit()	
        conn.close()
    
    def connect_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        self.save_data()
        



#用户功能界面
class Usr_function(QFrame):
    def __init__(self):
        super(Usr_function, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainbutton1 = QPushButton("课件")  #用户功能界面的控件
        self.mainbutton2 = QPushButton("练习")
        self.mainbutton3 = QPushButton("学习报告")
        self.mainbutton4 = QPushButton("我的")
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.desktop = QApplication.desktop() #获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        b= self.screenRect.height()  *1.0/5  
        a = self.screenRect.width() *1.0/5 
       
        self.mainbutton1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.mainbutton4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                QPushButton:hover{background-color:rgb(50, 170, 200)}")  
        self.mainbutton1.clicked.connect(self.connect_fun1)
        self.mainbutton2.clicked.connect(self.connect_fun2)
        self.mainbutton3.clicked.connect(self.connect_fun3)
        self.mainbutton4.clicked.connect(self.connect_fun4)
        self.layout.addWidget(self.mainbutton1, 0, 0)#往网格的不同坐标添加不同的组件
        self.layout.addWidget(self.mainbutton2, 0, 1)
        self.layout.addWidget(self.mainbutton3, 1, 0)
        self.layout.addWidget(self.mainbutton4, 1, 1)
        self.mainbutton1.setMaximumSize(a, b)
        self.mainbutton2.setMaximumSize(a, b)
        self.mainbutton3.setMaximumSize(a, b)
        self.mainbutton4.setMaximumSize(a, b)
        
    def connect_fun1(self):
        win.time2 = datetime.datetime.now()
        win.splitter.widget(0).setParent(None)
        if (win.grade =='一年级' or win.grade =='二年级' or win.grade == "三年级"):
            win.splitter.insertWidget(0, Usr_window1_child1())
        elif(win.grade =='四年级' or win.grade =='五年级' or win.grade == "六年级"):
            win.splitter.insertWidget(0, Usr_window1_child1())
        elif(win.grade =='初一' or win.grade =='初二' or win.grade == "初三") :
            win.splitter.insertWidget(0, Usr_window1_child2())
        elif(win.grade =='高一' or win.grade =='高二' or win.grade == "高三") :
            win.splitter.insertWidget(0, Usr_window1_child3())
    
    def connect_fun2(self):
        win.time2 = datetime.datetime.now()
        win.splitter.widget(0).setParent(None)
        if (win.grade =='一年级' or win.grade =='二年级' or win.grade == "三年级"):
            win.splitter.insertWidget(0, Usr_window2_child1())
        elif(win.grade =='四年级' or win.grade =='五年级' or win.grade == "六年级"):
            win.splitter.insertWidget(0, Usr_window2_child1())
        elif(win.grade =='初一' or win.grade =='初二' or win.grade == "初三") :
            win.splitter.insertWidget(0, Usr_window2_child2())
        elif(win.grade =='高一' or win.grade =='高二' or win.grade == "高三") :
            win.splitter.insertWidget(0, Usr_window2_child3())
    
    def connect_fun3(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_myself())
    
    def connect_fun4(self):
        win.splitter.widget(0).setParent(None)
        Usr_report().information()
        win.splitter.insertWidget(0, Usr_report)
    
    
#用户课件小学界面
class Usr_window1_child1(QFrame):
    def __init__(self):
        super(Usr_window1_child1, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child1_win1but1 = QPushButton("返回")#课件-小学的控件
        self.child1_win1but2 = QPushButton("语文")
        self.child1_win1but3 = QPushButton("数学")
        self.child1_win1but4 = QPushButton("英语")
        self.window1tree1 = QTreeView()
        self.window1tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child1_win1but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win1but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child1_win1but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win1but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win1but1.clicked.connect(self.return_fun)
        self.win_layout1.addWidget(self.child1_win1but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child1_win1but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child1_win1but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child1_win1but4, 4, 0,1,2)
        self.win_layout2.addWidget(self.window1tree, 0, 0, 20, 20)
        
    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0,Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[3] = win.data1[3] + b.seconds/1.0
 
        


#用户课件初中界面
class Usr_window1_child2(QFrame):
    def __init__(self):
        super(Usr_window1_child2, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child2_win1but1 = QPushButton("返回")#课件-初中的控件
        self.child2_win1but2 = QPushButton("语文")
        self.child2_win1but3 = QPushButton("数学")
        self.child2_win1but4 = QPushButton("英语")
        self.child2_win1but5 = QPushButton("物理")
        self.child2_win1but6 = QPushButton("化学")
        self.child2_win1but7 = QPushButton("生物")
        self.child2_win1but8 = QPushButton("政治")
        self.child2_win1but9 = QPushButton("历史")
        self.child2_win1but10 = QPushButton("地理")
        self.window1tree1 = QTreeView()
        self.window1tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child2_win1but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child2_win1but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}") 
        self.child2_win1but8.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but9.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but10.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but1.clicked.connect(self.return_fun)
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        self.win_layout1.addWidget(self.child2_win1but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but4, 4, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but5, 5, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but6, 6, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but7, 7, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but8, 8, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but9, 9, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but10, 10, 0,1,2)
        self.win_layout2.addWidget(self.window1tree, 0, 0, 20, 20)
        
        


    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[3] = win.data1[3] + b.seconds/1.0
#用户课件高中界面
class Usr_window1_child3(QFrame):
    def __init__(self):
        super(Usr_window1_child3, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child2_win1but1 = QPushButton("返回")#课件-初中的控件
        self.child2_win1but2 = QPushButton("语文")
        self.child2_win1but3 = QPushButton("数学")
        self.child2_win1but4 = QPushButton("英语")
        self.child2_win1but5 = QPushButton("物理")
        self.child2_win1but6 = QPushButton("化学")
        self.child2_win1but7 = QPushButton("生物")
        self.child2_win1but8 = QPushButton("政治")
        self.child2_win1but9 = QPushButton("历史")
        self.child2_win1but10 = QPushButton("地理")
        self.window1tree1 = QTreeView()
        self.window1tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child2_win1but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child2_win1but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}") 
        self.child2_win1but8.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but9.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but10.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win1but1.clicked.connect(self.return_fun)
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        self.win_layout1.addWidget(self.child2_win1but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but4, 4, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but5, 5, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but6, 6, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but7, 7, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but8, 8, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but9, 9, 0,1,2)
        self.win_layout1.addWidget(self.child2_win1but10, 10, 0,1,2)
        self.win_layout2.addWidget(self.window1tree, 0, 0, 20, 20)
        
        



    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[3] = win.data1[3] + b.seconds/1.0
#用户练习小学界面
class Usr_window2_child1(QFrame):
    def __init__(self):
        super(Usr_window2_child1, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child1_win2but1 = QPushButton("返回")#课件-小学的控件
        self.child1_win2but2 = QPushButton("语文")
        self.child1_win2but3 = QPushButton("数学")
        self.child1_win2but4 = QPushButton("英语")
        self.window2tree1 = QTreeView()
        self.window2tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child1_win2but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win2but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child1_win2but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win2but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child1_win2but1.clicked.connect(self.return_fun)
        self.win_layout1.addWidget(self.child1_win2but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child1_win2but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child1_win2but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child1_win2but4, 4, 0,1,2)
        self.win_layout2.addWidget(self.window2tree, 0, 0, 20, 20)
        
        
        






    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[4] = win.data1[4] + b.seconds/1.0
#用户练习初中界面
class Usr_window2_child2(QFrame):
    def __init__(self):
        super(Usr_window2_child2, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child2_win2but1 = QPushButton("返回")#课件-初中的控件
        self.child2_win2but2 = QPushButton("语文")
        self.child2_win2but3 = QPushButton("数学")
        self.child2_win2but4 = QPushButton("英语")
        self.child2_win2but5 = QPushButton("物理")
        self.child2_win2but6 = QPushButton("化学")
        self.child2_win2but7 = QPushButton("生物")
        self.child2_win2but8 = QPushButton("政治")
        self.child2_win2but9 = QPushButton("历史")
        self.child2_win2but10 = QPushButton("地理")
        self.window2tree1 = QTreeView()
        self.window2tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child2_win2but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child2_win2but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}") 
        self.child2_win2but8.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but9.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but10.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but1.clicked.connect(self.return_fun)
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        self.win_layout1.addWidget(self.child2_win2but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but4, 4, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but5, 5, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but6, 6, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but7, 7, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but8, 8, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but9, 9, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but10, 10, 0,1,2)
        self.win_layout2.addWidget(self.window2tree, 0, 0, 20, 20)
        
        
 

 
    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[4] = win.data1[4] + b.seconds/1.0
#用户练习高中界面
class Usr_window2_child3(QFrame):
    def __init__(self):
        super(Usr_window2_child3, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.child2_win2but1 = QPushButton("返回")#课件-初中的控件
        self.child2_win2but2 = QPushButton("语文")
        self.child2_win2but3 = QPushButton("数学")
        self.child2_win2but4 = QPushButton("英语")
        self.child2_win2but5 = QPushButton("物理")
        self.child2_win2but6 = QPushButton("化学")
        self.child2_win2but7 = QPushButton("生物")
        self.child2_win2but8 = QPushButton("政治")
        self.child2_win2but9 = QPushButton("历史")
        self.child2_win2but10 = QPushButton("地理")
        self.window2tree1 = QTreeView()
        self.window2tree = QTextEdit()
        self.win_lab = QLabel()
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        
        self.Lchild_win1 = QWidget()  #左侧控件布局
        self.win_layout1 = QGridLayout()  # 创建左侧部件的网格布局层
        self.Lchild_win1.setLayout(self.win_layout1)   # 设置左侧部件布局为网格    
        self.Rchild_win1 = QWidget()     #右侧控件布局
        self.win_layout2 = QGridLayout()   # 创建右侧部件的网格布局层
        self.Rchild_win1.setLayout(self.win_layout2)   # 设置右侧部件布局为网格
        self.layout.addWidget(self.Lchild_win1,0,0,20,2) # 左侧部件在第0行第0列，占20行2列
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        
        self.child2_win2but1.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but2.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")                        
        self.child2_win2but3.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but4.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but5.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but6.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but7.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}") 
        self.child2_win2but8.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but9.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but10.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.child2_win2but1.clicked.connect(self.return_fun)
        self.layout.addWidget(self.Rchild_win1,0,2,20,20) # 右侧部件在第1行第3列，占20行20列   
        self.win_layout1.addWidget(self.child2_win2but1, 1, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but2, 2, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but3, 3, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but4, 4, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but5, 5, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but6, 6, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but7, 7, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but8, 8, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but9, 9, 0,1,2)
        self.win_layout1.addWidget(self.child2_win2but10, 10, 0,1,2)
        self.win_layout2.addWidget(self.window2tree, 0, 0, 20, 20)
        
        
 

 


    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        a = datetime.datetime.now()
        b = a - win.time2
        win.data1[4] = win.data1[4] + b.seconds/1.0
#用户我的界面
class Usr_myself(QFrame):   #增加一个编辑资料的按钮
    def __init__(self):
        super(Usr_myself, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnBtn = QPushButton("返回")
        self.ExditBtn = QPushButton("编辑")
        self.name = QLabel("姓名:")
        self.sex = QLabel("性别:")
        self.number = QLabel("手机号:")
        self.school = QLabel("学校:")
        self.grade = QLabel("年级:")
        self.amend = QPushButton("修改密码")
        self.withdraw = QPushButton('退出')
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        
        self.name1 = QLabel(win.data[1])    #读取数据库中的信息，将信息输出label中
        self.sex1 = QLabel(win.data[3])
        self.number1 = QLabel(win.data[0])
        self.school1 = QLabel(win.data[4])
        self.grade1 = QLabel(win.data[5])
        self.returnBtn.setMaximumSize(60, 40)
        self.ExditBtn.setMaximumSize(60, 40)
        self.name.setMaximumSize(70, 40)
        self.sex.setMaximumSize(70, 40)
        self.number.setMaximumSize(70, 40)
        self.school.setMaximumSize(70, 40)
        self.grade.setMaximumSize(70, 40)
        self.name1.setMaximumSize(350, 40)
        self.sex1.setMaximumSize(350, 40)
        self.number1.setMaximumSize(350, 40)
        self.school1.setMaximumSize(350, 40)
        self.grade1.setMaximumSize(350, 40)
        self.amend.setMaximumSize(500, 40)
        self.withdraw.setMaximumSize(500, 40)
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.amend.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(0,0,0,255);}")
        self.withdraw.setStyleSheet("QPushButton{ font-family:'宋体';font-size:28px;color:rgb(255,0,0,255);}")
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.ExditBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.name1.setStyleSheet("QLabel{color:rgb(255,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.sex1.setStyleSheet("QLabel{color:rgb(255,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.number1.setStyleSheet("QLabel{color:rgb(255,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.school1.setStyleSheet("QLabel{color:rgb(255,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.grade1.setStyleSheet("QLabel{color:rgb(255,0,0,255);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.withdraw.clicked.connect(self.return_win)
        self.returnBtn.clicked.connect(self.return_fun)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.ExditBtn, 0, 14, 1, 1)
        self.layout.addWidget(self.name, 1, 3, 1, 1)
        self.layout.addWidget(self.name1, 1, 5, 1, 15)
        self.layout.addWidget(self.sex, 2, 3, 1, 1)
        self.layout.addWidget(self.sex1, 2, 5, 1, 15)
        self.layout.addWidget(self.number, 3, 3, 1, 1)
        self.layout.addWidget(self.number1, 3, 5, 1, 15)
        self.layout.addWidget(self.school, 4, 3, 1, 1)
        self.layout.addWidget(self.school1, 4, 5, 1, 15)
        self.layout.addWidget(self.grade, 5, 3, 1, 1)
        self.layout.addWidget(self.grade1, 5, 5, 1, 15)
        self.layout.addWidget(self.amend, 6, 3, 1, 15)
        self.layout.addWidget(self.withdraw, 7, 3, 1, 15)
        
    def return_win(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Choice_status())
        
    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())    

#用户学习报告的界面
class Usr_report(QFrame):
    def __init__(self):
        super(Usr_report, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnBtn = QPushButton("返回")
        self.day = QLabel("学习天数:")
        self.learntime = QLabel("学习总时长:")
        self.learncou =  QLabel("学习课件:")
        self.learnexe = QLabel("学习练习:")
        self.avglearn = QLabel("日均学习:")
        self.devise_Ui()
    
    def devise_Ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)    #设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True) # 设置widget鼠标跟踪
        self.layout.setContentsMargins (300, 0, 0, 0)
        self.returnBtn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:22px;color:rgb(0,0,0,255);}")
        self.day .setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learntime.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learncou.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.learnexe.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:22px;font-weight:Bold;font-family:'宋体';}")
        self.returnBtn.setMaximumSize(60, 40)
        self.day.setMaximumSize(140, 40)
        self.learntime.setMaximumSize(140, 40)
        self.learncou.setMaximumSize(140, 40)
        self.learnexe.setMaximumSize(140, 40)
        self.avglearn.setMaximumSize(140, 40)
        self.returnBtn.clicked.connect(self.return_fun)
        self.layout.addWidget(self.returnBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.day, 2, 3, 1, 1)
        self.layout.addWidget(self.learntime, 3, 3, 1, 1)
        self.layout.addWidget(self.learncou, 4, 3, 1, 1)
        self.layout.addWidget(self.learnexe, 5, 3, 1, 1)
        self.layout.addWidget(self.avglearn, 6, 3, 1, 1)
        
    
    def information(self):
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(win.data1[1], abcd)
        a = (new -a1).days
        self.join =  QLabel("已加入"+ str(a)+ "天")
        self.day1 = QLabel(str(win.data1[2])+"天")
        ab = win.data1[3]+win.data1[4]
        if (ab/3600)>1:
            ac = str(ab/3600) +'时'+str((ab/3600 - int(ab/3600))*60) +"分"
        else:
            ac = str(ab/60)  +"分"
        self.learntime1 = QLabel(ac)
        b = win.data1[3]
        if (b/3600)>1:
            c = str(b/3600) +'时'+str((b/3600 - int(b/3600))*60) +"分"
        else:
            c = str(b/60)  +"分"
        self.learncou1 =  QLabel(c)
        d = win.data1[4]
        if (d/3600)>1:
            e = str(d/3600) +'时'+str((d/3600 - int(d/3600))*60) +"分"
        else:
            d = str(d/60) +"分"
        self.learnexe1 = QLabel(e)
        ad = ab/win.data1[2]
        if (ad/3600)>1:
            ae = str(ad/3600) +'时'+str((ad/3600 - int(ad/3600))*60) +"分"
        else:
            ae = str(ad/60)  +"分"
        self.avglearn1 = QLabel(ae)
        self.join.setStyleSheet("QLabel{color:rgb(0,200,0,255);font-size:24px;font-weight:Bold;font-family:'宋体';}")
        self.day1 .setStyleSheet("QLabel{color:rgb(0,255,0,255);font-size:26px;font-weight:Bold;font-family:'宋体';}")
        self.learntime1.setStyleSheet("QLabel{color:rgb(0,255,0,255);font-size:26px;font-weight:Bold;font-family:'宋体';}")
        self.learncou1.setStyleSheet("QLabel{color:rgb(0,255,0,255);font-size:26px;font-weight:Bold;font-family:'宋体';}")
        self.learnexe1.setStyleSheet("QLabel{color:rgb(0,255,0,255);font-size:26px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn1.setStyleSheet("QLabel{color:rgb(0,255,0,255);font-size:26px;font-weight:Bold;font-family:'宋体';}")
        self.join.setMaximumSize(400, 40)
        self.day1.setMaximumSize(350, 40)
        self.learntime1.setMaximumSize(350, 40)
        self.learncou1.setMaximumSize(350, 40)
        self.learnexe1.setMaximumSize(350, 40)
        self.avglearn1.setMaximumSize(350, 40)
        self.layout.addWidget(self.day1, 2, 5, 1, 16)
        self.layout.addWidget(self.join, 1, 3, 1, 18)
        self.layout.addWidget(self.learntime1, 3, 5, 1, 16)
        self.layout.addWidget(self.learncou1, 4, 5, 1, 16)
        self.layout.addWidget(self.learnexe1, 5, 5, 1, 16)
        self.layout.addWidget(self.avglearn1, 6, 5, 1, 16)
        
    
    def return_fun(self):
        win.splitter.widget(0).setParent(None)
        win.splitter.insertWidget(0, Usr_function())
        
        

#主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("E:/python/Qt/UnFrameStyle.qss").read())
    win = QUnFrameWindow()
    win.setCloseButton(True)
    win.setMinMaxButtons(True)
    win.show()
    sys.exit(app.exec_())

  
