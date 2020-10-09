from PyQt5.QtWidgets import QFrame, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM
from UserOperation import Function
import cv2
from UserInterface.MyLabel import MyLabel


# 用户功能界面
class Function_win(QFrame):
    def __init__(self):
        super(Function_win, self).__init__()
        # 获取显示器分辨率大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.width1 = self.screenRect.width() / 2
        self.height1 = self.screenRect.height() / 2
        self.win = QWidget()
        self.layout = QGridLayout()
        self.horizontalLayout = QHBoxLayout(self)
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频

        self.image = None
        self.newlab.setxy(75, 150, 175, 220, "查看课程")
        self.newlab.setxy(250, 150, 350, 220, "问问题")
        self.newlab.setxy(425, 150, 525, 220, "学习记录")
        self.newlab.setxy(75, 330, 175, 400, "我的")
        self.newlab.setxy(250, 330, 350, 400, "退出登录")
        self.newlab.setxy(425, 330, 525, 400, "退出程序")
        self.datalayer = Function.Function(self)
        self.devise_Ui()

    def devise_Ui(self):
        self.resize(self.width1 * 2, self.height1 * 2)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1, 90)
        self.newlab.setMaximumSize(600, 550)
        self.layout.addWidget(self.messagelab, 0, 0, 4, 9)
        self.layout.addWidget(self.progresslab, 4, 11, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 12, 1, 4)
        self.layout.addWidget(self.newlab, 5, 7, 10, 24)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image))
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
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.newlab.setPixmap(QPixmap.fromImage(showImage))
