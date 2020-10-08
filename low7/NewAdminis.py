"""
作者：钟培望
名称：具体人工智能沉浸式学习系统管理员端
时间：2020.8.11
版本: 1.1
"""

from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QSplitter, QMessageBox, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import ManageOperation
from ManageOperation import Record
import sys


class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """

    def __init__(self):  # 设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None)  # 设置为顶级窗口
        self.setWindowTitle("low_Administrators")
        self.setWindowIcon(QIcon("./datas/logo.ico"))
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.setMinimumWidth(670)
        self.setMinimumHeight(560)
        self.resize(self.x, self.y)
        self.number = ''
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.bar = self.menuBar()
        file = self.bar.addMenu("文件")
        logonquit = QAction("退出登录", self)
        file.addAction(logonquit)
        quit = QAction("退出", self)
        file.addAction(quit)
        logonquit.triggered.connect(self.logonquit_fun)
        quit.triggered.connect(self.close_win)
        self.splitter.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.splitter.addWidget(Record.Record())
        # self.splitter.addWidget(Function())

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
        self.splitter.addWidget(Record.Record())


# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ManageOperation.win = QUnFrameWindow()
    ManageOperation.win.show()
    sys.exit(app.exec_())
