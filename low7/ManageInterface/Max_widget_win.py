from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt

# 管理员播放课件　
from ManageOperation import Max_widget


class Max_widget_win(QWidget):
    def __init__(self):
        super(Max_widget_win, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.datawindow = Max_widget.Max_widget(self)
        self.setWindowFlags(
            Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.lab2 = QLabel(self)
        self.lab2.resize(self.width1, self.height1)
        self.lab2.setMouseTracking(True)  # 设置widget鼠标跟踪
