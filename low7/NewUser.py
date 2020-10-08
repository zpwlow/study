"""
作者：钟培望
名称：具体人工智能沉浸式学习系统用户端
时间：2020.8.11
版本: 1.1
"""

from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt
from UserInterface.Function_win import Function_win
from UserOperation.FingerDetection import Finger_win
import UserOperation
import sys

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

close_Mouse_key = []


class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """

    def __init__(self):  # 设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None)  # 设置为顶级窗口
        self.setWindowTitle("low_User")
        self.setWindowIcon(QIcon("./datas/logo.ico"))
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.resize(self.x, self.y)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        # self.splitter.addWidget(Record())
        self.splitter.addWidget(Function_win())
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))

    def closeEvent(self, event):
        # open_mouse_and_key()
        # 清理一些 自己需要关闭的东西
        event.accept()  # 界面的关闭,但是会有一些时候退出不完全,需要调用 os 的_exit 完全退出
        print(UserOperation.bgModel)
        try:
            os._exit(5)
        except:
            pass


def changfun():
    UserOperation.win.show()


# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    finger = Finger_win()
    UserOperation.win = QUnFrameWindow()
    finger.my_Signal.connect(changfun)
    finger.show()
    sys.exit(app.exec_())
