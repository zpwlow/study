from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtGui import QImage,QPixmap,QMovie
from PyQt5.QtCore import QTimer
from UserInterface.User_Record_win import User_Record_win
from UserOperation import self_cap,self_CAM_NUM
import time,sqlite3
import cv2,sys,datetime
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserOperation import Logon,Forget,Function



# 用户登录操作类
class Record(QFrame):
    def __init__(self):
        super(Record, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.record_win = User_Record_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.record_win)
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
                self.record_win.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    #获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        self.face = show[self.record_win.newlab.y1:self.record_win.newlab.y2,
                           self.record_win.newlab.x1:self.record_win.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.record_win.newlab.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框

    #识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            print(fingers)
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 75 and x < 175 and y > 270 and y < 340:
                    # 上一步
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：上一步\n\t操作成功")
                    sign = self.sign
                    if sign == 1:
                        if len(self.data) > 0:
                            self.number = self.data[-1]
                            self.record_win.usrLineEdit.setText(self.number)
                            self.data = self.data[:-1]
                        else:
                            self.number = ''
                            self.record_win.usrLineEdit.setText(self.number)
                            self.data = []
                        self.record_win.messagelab.setText("提示!\n\t" +
                                                           "请您把账号分段输入，再输入确定！！")
                    elif sign == 2:
                        if len(self.data1) > 0:
                            self.passw = self.data1[-1]
                            self.record_win.pwdLineEdit.setText(self.passw)
                            self.data1 = self.data1[:-1]
                            self.record_win.messagelab.setText("提示!\n\t" +
                                                               "请您把密码分段输入，再输入确定！！")
                        else:
                            self.passw = ''
                            self.record_win.pwdLineEdit.setText(self.passw)
                            self.data1 = []
                            self.sign = 1
                            self.number = self.data[-1]
                            self.record_win.usrLineEdit.setText(self.number)
                            self.data = self.data[:-1]
                            self.record_win.messagelab.setText("提示!\n\t" +
                                                               "请您把账号分段输入，再输入确定！！")
                elif x > 250 and x < 350 and y > 270 and y < 340:
                    # 确定
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功")
                    self.contrast_answer()

                elif x > 425 and x < 525 and y > 270 and y < 340:
                    # 退出
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：退出\n\t操作成功")
                    time.sleep(1)
                    try:
                        self.timer_next.stop()
                        self.timer_camera.stop()
                        self_cap.release()  # 释放视频流
                        self.record_win.newlab.clear()
                    except:
                        pass
                    UserOperation.win.close()
                    sys.exit()
                elif x > 75 and x < 175 and y > 410 and y < 480:
                    # 忘记密码
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：忘记密码\n\t操作成功")
                    time.sleep(1)
                    self.forgetfun()
                elif x > 250 and x < 350 and y > 410 and y < 480:
                    # 登录
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：登录\n\t操作成功")
                    time.sleep(1)
                    self.accept()

                elif x > 425 and x < 525 and y > 410 and y < 480:
                    # 注册
                    self.record_win.messagelab.setText("提示!\n\t" + "本次操作为：注册\n\t操作成功")
                    time.sleep(1)
                    self.logonfun()


    #识别操作区的手写文字
    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.record_win.setextlab.setText("正在识别输入中．．")
        self.record_win.progresslab.clear()
        self.record_win.progresslab.setMovie(self.record_win.movie)
        self.record_win.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    #将操作区识别出来的文字写入界面
    def contrast_answer_right(self):
        self.record_win.movie.stop()
        self.record_win.progresslab.clear()
        self.record_win.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.record_win.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.record_win.setextlab.clear()
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
                    self.record_win.usrLineEdit.setText(self.number)
                    self.record_win.messagelab.setText("提示!\n\t" + "部分号码输入成功！请您继续输入\n\t"
                                                  +"如果输入错误请您手指指在＇上一步＇操作！！")
            if len(self.number)!=11:
                pass
            elif (self.checking1()):
                self.record_win.messagelab.setText("提示!\n\t" +
                                                   "您输入的号码未注册！\n\t请您先注册！")
            else:
                self.record_win.messagelab.setText("提示!\n\t" + "号码输入成功！请您输入密码\n\t" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
                self.sign = 2
        elif self.sign == 2:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.data1.append(self.passw)
                self.passw = self.passw + da
                self.record_win.pwdLineEdit.setText(self.passw)
                self.record_win.messagelab.setText("提示!\n\t" + "部分密码输入成功！\n" +
                                        "如果输入错误请您在操作区输入＇上一步＇操作！！")
        time.sleep(1)
        self.timer_next.start(900)

    # 连接注册界面
    def logonfun(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.record_win.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Logon.Logon())

    # 登录时检验号码是否没有注册
    def checking1(self):
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User")
        for variate in c.fetchall():
            if variate[0] == self.record_win.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    # 登录时判断密码是否正确
    def accept(self):
        if len(self.record_win.usrLineEdit.text()) == 0:
            self.record_win.messagelab.setText("提示!\n\t" + "号码不能为空！")
            self.sign = 1
        elif len(self.record_win.usrLineEdit.text()) != 11:
            self.record_win.messagelab.setText("提示!\n\t" + "您输入的号码是错误的！\n\t请重新输入")
            self.sign = 1
        elif (self.checking1()):
            self.record_win.messagelab.setText("提示!\n\t" + "您输入的号码未注册！\n\t请您先注册！")
            self.sign = 1
        elif len(self.record_win.pwdLineEdit.text()) == 0:
            self.record_win.messagelab.setText("提示!\n\t" + "密码不能为空！")
            self.sign = 3
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from User")
            d = 0
            for variate in c.fetchall():
                if variate[0] == self.record_win.usrLineEdit.text() \
                        and variate[2] == self.record_win.pwdLineEdit.text():
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:  # 连接主界面函数
                try:
                    self.timer_next.stop()
                    self.timer_camera.stop()
                    self_cap.release()  # 释放视频流
                    self.record_win.newlab.clear()
                except:
                    pass
                UserOperation.number = self.record_win.usrLineEdit.text()
                self.finddata()
                UserOperation.win.splitter.widget(0).setParent(None)
                UserOperation.win.splitter.insertWidget(0, Function.Function())
            else:
                self.record_win.messagelab.setText("提示!\n\t"+ "账号或密码输入错误")

    # 连接忘记密码界面
    def forgetfun(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.newlab.clear()
        except:
            pass
        UserOperation.win.splitter.widget(0).setParent(None)
        UserOperation.win.splitter.insertWidget(0, Forget.Forget())
    
    #保存用户的登录时间
    def finddata(self):
        time1 = datetime.datetime.now()
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date")
        for variate in c.fetchall():
            if variate[0] == UserOperation.number:
                abcd = '%Y-%m-%d %H:%M:%S'
                b = datetime.datetime.strptime(variate[4], abcd)
                theTime = time1.strftime(abcd)
                if b.year == time1.year and b.month == time1.month and b.day == time1.day:
                    a = variate[2]
                else:
                    a = variate[2] + 1
                c.execute("update Student_date set logonday=(?),lasttime = (?) where number = (?)",
                          (a, theTime, UserOperation.number))
                conn.commit()
                break
        c.close()
        conn.close()


