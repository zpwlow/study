from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.User_amend_win import User_amend_win
from UserOperation import self_cap, self_CAM_NUM
import cv2, sqlite3,time
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import ContrastJob, User_amend,User_Myself


class User_amend(QFrame):
    def __init__(self):
        super(User_amend, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.sign = 1
        self.passw1 = ''
        self.passw2 = ''
        self.data = []
        self.data1 = []
        self.amend = User_amend_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.amend)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.amend.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  # 翻转镜像--->对角翻转.
        self.face = show[self.amend.newlab.y1:self.amend.newlab.y2,
                    self.amend.newlab.x1:self.amend.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.amend.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            # print(fingers)
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 75 and x < 175 and y > 270 and y < 340:
                    # 返回
                    self.amend.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_Myself.User_Myself())
                elif x > 250 and x < 350 and y > 270 and y < 340:
                    self.amend.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()
                    # 确定
                elif x > 425 and x < 525 and y > 270 and y < 340:
                    # 修改
                    self.amend.messagelab.setText("提示!\n\t" + "本次操作为：修改\n\t操作成功")
                    self.accept()
                elif x > 75 and x < 175 and y > 410 and y < 480:
                    # 上一步
                    self.amend.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.passw1 = self.data[-1]
                            self.amend.amendedit1.setText(self.passw1)
                            self.data = self.data[:-1]
                        else:
                            self.passw1 = ''
                            self.amend.amendedit1.setText(self.passw1)
                            self.data = []
                        self.amend.messagelab.setText("提示!\n\t" +
                                                "请把原密码分段输入输入区后，再在操作区输入确定！！")
                    elif sign == 2:
                        if len(self.data1) > 0:
                            self.passw2 = self.data1[-1]
                            self.amend.amendedit2.setText(self.passw2)
                            self.data1 = self.data1[:-1]
                            self.amend.messagelab.setText("提示!\n\t" +
                                                    "请把新密码分段输入输入区后，再在操作区输入确定！！")
                        else:
                            self.passw2 = ''
                            self.amend.amendedit2.setText(self.passw2)
                            self.data1 = []
                            self.sign = 1
                            self.passw1 = self.data[-1]
                            self.amend.amendedit1.setText(self.passw1)
                            self.data = self.data[:-1]
                            self.amend.messagelab.setText("提示!\n\t" +
                                                    "请把原密码分段输入输入区后，再在操作区输入确定！！")
                elif x > 250 and x < 350 and y > 410 and y < 480:
                    # 下一步
                    self.amend.messagelab.setText("提示!\n\t" + "本次操作为：下一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        self.sign = 2
                    elif sign == 2:
                        self.accept()


    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        self.amend.newlab.clear()


    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.amend.setextlab.setText("正在识别输入中．．")
        self.amend.progresslab.setMovie(self.amend.movie)
        self.amend.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob.ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    def contrast_answer_right(self):
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.amend.amendedit1.setText(self.passw)
                self.amend.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                        "如果输入错误请您在操作区输入上一步操作！\n\t输入完整后可输入下一步")
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data.append(self.passw)
                self.passw = self.passw + da
                self.amend.amendedit1.setText(self.passw)
                self.amend.messagelab.setText("提示!\n\t" + "部分密码输入成功！" +
                                        "如果输入错误请您在操作区输入上一步操作!\n\t输入完整后可输入登录")
        time.sleep(1)
        self.timer_next.start(900)

    def accept(self):
        if len(self.amend.amendedit1.text()) == 0:
            self.amend.messagelab.setText("提示!\n\t" + "原密码没有填写")
        elif len(self.amend.amendedit2.text()) == 0:
            self.amend.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif len(self.amend.amendedit3.text()) == 0:
            self.amend.messagelab.setText("提示!\n\t" + "新密码框不能为空！")
        elif self.amend.amendedit3.text() != self.amendedit2.text():
            self.amend.messagelab.setText("提示!\n\t" +"前后密码输入不一样！")
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            sign = 0
            for variate in c.fetchall():
                if variate[0] == UserOperation.number and variate[2] == self.amend.amendedit1.text():
                    conn.execute("update User set password=(?) where number=(?)",
                                 (self.amend.amendedit2.text(), variate[0],))
                    conn.commit()
                    sign = 1
                    break
            c.close()
            conn.close()
            if sign == 0:
                self.amend.messagelab.setText("提示!\n\t" + "原密码输入错误！！")
                self.sign = 1
            else:
                self.amend.messagelab.setText("提示!\n\t" + "修改成功！！")
                try:
                    self.timer_next.stop()
                    self.timer_camera.stop()
                    self_cap.release()  # 释放视频流
                    self.amend.newlab.clear()
                except:
                    pass
                time.sleep(1)
                UserOperation.win.splitter.widget(0).setParent(None)
                UserOperation.win.splitter.insertWidget(0, User_Myself.User_Myself())