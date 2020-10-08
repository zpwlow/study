from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.User_informent_win import User_informent_win
from UserOperation import self_cap,self_CAM_NUM
import time,sqlite3,base64
import cv2,datetime
from UserOperation.FingerDetection import figer_number
from UserOperation.ContrastJob import ContrastJob
import UserOperation
from UserOperation import Function

class User_informent(QFrame):
    def __init__(self):
        super(User_informent, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.informent = User_informent_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.forget)
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
                self.informent.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        self.face = show[self.informent.newlab.y1:self.informent.newlab.y2,
                           self.informent.newlab.x1:self.informent.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.informent.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 75 and x < 175 and y > 320 and y < 390:
                    # 完成
                    self.informent.messagelab.setText("提示!\n\t"
                                                      + "本次操作为：完成\n\t操作成功!")
                    self.connect_fun()
                elif x > 250 and x < 350 and y > 320 and y < 390:
                    # 上一步
                    self.informent.messagelab.setText("提示!\n\t"
                                                      + "本次操作为：上一步\n\t操作成功!")
                    sign = self.sign
                    if sign == 1:
                        self.informent.nameEdit.setText("")
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的姓名输入输入区后，再在操作区输入确定！！")
                    elif sign == 2:
                        self.informent.nameEdit.setText("")
                        self.sign = 1
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的姓名输入输入区后，再在操作区输入确定！！")
                    elif sign == 3:
                        self.informent.sexEdit.setText("")
                        self.sign = 2
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的性别输入输入区后，再在操作区＇输入确定！！")
                    elif sign == 4:
                        self.informent.yearEdit.setText("")
                        self.sign = 3
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的出生年月输入输入区后，再在操作区输入确定！！")
                    elif sign == 5:
                        self.informent.schoolEiit.setText("")
                        self.sign = 4
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的学校输入输入区后，再在操作区输入确定！！")
                    elif sign == 6:
                        self.informent.gradeEdit.setText("")
                        self.sign = 5
                        self.informent.messagelab.setText("提示!\n\t" +
                                                "请把您的年级输入输入区后，再在操作区输入确定！！")
                elif x > 425 and x < 525 and y > 320 and y < 390:
                    # 确定
                    self.informent.messagelab.setText("提示!\n\t" + "本次操作为：确定\n\t操作成功!")
                    self.contrast_answer()

    # 识别操作区的手写文字
    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.informent.setextlab.setText("正在识别输入中．．")
        self.informent.progresslab.setMovie(self.informent.movie)
        self.informent.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    # 将操作区识别出来的文字写入界面
    def contrast_answer_right(self):
        self.informent.movie.stop()
        self.informent.progresslab.clear()
        self.informent.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.informent.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.setextlab.clear()
        data = self.contrastjob.getanswer()
        if self.sign == 1:
            self.informent.nameEdit.setText(data[0])
            self.informent.messagelab.setText("提示!\n\t" + "姓名输入成功！请您下一步输入性别\n\t" +
                                    "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 2
        elif self.sign == 2:
            self.informent.sexEdit.setText(data[0])
            self.informent.messagelab.setText("提示!\n\t" + "性别输入成功！请您下一步输入出生年月\n\t" +
                                    "如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 3
        elif self.sign == 3:
            if data[1] > 0.6:
                try:
                    da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
                except:
                    da = data[0]
                self.informent.yearEdit.setText(da)
                self.informent.messagelab.setText("提示!\n\t" + "出生年月输入成功！请您下一步输入学校" +
                                        "\n\t如果输入错误请您操作区输入＇上一步＇操作")
                self.sign = 4
        elif self.sign == 4:
            self.informent.schoolEiit.setText(data[0])
            self.informent.messagelab.setText("提示!\n\t" + "学校输入成功！请您下一步输入年级" +
                                    "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 5
        elif self.sign == 5:
            self.informent.gradeEdit.setText(data[0])
            self.informent.messagelab.setText("提示!\n\t" + "年级输入成功！" +
                                    "\n\t如果输入错误请您操作区输入＇上一步＇操作")
            self.sign = 6
        time.sleep(1)
        self.timer_next.start(900)

    #连接用户主界面
    def connect_fun(self):
        if len(self.informent.nameEdit.text()) == 0:
            self.informent.messagelab.setText("提示!\n\t" + "姓名框不能为空！！")
            self.sign = 1
        elif len(self.informent.sexEdit.text()) == 0:
            self.informent.messagelab.setText("提示!\n\t" + "性别框不能为空！！")
            self.sign = 2
        elif len(self.yearEdit.text()) == 0:
            self.informent.messagelab.setText("提示!\n\t" + "出生年月框不能为空！！")
            self.sign = 3
        elif len(self.informent.schoolEiit.text()) == 0:
            self.informent.messagelab.setText("提示!\n\t" + "学校框不能为空！！")
            self.sign = 4
        elif len(self.informent.gradeEdit.text()) == 0:
            self.informent.messagelab.setText("提示!\n\t" + "年级框不能为空！！")
            self.sign = 5
        else:
            try:
                self.timer_next.stop()
                self.timer_camera.stop()
                self_cap.release()  # 释放视频流
                self.informent.newlab.clear()
            except:
                pass
            self.save_data()
            UserOperation.win.splitter.widget(0).setParent(None)
            UserOperation.win.splitter.insertWidget(0, Function.Function())

    #保存用户的信息
    def save_data(self):
        self.image_path = "./datas/image/a7.jpeg"
        a = self.informent.nameEdit.text()
        b = self.informent.yearEdit.text()
        c = self.informent.sexEdit.text()
        d = self.informent.schoolEiit.text()
        e = self.informent.gradeEdit.text()
        print(10)
        with open(self.image_path, "rb") as f:
            total = base64.b64encode(f.read())  # 将文件转换为字节。
        f.close()
        print(0)
        ab = '%Y-%m-%d %H:%M:%S'
        theTime = datetime.datetime.now().strftime(ab)
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_date VALUES(?,?,?,?,?,?)",
                     (UserOperation.number, a, b, c, d, e))
        conn.execute("insert into User_image values(?,?,?)",
                     (UserOperation.number, total, '.jpeg',))
        conn.execute("INSERT INTO Student_date VALUES(?,?,?,?,?)",
                     (UserOperation.number, theTime, 1, 0.0, theTime))
        conn.commit()
        conn.close()
        print(101)
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        try:  # 开始时间  ， 课程号，课程名， 文件名 ， 结束时间
            c.execute('''CREATE TABLE User_data(strat_time text,
                Cno text,Coursename text, filename text,last_time text)''')
        except:
            pass
        c.close()
        conn.close()

