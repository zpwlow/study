import cv2
from PyQt5.QtWidgets import QWidget, QLabel,QGridLayout,QListWidget,QToolBox
from PyQt5.QtWidgets import QApplication,QHBoxLayout,QListWidgetItem
from PyQt5.QtGui import QPixmap, QMovie, QColor, QIcon, QImage
from PyQt5.QtCore import QSize, QTimer
import base64
from UserInterface.MyLabel import MyLabel
from UserOperation import self_cap, self_CAM_NUM


class AddCourse_win(QWidget):
    def __init__(self):
        super(AddCourse_win, self).__init__()
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.setWindowTitle("添加课程")
        self.setWindowIcon(QIcon("./datas/logo.ico"))
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.face = None
        self.newlab.setocr(220, 150, 380, 230, "输入区")
        self.newlab.setxy(75, 300, 175, 370, "关闭")
        self.newlab.setxy(250, 300, 350, 370, "搜索")
        self.newlab.setxy(425, 300, 525, 370, "加入")
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):

        self.resize(self.width1 , self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪

        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1/2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.qtool.setMaximumSize(self.width1/2, self.height1-100)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.messagelab, 0, 11, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.qtool, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")

        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image,self.face))
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
        self.face = show[self.forget.newlab.y1:self.forget.newlab.y2,
                    self.forget.newlab.x1:self.forget.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.newlab.setPixmap(QPixmap.fromImage(showImage))


class CourseQlist(QListWidget):
    def __init__(self,  datas):
        super(CourseQlist, self).__init__()
        item = QListWidgetItem(self)
        item.setSizeHint(QSize(800, 200))
        item.setBackground(QColor(240, 240, 240))
        self.setItemWidget(item, CourseWidget(datas))


class CourseWidget(QWidget):
    def __init__(self, data):
        super(CourseWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.data = data
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.imagelab = QLabel()
        self.numlab = QLabel("课程号:")
        self.numlab2 = QLabel(data[0])
        self.namelab = QLabel("课程名:")
        self.namelab2 = QLabel(data[1])
        self.teacherlab = QLabel("教师:")
        self.teacherlab2 = QLabel(data[2])
        self.image_path = "./datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.namelab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.numlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(200, 200)
        self.namelab.setMaximumSize(80, 40)
        self.numlab.setMaximumSize(80,40)
        self.teacherlab.setMaximumSize(80,40)
        self.namelab2.setMaximumSize(200, 40)
        self.numlab2.setMaximumSize(200, 40)
        self.teacherlab2.setMaximumSize(200, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 5, 3)
        self.layout.addWidget(self.numlab, 0, 3, 1, 1)
        self.layout.addWidget(self.namelab, 1, 3, 1, 1)
        self.layout.addWidget(self.teacherlab,2,3,1,1)
        self.layout.addWidget(self.numlab2, 0, 4, 1, 3)
        self.layout.addWidget(self.namelab2, 1, 4, 1, 3)
        self.layout.addWidget(self.teacherlab2, 2, 4, 1, 3)

