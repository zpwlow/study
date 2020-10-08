from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QGridLayout
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM, Question
import cv2


class Question_win(QFrame):
    def __init__(self):
        super(Question_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.datalayer = Question.Question(self)
        self.image = None
        self.face = None
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(125, 300, 225, 370, "返回")
        self.newlab.setxy(375, 300, 475, 370, "查看答案")
        self.devise_ui()

    def devise_ui(self):
        palette1 = QPalette()
        palette1.setColor(palette1.Background, QColor(245, 245, 245))
        self.setPalette(palette1)

        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:30px;font-weight:Bold;font-family:Arial;}")
        self.answerlab.setAlignment(Qt.AlignCenter)
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.answerlab.setMaximumSize(self.width1 / 2, self.height1 - 100)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 2, 3, 1, 1)
        self.layout.addWidget(self.setextlab, 2, 4, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.answerlab, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image, self.face))
        if not self.timer_camera.isActive():  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if not flag:  # flag表示open()成不成功
                self.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(200)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  # 翻转镜像--->对角翻转.
        self.face = show[self.forget.newlab.y1:self.forget.newlab.y2,
                    self.forget.newlab.x1:self.forget.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.newlab.setPixmap(QPixmap.fromImage(showImage))
