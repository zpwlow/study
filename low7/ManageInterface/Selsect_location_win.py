from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QGridLayout, QLabel, QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt


# 选择添加系统课件的内容
from ManageOperation import Select_location


class Select_location_win(QWidget):
    def __init__(self, dow):
        super(Select_location_win, self).__init__()
        self.datawindow = Select_location.Select_location(self)
        self.setWindowTitle("选择添加系统文件的内容")
        self.dow = dow
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
            Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作

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
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.sure.setStyleSheet("QPushButton{ font-family:'宋体';font-size:18px;color:rgb(0,0,0);}\
                                 QPushButton{background-color:rgb(170,200, 50)}\
                                 QPushButton:hover{background-color:rgb(50, 170, 200)}")
        self.lab.setMaximumSize(400, 80)
        self.typelab.setMaximumSize(80, 50)
        self.greadelab.setMaximumSize(80, 50)
        self.courselab.setMaximumSize(80, 50)
        self.typebox.setMaximumSize(160, 50)
        self.greadebox.setMaximumSize(160, 50)
        self.coursebox.setMaximumSize(160, 50)
        self.sure.setMaximumSize(80, 50)
        self.typebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.greadebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.coursebox.setStyleSheet("QComboBox{font-family:'宋体';font-size: 18px;}")
        self.typebox.addItems(['', '小学', '初中', '高中'])
        self.layout.addWidget(self.lab, 0, 2, 1, 6)
        self.layout.addWidget(self.typelab, 1, 0, 1, 1)
        self.layout.addWidget(self.typebox, 1, 1, 1, 2)
        self.layout.addWidget(self.greadelab, 1, 3, 1, 1)
        self.layout.addWidget(self.greadebox, 1, 4, 1, 2)
        self.layout.addWidget(self.courselab, 1, 6, 1, 1)
        self.layout.addWidget(self.coursebox, 1, 7, 1, 2)
        self.layout.addWidget(self.sure, 2, 8, 1, 1)
