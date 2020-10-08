from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.Logon_win import Logon_win
from UserOperation import self_cap,self_CAM_NUM
import time,sqlite3
import cv2
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserOperation import Record,User_informent

#用户注册操作类
class Logon(QFrame):
    def __init__(self):
        super(Logon, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.logon = Logon_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.logon)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.sign  = 1
        self.number = ''
        self.passw = ''
        self.data = []
        self.data1 = []
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.logon.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        self.face = show[self.logon.newlab.y1:self.logon.newlab.y2,
                           self.logon.newlab.x1:self.logon.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.logon.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        print(fingers)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 125 and x < 225 and y > 270 and y < 340:
                    # 返回
                    self.logon.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功")
                    self.change_record()
                elif x > 375 and x < 475 and y > 270 and y < 340:
                    # 上一步
                    self.logon.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.number = self.data[-1]
                            self.logon.usrLine.setText(self.number)
                            self.data = self.data[:-1]
                        else:
                            self.number = ''
                            self.logon.usrLine.setText(self.number)
                            self.data = []
                        self.logon.messagelab.setText("提示!\n\t" +
                                                "请您把账号分段输入，再输入确定！！")
                    elif sign == 2:
                        self.number = self.data[-1]
                        self.logon.usrLine.setText(self.number)
                        self.data = self.data[:-1]
                        self.sign = 1
                        self.logon.messagelab.setText("提示!\n\t" +
                                                "请您把账号分段输入，再输入确定！！")
                    elif sign == 3:
                        if len(self.data1) > 0:
                            self.passw = self.data1[-1]
                            self.logon.pwdLineEdit1.setText(self.passw)
                            self.data1 = self.data1[:-1]
                            self.logon.messagelab.setText("提示!\n\t" +
                                                    "请您把密码输入后，再输入确定！！")
                        else:
                            self.passw = ''
                            self.logon.pwdLineEdit1.setText(self.passw)
                            self.data1 = []
                            self.usrnameLine.setText("")
                            self.sign = 2
                            self.logon.messagelab.setText("提示!\n\t" +
                                                    "请您把用户名输入后，再输入确定！！")
                elif x > 125 and x < 225 and y > 410 and y < 480:
                    # 确定
                    self.logon.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()
                elif x > 375 and x < 475 and y > 410 and y < 480:
                    # 注册
                    self.logon.messagelab.setText("提示!\n" + "本次操作为：注册\n操作成功")
                    self.accept()

    # 识别操作区的手写文字
    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.logon.setextlab.setText("正在识别输入中．．")
        self.logon.progresslab.setMovie(self.logon.movie)
        self.logon.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()


    # 将操作区识别出来的文字写入界面
    def contrast_answer_right(self):
        self.logon.movie.stop()
        self.logon.progresslab.clear()
        self.logon.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.logon.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.logon.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            if len(self.number) < 11:
                if data[1] > 0.6:
                    try:
                        da = data[0].replace('I','1').replace('l','1').replace('b','6').replace('q','9')
                    except:
                        da  = data[0]
                    self.data.append(self.number)
                    self.number = self.number + da
                    self.logon.usrLine.setText(self.number)
                    self.logon.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t" +
                                            "如果输入错误请您在操作区输入＇上一步＇操作！！")
            if len(self.number) != 11:
                pass
            elif (self.checking1()):
                self.logon.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n请您先登录！")
            else:
                self.logon.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入昵称\n\t" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            self.logon.usrnameLine.setText(data[0])
            self.logon.messagelab.setText("提示!\n\t" + "用户名输入成功！请您输入密码(每次输入的数字不能超过四位数)\n\t" +
                                    "如果输入错误请您在操作区输入＇上一步＇操作！！")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.logon.pwdLineEdit1.setText(self.passw)
                self.logon.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
        time.sleep(1)
        self.timer_next.start(900)


    # 注册时输入的号码检验是否已经注册过的
    def checking1(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.logon.usrLine.text():
                return True
        c.close()
        conn.close()
        return False

    # 登录时密码在数据库中保存过来
    def save_data(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        a = self.logon.usrLine.text()
        b = self.logon.usrnameLine.text()
        c = self.logon.pwdLineEdit1.text()
        conn.execute("INSERT INTO User VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    # 注册时将账号密码保存并登录。
    def accept(self):
        if len(self.logon.usrLine.text()) == 0:
            self.logon.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.logon.usrLine.text()) != 11:
            self.logon.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif (self.checking1()):
            self.logon.messagelab.setText("提示!\n\t" + "您输入的号码已注册！\n\t请您登录！")
            self.sign = 1
        elif (len(self.logon.usrnameLine.text()) == 0):
            self.logon.messagelab.setText("提示!\n\t" + "用户名不能为空！")
            self.sign = 2
        elif len(self.logon.pwdLineEdit1.text()) == 0:
            self.logon.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            try:
                self.timer_next.stop()
                self.timer_camera.stop()
                self_cap.release()  # 释放视频流
                self.logon.newlab.clear()
            except:
                pass
            UserOperation.number = self.logon.usrLine.text()
            self.save_data()
            UserOperation.win.splitter.widget(0).setParent(None)
            UserOperation.win.splitter.insertWidget(0, User_informent.User_informent())
            # 连接主窗口界面。

    # 连接用户登录界面
    def change_record(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.logon.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Record.Record())