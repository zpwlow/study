from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QTextEdit, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ManageOperation import Addexfilewin


class Addexfilewin_win(QWidget):
    def __init__(self, data, fname):
        super(Addexfilewin_win, self).__init__()
        self.datawindow = Addexfilewin.Addexfilewin(self)
        self.fname = fname
        self.data = data
        self.sure = QPushButton("保存")
        self.concle = QPushButton("取消")
        self.cutimage = QPushButton("上一题")
        self.addimage = QPushButton("下一题")
        self.imagelab = QLabel()
        self.answerlab = QLabel("答案")
        self.answerEdit = QLineEdit()
        self.analysislab = QLabel("解析")
        self.analysisEdit = QTextEdit()
        self.addimage.clicked.connect(self.datawindow.addfun)
        self.cutimage.clicked.connect(self.datawindow.cutfun)
        self.concle.clicked.connect(self.datawindow.conclefun)
        self.sure.clicked.connect(self.datawindow.surefun)
        self.devise_Ui()

    def devise_Ui(self):
        self.resize(800, 500)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 500) / 2)  # 窗口移动至中心
        self.setWindowFlags(
            Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #窗口置顶

        self.horizontalLayout = QHBoxLayout(self)
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
        self.imagelab.setMaximumSize(400, 250)
        self.cutimage.setMaximumSize(80, 40)
        self.addimage.setMaximumSize(80, 40)
        self.answerlab.setMaximumSize(80, 40)
        self.analysislab.setMaximumSize(80, 40)
        self.answerEdit.setMaximumSize(250, 40)
        self.analysisEdit.setMaximumSize(250, 180)
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.cutimage, 0, 1, 1, 1)
        self.layout.addWidget(self.addimage, 0, 9, 1, 1)
        self.layout.addWidget(self.answerlab, 2, 1, 2, 1)
        self.layout.addWidget(self.answerEdit, 2, 2, 2, 3)
        self.layout.addWidget(self.analysislab, 4, 1, 2, 1)
        self.layout.addWidget(self.analysisEdit, 4, 2, 4, 3)
        self.layout.addWidget(self.imagelab, 3, 6, 4, 4)
        self.layout.addWidget(self.sure, 11, 8, 1, 1)
        self.layout.addWidget(self.concle, 11, 9, 1, 1)
