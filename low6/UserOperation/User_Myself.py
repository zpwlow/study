from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.User_Myself_win import User_Myself_win
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import Function,User_amend

class User_Myself(QFrame):
    def __init__(self):
        super(User_Myself, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_date where number=(?)", (UserOperation.number,))
        data = c.fetchall()[0]
        c.close()
        conn.close()
        self.myself = User_Myself_win(data)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.myself)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.myself.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
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
        self.myself.newlab.setPixmap(QPixmap.fromImage(showImage))


    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers,x,y)
            if fingers[0] == 1:
                if x > 125 and x < 225 and y > 300 and y < 370:
                    #返回
                    self.myself.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function.Function())
                elif x > 375 and x < 475 and y > 300 and y < 370:
                    #查看答案
                    self.myself.messagelab.setText("提示!\n\t" + "本次操作为：修改密码\n\t操作成功")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_amend.User_amend())

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        self.myself.newlab.clear()