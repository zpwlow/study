from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QLineEdit,QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


#添加课程
class AddCourse_win(QWidget):
    def __init__(self):
        super(AddCourse_win, self).__init__()
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
            Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶,父窗口不可操作
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #窗口置顶

        self.horizontalLayout = QHBoxLayout(self)
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