from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout
from PyQt5.QtWidgets import QApplication,QHBoxLayout
from PyQt5.QtGui import QPalette, QColor,QPixmap,QMovie
from PyQt5.QtCore import Qt
from UserInterface.MyLabel import MyLabel

class Question_win(QWidget):
    def __init__(self):
        super(Question_win, self).__init__()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(125, 300, 225, 370, "返回")
        self.newlab.setxy(375, 300, 475, 370, "查看答案")
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
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        #self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
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
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 2, 3, 1, 1)
        self.layout.addWidget(self.setextlab, 2, 4, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.answerlab, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("./datas/progress_bar.gif")
        self.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小