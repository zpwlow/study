from PyQt5.QtWidgets import QFrame,QHBoxLayout,QWidget
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
from UserInterface.AddCourse_win import AddCourse_win,CourseQlist
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3,datetime
from UserOperation.ContrastJob import ContrastJob
from UserOperation.FingerDetection import figer_number
import UserOperation

class My_Course(QWidget):
    def __init__(self):
        super(My_Course, self).__init__()
        self.addcourse = AddCourse_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.addcourse)
        self.sign = 0
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(self.finger_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                self.addcourse.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_next.start(900)

    # 获取视频流装换为图片放在QLabel中
    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        self.face = show[self.addcourse.newlab.y1:self.addcourse.newlab.y2,
                    self.addcourse.newlab.x1:self.addcourse.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.addcourse.newlab.setPixmap(QPixmap.fromImage(showImage))

    # 识别手指指的操作命令
    def finger_camera(self):
        fingers = figer_number(self.image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 75 and x < 175 and y > 300 and y < 370:
                    # 关闭
                    self.addcourse.messagelab.setText("提示!\n\t" + "本次操作为：关闭\n\t操作成功")
                    self.clear_cap()
                    self.close()
                elif x > 250 and x < 350 and y > 300 and y < 370:
                    # 搜索
                    self.addcourse.messagelab.setText("提示!\n\t" + "本次操作为：搜索\n\t操作成功")
                    self.contrast_answer()
                elif x > 425 and x < 525 and y > 300 and y < 370:
                    # 加入
                    self.addcourse.messagelab.setText("提示!\n\t" + "本次操作为：加入\n\t操作成功")
                    self.joinfun()

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.timer_next.stop()
            self.timer_camera.stop()
            self_cap.release()  # 释放视频流
        except:
            pass
        self.newlab.clear()


    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    #检测窗口关闭发射信号
    def closeEvent(self, event):
        self.sendEditContent()

    #识别输入区的手写数字
    def contrast_answer(self):
        self.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.addcourse.setextlab.setText("正在识别输入中．．")
        self.addcourse.progresslab.setMovie(self.addcourse.movie)
        self.addcourse.movie.start()
        cv2.imwrite(imgpath, self.face)
        self.contrastjob = ContrastJob(imgpath)
        self.contrastjob.updated.connect(self.chang_fun)
        self.contrastjob.start()

    #将识别的输入信息写在界面
    def chang_fun(self):
        self.addcourse.movie.stop()
        self.addcourse.progresslab.clear()
        self.addcourse.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.addcourse.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.addcourse.setextlab.clear()
        data = self.contrastjob.getanswer()
        x = 0
        if data[1] > 0.6:
            x = 1
            try:
                da = data[0].replace('I', '1').replace('l', '1').replace('b','6').replace('q','9')
            except:
                da = data[0]

            self.addcourse.messagelab.setText("提示!\n\t" + "本次搜索内容为：" + da)
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select Course.Cno,Course.name,Controller_data.name,numble,total,filename \
                                                  from Course,Controller_data,Course_image,Teacher_Course \
                                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                                   and Teacher_Course.number=Controller_data.number and \
                                                    Course.Cno=(?)", (da,))
            self.datas = c.fetchall()
            if len(self.datas) > 0:
                self.data = self.datas[0]
                self.coursewin = CourseQlist(self.data)
                self.addcourse.qtool.removeItem(0)
                self.addcourse.qtool.addItem(self.coursewin, '查找的课程')
                self.addcourse.qtool.setStyleSheet("QToolBox{background:rgb(240,240,240);font-weight:Bold;color:rgb(0,0,0);}")
            else:
                try:
                    self.addcourse.qtool.removeItem(0)
                except:
                    pass
                self.addcourse.messagelab.setText("提示!\n\t" + "没有找到课程号为:'" + da + "'的信息!!!")
        if x==0:
            self.addcourse.messagelab.setText("提示!\n\t" + "没有找到课程" + "的任何信息!!!")
            try:
                self.addcourse.qtool.removeItem(0)
            except:
                pass
        self.timer_next.start(900)

    #加入课程
    def joinfun(self):
        if len(self.data)>0:
            ab = '%Y-%m-%d %H:%M:%S'
            theTime = datetime.datetime.now().strftime(ab)
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from Join_Course where number=(?) and Cno=(?)",
                               (UserOperation.number, self.data[0],))
            n = len(c.fetchall())
            if n > 0:
                c.close()
                conn.close()
                self.addcourse.messagelab.setText("提示!\n\t" +
                                                  "您已经加入此课程了!\n\t不用重复加入!!")
            else:
                c.execute("insert into Join_Course values(?,?,?)",
                               (UserOperation.number, self.data[0], theTime,))
                c.execute("insert into Coursetime values(?,?,?)",
                                 (UserOperation.number, self.data[0], 0.0,))
                c.execute("update Course set numble=(?) where Cno=(?)",
                                  (self.data[3] + 1, self.data[0],))
                conn.commit()
                c.close()
                conn.close()
                self.addcourse.messagelab.setText("提示!\n\t" + "加入成功!!!")
        else:
            self.addcourse.messagelab.setText("提示!\n\t" + "您没有搜索出任何课程，请重新搜索!!!")