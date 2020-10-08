from PyQt5.QtWidgets import QHBoxLayout,QWidget
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.Practice_widget_win import Practice_widget_win
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3,os,glob,time,datetime
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import ContrastJob

class Practice_widget(QWidget):
    def __init__(self,dow,data1,data2,data3):
        super(Practice_widget, self).__init__()
        self.startime = datetime.datetime.now()
        self.pa = './datas/tupian'
        self.a = 0
        self.dow = dow
        self.data1 = data1
        self.data2 = data2[0]
        self.data3 = data3

        list3 = data2[2].split("@")
        self.answers = []
        for list in list3:
            da = list.split("#")
            self.answers.append(da)
        self.fileNames = glob.glob(self.pa + r'/*')
        self.practice = Practice_widget_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.practice)
        self.pa = self.fileNames[self.a]
        self.filename = os.path.split(self.pa)[1]
        pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.practice.imagelab.setPixmap(pixmap)  # 在label上显示图片
        self.practice.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.practice.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        self.face = show[self.practice.newlab.y1:self.practice.newlab.y2,
                    self.practice.newlab.x1:self.practice.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.practice.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 125 and x < 225 and y > 270 and y < 340:
                    # 关闭
                    self.practice.messagelab.setText("提示!\n\t" + "本次操作为：关闭\n\t操作成功")
                    self.closewin()
                elif x > 375 and x < 475 and y > 270 and y < 340:
                    # 验证答案
                    self.practice.messagelab.setText("提示!\n\t" + "本次操作为：验证答案\n\t操作成功")
                    self.contrast_answer()
                elif x > 125 and x < 225 and y > 410 and y < 480:
                    # 上一题
                    self.practice.messagelab.setText("提示!\n\t" + "本次操作为：上一题\n\t操作成功")
                    self.lastfun()
                elif x > 375 and x < 475 and y > 410 and y < 480:
                    # 下一题
                    self.practice.messagelab.setText("提示!\n\t" + "本次操作为：下一题\n\t操作成功")
                    self.addfun()

    #关闭窗口
    def closewin(self):
        self.timer_next.stop()
        try:
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
            self.practice.newlab.clear()
        except:
            pass
        ab = '%Y-%m-%d %H:%M:%S'
        endtime = datetime.datetime.now()
        b = endtime - self.startime
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Student_date where number=(?)", (UserOperation.number,))
        data = c.fetchall()[0]
        da = data[3] + b.seconds
        conn.execute("update Student_date set stude_day =(?) where number=(?)",
                     (da, UserOperation.number))
        conn.commit()
        c.execute("select * from Coursetime where number=(?) and Cno=(?)",
                  (UserOperation.number, self.data1))
        data = c.fetchall()[0]
        da = data[2] + b.seconds
        conn.execute("update Coursetime set time =(?) where number=(?)and Cno=(?)",
                     (da, UserOperation.number, self.data1))
        conn.commit()
        conn.close()
        sqlpath = "./datas/database/SQ" + str(UserOperation.number) + "L.db"
        conn = sqlite3.connect(sqlpath)
        conn.execute("INSERT INTO User_data VALUES(?,?,?,?,?)",
                     (self.startime.strftime(ab), self.data1, self.data2, self.data3, endtime.strftime(ab)))
        conn.commit()
        conn.close()
        self.close()
        self.dow.changetime()

    #识别输入区的答案
    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.practice.setextlab.setText("正在识别输入中．．")
        self.practice.progresslab.setMovie(self.practice.movie)
        self.practice.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.contrast_answer_right)
        self.contrastjob.start()

    #判断答案是否正确,正确则输出
    def contrast_answer_right(self):
        self.practice.movie.stop()
        self.practice.progresslab.clear()
        self.practice.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.practice.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.practice.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        da = data[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9')
        if data[1] > 0.85:
            for answer in self.answers:
                if answer[0] == self.filename:
                    if answer[1] == da:
                        self.practice.answerlab.setText("答案：" +
                                                        answer[1] + "\n解析:\n" + answer[2])
                        self.practice.messagelab.setText("提示!\n\t" + "回答正确！！")
                        x = 1
                        time.sleep(3)
        else:
            self.practice.messagelab.setText("提示!\n\t"+ "请写入答案后再验证答案！！！")
        if x==0:
            self.practice.messagelab.setText("提示!\n\t" + "回答错误\n\t请把正确答案放置在答案区！！")
            self.practice.answerlab.setText("")
        self.timer_next.start(900)

    #下一题
    def addfun(self):
        self.timer_next.stop()
        self.a = self.a + 1
        try:
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.practice.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.practice.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.answerlab.clear()
        except:
            self.a = self.a - 1
            self.pa = self.fileNames[self.a]
            self.practice.messagelab.setText("提示!\n\t"+"这是最后一题")
        self.timer_next.start(900)

    #上一题
    def lastfun(self):
        self.a = self.a - 1
        if self.a < 0:
            self.a = self.a + 1
            self.practice.messagelab.setText("提示!\n\t"+"这是第一题")
        else:
            self.timer_next.stop()
            self.pa = self.fileNames[self.a]
            self.filename = os.path.split(self.pa)[1]
            pixmap = QPixmap(self.pa)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.practice.imagelab.setPixmap(pixmap)  # 在label上显示图片
            self.practice.imagelab.setScaledContents(True)  # 让图片自适应label大小
            self.answerlab.clear()
            self.timer_next.start(900)


