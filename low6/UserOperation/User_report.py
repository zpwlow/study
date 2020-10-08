from PyQt5.QtWidgets import QFrame,QHBoxLayout,QGridLayout
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.User_report_win import Usr_report_win
from UserOperation import self_cap,self_CAM_NUM
import cv2
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import Function

class User_report(QFrame):
    def __init__(self):
        super(User_report, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.report = Usr_report_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.report)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.report.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.report.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 150 and x < 250 and y > 200 and y < 270:
                    # 返回
                    try:
                        self.timer_next.stop()
                        self.timer_camera.stop()
                        self_cap.release()  # 释放视频流
                        self.report.newlab.clear()
                    except:
                        pass
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function.Function())