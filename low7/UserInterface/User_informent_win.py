from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QGridLayout, QLineEdit
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from PyQt5.QtGui import QFont
from UserInterface.MyLabel import MyLabel
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtCore import QTimer
from UserOperation import self_cap, self_CAM_NUM
from UserOperation import User_informent
import cv2


class User_informent_win(QFrame):
    def __init__(self):
        super(User_informent_win, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.name = QLabel("姓名:")
        self.year = QLabel("出生年月")
        self.yearEdit = QLineEdit()
        self.sex = QLabel("性别:")
        self.sexEdit = QLineEdit()
        self.school = QLabel("学校:")
        self.grade = QLabel("年级")
        self.gradeEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.schoolEiit = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel("输入区")  # 放置视频
        self.movie = QMovie("./datas/progress_bar.gif")
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_next = QTimer()  # 定义定时器，对题目进行识别．
        self.datalayer = User_informent.User_informent(self)
        self.image = None
        self.face = None
        self.newlab.setocr(220, 120, 380, 200, "输入区")
        self.newlab.setxy(75, 320, 175, 390, "上一步")
        self.newlab.setxy(250, 320, 350, 390, "确定")
        self.newlab.setxy(425, 320, 525, 390, "完成")
        self.devise_Ui()

    def devise_Ui(self):
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.sex.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.school.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.grade.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.name.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.year.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.nameEdit.setPlaceholderText("请在输入区输入姓名")
        self.yearEdit.setPlaceholderText("请在输入区输入年月如:201912")
        self.sexEdit.setPlaceholderText("请在输入区输入性别")
        self.schoolEiit.setPlaceholderText("请在输入区输入学校名称")
        self.gradeEdit.setPlaceholderText("请在输入区输入年级")
        self.nameEdit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.schoolEiit.setFont(QFont("宋体", 14))  # 设置QLineEditn 的字体及大小
        self.sexEdit.setFont(QFont("宋体", 14))
        self.yearEdit.setFont(QFont("宋体", 14))
        self.gradeEdit.setFont(QFont("宋体", 14))
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.name.setMaximumSize(100, 40)
        self.school.setMaximumSize(100, 40)
        self.year.setMaximumSize(100, 40)
        self.sex.setMaximumSize(100, 40)
        self.grade.setMaximumSize(100, 40)
        self.nameEdit.setMaximumSize(420, 40)
        self.schoolEiit.setMaximumSize(420, 40)
        self.sexEdit.setMaximumSize(420, 40)
        self.gradeEdit.setMaximumSize(420, 40)
        self.yearEdit.setMaximumSize(420, 40)
        self.layout.addWidget(self.messagelab, 0, 12, 3, 10)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 11, 12)
        self.layout.addWidget(self.name, 4, 13, 1, 2)
        self.layout.addWidget(self.nameEdit, 4, 15, 1, 8)
        self.layout.addWidget(self.sex, 6, 13, 1, 2)
        self.layout.addWidget(self.sexEdit, 6, 15, 1, 8)
        self.layout.addWidget(self.year, 8, 13, 1, 2)
        self.layout.addWidget(self.yearEdit, 8, 15, 1, 8)
        self.layout.addWidget(self.school, 10, 13, 1, 2)
        self.layout.addWidget(self.schoolEiit, 10, 15, 1, 8)
        self.layout.addWidget(self.grade, 12, 13, 1, 2)
        self.layout.addWidget(self.gradeEdit, 12, 15, 1, 8)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_next.timeout.connect(lambda: self.datalayer.finger_camera(self.image, self.face))
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
        self.face = show[self.informent.newlab.y1:self.informent.newlab.y2,
                    self.informent.newlab.x1:self.informent.newlab.x2]
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.informent.newlab.setPixmap(QPixmap.fromImage(showImage))
