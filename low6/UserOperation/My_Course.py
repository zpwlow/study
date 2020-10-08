from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from UserInterface.My_Course_win import My_Course_win,Coursewindow
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation import Function,AddCourse,Course_news

class My_Course(QFrame):
    def __init__(self):
        super(My_Course, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.course = My_Course_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.course)
        self.sign = 0
        conn = sqlite3.connect('./datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                  from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                    and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                    and Join_Course.number=(?)", (UserOperation.number,))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = Coursewindow(self.datas, self.sign)
        self.course.qtool.addItem(self.window1, "我的课程")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.course.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
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
        self.course.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 45 and x < 125 and y > 60 and y < 130:
                    # 返回
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function.Function())
                elif x > 170 and x < 250 and y > 60 and y < 130:
                    # 添加课程
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：添加课程\n\t操作成功！！")
                    self.clear_cap()
                    self.add = AddCourse.AddCourse()
                    # 接受子窗口传回来的信号  然后调用主界面的函数
                    self.add.my_Signal.connect(self.changfun)
                    self.add.show()
                elif x > 45 and x < 125 and y > 190 and y < 260:
                    # 上一页
                    self.timer_next.stop()
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                    self.cut_images()
                elif x > 170 and x < 250 and y > 190 and y < 260:
                    # 下一页
                    self.timer_next.stop()
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                    self.add_images()
                elif x > 45 and x < 125 and y > 320 and y < 390:
                    # 课程一
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：课程一\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 0][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news.Course_news(data))
                elif x > 170 and x < 250 and y > 320 and y < 390:
                    # 课程二
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：课程二\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 1][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news.Course_news(data))
                elif x > 295 and x < 375 and y > 320 and y < 390:
                    # 课程三
                    self.course.messagelab.setText("提示!\n\t" + "本次操作为：课程三\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 2][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news.Course_news(data))

    #暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        self.course.newlab.clear()

    # 上一页课程
    def cut_images(self):
        self.sign = self.sign - 3
        if self.sign <0:
            self.sign=0
        self.course.qtool.removeItem(0)
        self.window1 = Coursewindow(self.datas, self.sign)
        self.course.qtool.addItem(self.window1, self.data[2])
        self.timer_next.start(900)

    # 下一页课程
    def add_images(self):
        self.equal =1
        self.sign = self.sign +3
        n = len(self.datas)
        if n>self.sign:
            self.course.qtool.removeItem(0)
            self.window1 = Coursewindow(self.datas, self.sign)
            self.course.qtool.addItem(self.window1, self.data[2])
        else:
            self.sign = self.sign - 3
        self.timer_next.start(900)

    #添加完课程后更新课程列表
    def changfun(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.course.messagelab.setText("提示!\n\t" +"请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)
                self.equal = 0
                self.course.qtool.removeItem(0)
                conn = sqlite3.connect('./datas/database/Information.db')
                c = conn.cursor()
                c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                         from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                          where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                           and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                           and Join_Course.number=(?)", (UserOperation.number,))
                self.datas = c.fetchall()
                c.close()
                conn.close()
                self.window1 = Coursewindow(self.datas, self.sign)
                self.course.qtool.addItem(self.window1, '我的课程')