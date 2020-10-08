from PyQt5.QtWidgets import QFrame,QHBoxLayout,QApplication,QMainWindow,QToolBox,QListWidgetItem
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QGridLayout,QSplitter,QListWidget
from PyQt5.QtGui import QImage,QPixmap,QFont,QCursor,QMovie,QIcon,QColor,QPalette
from PyQt5.QtCore import QTimer,Qt,QSize
from UserOperation import self_cap,self_CAM_NUM
import cv2,sqlite3,base64
from MyLabel import MyLabel
import sys,os


class User_Record_win(QWidget):
    def __init__(self):
        super(User_Record_win, self).__init__()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170, 150, 430, 250, "输入区")
        self.newlab.setxy(125, 300, 225, 370, "返回")
        self.newlab.setxy(375, 300, 475, 370, "查看答案")
        self.devise_ui()

    def devise_ui(self):
        palette1 = QPalette()
        palette1.setColor(palette1.Background, QColor(245, 245, 245))
        self.setPalette(palette1)
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:30px;font-weight:Bold;font-family:Arial;}")
        self.answerlab.setAlignment(Qt.AlignCenter)
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.answerlab.setMaximumSize(self.width1 / 2, self.height1 - 100)
        self.layout.addWidget(self.messagelab, 0, 11, 3, 10)
        self.layout.addWidget(self.progresslab, 3, 3, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 4, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.answerlab, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小


class Record(QFrame):  # 用户登录界面
    def __init__(self):
        super(Record, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.record_win = User_Record_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.record_win)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.timer_camera.timeout.connect(self.show_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                pass
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示


    def show_camera(self):
        flag, self.image = self_cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (600, 550))  # 把读到的帧的大小重新设置为 600x500
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        cv2.flip(show, -1, show)  #翻转镜像--->对角翻转.
        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.record_win.newlab.setPixmap(QPixmap.fromImage(showImage))
        # self.newlab.setCursor(Qt.CrossCursor) #可使用鼠标绘制方框


class QUnFrameWindow(QMainWindow):
    """
    无边框窗口类
    """
    def __init__(self):   #设置界面布局，界面大小，声名控件
        super(QUnFrameWindow, self).__init__(None) # 设置为顶级窗口
        self.setWindowTitle("low_User")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.desktop = QApplication.desktop() #获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        self.resize(self.x, self.y)
        self.number = '15812904182'
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.splitter.addWidget(Record())
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
        #close_mouse_and_key()

    def closeEvent(self, event):
        #open_mouse_and_key()
        # 清理一些 自己需要关闭的东西
        event.accept()  # 界面的关闭,但是会有一些时候退出不完全,需要调用 os 的_exit 完全退出
        try:
            os._exit(5)
        except:
            pass



#主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = QUnFrameWindow()

    win.show()
    sys.exit(app.exec_())

#用户登录界面
class Record_win(QWidget):
    def __init__(self):
        super(Record_win, self).__init__()
        self.usr = QLabel("用户:")
        self.password = QLabel("密码:")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.answerlab = QLabel()  # 放置答案的图片
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170,120,430,220,"输入区")
        self.newlab.setxy(75,270,175,340,"上一步")
        self.newlab.setxy(250, 270, 350, 340, "确定")
        self.newlab.setxy(425, 270, 525, 340, "退出")
        self.newlab.setxy(75, 410, 175, 480, "忘记密码")
        self.newlab.setxy(250, 410, 350, 480, "登录")
        self.newlab.setxy(425, 410, 525, 480, "注册")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.password.setMaximumSize(60, 60)
        # 设置QLabel 的字体颜色，大小,
        self.password.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.answerlab.setStyleSheet("QLabel{background-color:rgb(230,230, 230)}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit.setPlaceholderText("请在输入框输入手机号码(一次输入不能超过四位数)")
        self.usrLineEdit.setMaximumSize(420, 40)
        self.usrLineEdit.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit.setMaximumSize(420, 40)
        self.pwdLineEdit.setPlaceholderText("请在输入框输入密码(一次输入不能超过四位数)")
        self.pwdLineEdit.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.messagelab, 0, 12, 4, 7)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 2, 0, 10, 10)
        self.layout.addWidget(self.usr, 5, 11, 1, 1)
        self.layout.addWidget(self.usrLineEdit, 5, 12, 1, 8)
        self.layout.addWidget(self.password, 7, 11, 1, 1)
        self.layout.addWidget(self.pwdLineEdit, 7, 12, 1,8)
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

#用户注册界面
class Logon_win(QWidget):
    def __init__(self):
        super(Logon_win, self).__init__()
        self.usr = QLabel("用户:")
        self.usrname = QLabel("用户名：")
        self.password1 = QLabel("密码:")
        self.usrLine = QLineEdit()
        self.usrnameLine = QLineEdit()
        self.pwdLineEdit1 = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170, 120, 430, 220, "输入区")
        self.newlab.setxy(125, 270, 225, 340, "返回")
        self.newlab.setxy(375, 270, 475, 340, "上一步")
        self.newlab.setxy(125, 410, 225, 480, "确定")
        self.newlab.setxy(375, 410, 475, 480, "注册")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr.setMaximumSize(50, 40)
        self.usrname.setMaximumSize(60, 40)
        self.password1.setMaximumSize(50, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.usrname.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.password1.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.usrLine.setMaximumSize(420, 40)
        self.usrnameLine.setMaximumSize(420, 40)
        self.pwdLineEdit1.setMaximumSize(420, 40)
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLine.setPlaceholderText("请在输入区输入手机号码(一次输入不能超过四位数)")
        self.usrnameLine.setPlaceholderText("请在输入区输入您的昵称")
        self.pwdLineEdit1.setPlaceholderText("请在输入区输入密码(一次输入不能超过四位数)")
        self.usrLine.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.usrnameLine.setFont(QFont("宋体", 12))
        self.pwdLineEdit1.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.messagelab, 0, 13, 3, 10)
        self.layout.addWidget(self.progresslab, 0, 1, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 2, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 10, 12)
        self.layout.addWidget(self.usr, 5, 13, 1, 1)
        self.layout.addWidget(self.usrLine, 5, 14, 1, 10)
        self.layout.addWidget(self.usrname, 8, 13, 1, 1)
        self.layout.addWidget(self.usrnameLine, 8, 14, 1, 10)
        self.layout.addWidget(self.password1, 11, 13, 1, 1)
        self.layout.addWidget(self.pwdLineEdit1, 11, 14, 1, 10)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

#用户忘记密码界面
class Forget_win(QWidget):
    def __init__(self):
        super(Forget_win, self).__init__()
        self.usr2 = QLabel("用户:")
        self.pwd2 = QLabel("密码:")
        self.usrLineEdit2 = QLineEdit()
        self.pwdLineEdit2 = QLineEdit()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170, 120, 430, 220, "输入区")
        self.newlab.setxy(125, 270, 225, 340, "返回")
        self.newlab.setxy(375, 270, 475, 340, "上一步")
        self.newlab.setxy(125, 410, 225, 480, "确定")
        self.newlab.setxy(375, 410, 475, 480, "修改密码")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.usr2.setMaximumSize(50, 40)
        self.pwd2.setMaximumSize(50, 40)
        # 设置QLabel 的字体颜色，大小，
        self.usr2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.pwd2.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:18px;font-weight:Bold;font-family:Arial;}")
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.usrLineEdit2.setMaximumSize(420, 40)
        self.pwdLineEdit2.setMaximumSize(420, 40)
        self.usrLineEdit2.setPlaceholderText("请在输入区输入手机号码(一次输入不能超过四位数)")
        self.pwdLineEdit2.setPlaceholderText("请在输入区输入新的密码(一次输入不能超过四位数)")
        self.usrLineEdit2.setFont(QFont("宋体", 12))  # 设置QLineEditn 的字体及大小
        self.pwdLineEdit2.setFont(QFont("宋体", 12))
        self.layout.addWidget(self.messagelab, 0, 13, 3, 8)
        self.layout.addWidget(self.progresslab, 0, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 0, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 10, 12)
        self.layout.addWidget(self.usr2, 6, 13, 1, 1)
        self.layout.addWidget(self.usrLineEdit2, 6, 14, 1, 8)
        self.layout.addWidget(self.pwd2, 9, 13, 1, 1)
        self.layout.addWidget(self.pwdLineEdit2, 9, 14, 1, 8)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

#用户填写信息界面
class User_informent_win(QWidget):
    def __init__(self):
        super(User_informent_win, self).__init__()
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
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170, 120, 430, 220, "输入区")
        self.newlab.setxy(75, 320, 175, 390, "上一步")
        self.newlab.setxy(250, 320, 350, 390, "确定")
        self.newlab.setxy(425, 320, 525, 390, "完成")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
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
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

#用户功能界面
class Function_win(QWidget):
    def __init__(self):
        super(Function_win, self).__init__()
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setxy(75, 150, 175, 220, "查看课程")
        self.newlab.setxy(250, 150, 350, 220, "学习记录")
        self.newlab.setxy(425, 150, 525, 220, "我的")
        self.newlab.setxy(75, 330, 175, 400, "退出登录")
        self.newlab.setxy(250, 330, 350, 400, "退出程序")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 2
        self.width1 = self.screenRect.width() / 2
        self.resize(self.width1 * 2, self.height1 * 2)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1, 90)
        self.newlab.setMaximumSize(600, 550)
        self.layout.addWidget(self.messagelab, 0, 0, 4, 9)
        self.layout.addWidget(self.progresslab, 4, 11, 1, 1)
        self.layout.addWidget(self.setextlab, 4, 12, 1, 4)
        self.layout.addWidget(self.newlab, 5, 7, 10, 24)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

#我的课程界面
class My_Course_win(QWidget):
    def __init__(self):
        super(My_Course_win, self).__init__()
        self.sign = 0
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.qtool = QToolBox()
        self.newlab.setxy(45,60,125,130,"返回")
        self.newlab.setxy(170, 60, 250, 130, "添加课程")
        self.newlab.setxy(45, 190, 125, 260, "上一页")
        self.newlab.setxy(170, 190, 250, 260, "下一页")
        self.newlab.setxy(45, 320, 125, 390, "课程一")
        self.newlab.setxy(170, 320, 250, 390, "课程二")
        self.newlab.setxy(295, 320, 375, 390, "课程二")
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height() / 4
        self.width1 = self.screenRect.width() / 4
        self.resize(self.width1 * 4, self.height1 * 4)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        # self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 * 2, 90)
        self.newlab.setMaximumSize(450, 450)
        conn = sqlite3.connect('../datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                  from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                    and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                    and Join_Course.number=(?)", (15812904182,))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = Coursewindow(self.datas, self.sign)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.qtool.addItem(self.window1, "我的课程")
        self.layout.addWidget(self.messagelab, 0, 12, 3, 10)
        self.layout.addWidget(self.progresslab, 2, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 2, 3, 1, 4)
        self.layout.addWidget(self.newlab, 3, 0, 6, 8)
        self.layout.addWidget(self.qtool, 3, 8, 10, 14)
        self.messagelab.setText("提示!\n\t" + "输入区输入后请在操作区输入＇确定＇")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小

class CustomWidget(QWidget):
    def __init__(self, data,y):
        super(CustomWidget, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.win.setMouseTracking(True)  # 设置widget鼠标跟踪
        if y==0:
            text = "课程一: "
        elif y==1:
            text = "课程二: "
        elif y==2:
            text = "课程三: "
        self.imagelab = QLabel()
        self.namelab = QLabel(text+data[2])
        self.teacherlab = QLabel("老师:")
        self.teacherlab2 = QLabel(str(data[3]))
        self.image_path = "../datas/image/image" + data[5]
        total = base64.b64decode(data[4])
        f = open(self.image_path, 'wb')
        f.write(total)
        f.close()
        self.namelab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:20px;font-weight:Bold;font-family:Arial;}")
        self.teacherlab2.setStyleSheet("QLabel{color:rgb(0, 255, 0);font-size:22px;font-weight:Bold;font-family:Arial;}")
        self.imagelab.setMaximumSize(150, 150)
        self.namelab.setMaximumSize(400, 80)
        self.teacherlab.setMaximumSize(80, 40)
        self.teacherlab2.setMaximumSize(100, 40)
        self.imagelab.setPixmap(QPixmap(self.image_path))
        self.imagelab.setScaledContents(True)  # 让图片自适应label大小
        self.layout.addWidget(self.imagelab, 0, 0, 4, 4)
        self.layout.addWidget(self.namelab, 1, 4, 3, 4)
        self.layout.addWidget(self.teacherlab, 3, 8, 1, 1)
        self.layout.addWidget(self.teacherlab2, 3, 9, 1, 2)

class Coursewindow(QListWidget):
    def __init__(self, datas,sign):
        super(Coursewindow, self).__init__()
        x = 0
        y = 0
        for data in datas:
            if y==3:
                break
            if x>=sign:
                item = QListWidgetItem(self)
                item.setSizeHint(QSize(800, 150))
                item.setBackground(QColor(240, 240, 240))
                self.setItemWidget(item, CustomWidget(data,y))
                y = y + 1
            x = x + 1

#添加课程界面
class AddCoursse_win(QWidget):
    def __init__(self):
        super(AddCoursse_win, self).__init__()
        self.setWindowTitle("添加课程")
        self.setWindowIcon(QIcon("../datas/logo.ico"))
        self.messagelab = QLabel()  # 用于作为一个提示信息lab
        self.messagelab2 = QLabel()  # 用于作为一个提示信息lab
        self.setextlab = QLabel()
        self.progresslab = QLabel()
        self.newlab = MyLabel()  # 放置视频
        self.newlab.setocr(170, 150, 430, 250, "输入区")
        self.newlab.setxy(75, 300, 175, 370, "关闭")
        self.newlab.setxy(250, 300, 350, 370, "搜索")
        self.newlab.setxy(425, 300, 525, 370, "加入")
        self.qtool = QToolBox()
        self.devise_Ui()

    def devise_Ui(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.horizontalLayout = QHBoxLayout(self)
        self.layout = QGridLayout()
        self.win = QWidget()
        self.win.setLayout(self.layout)  # 设置顶级布局管理器
        self.horizontalLayout.addWidget(self.win)
        self.messagelab.setStyleSheet("QLabel{color:rgb(255,0,0);font-size:20px;font-family:Arial;}")
        self.setextlab.setStyleSheet("QLabel{color:rgb(0,0,255);font-size:16px;font-family:Arial;}")
        self.newlab.setStyleSheet("QLabel{background-color:rgb(240,240, 240)}")
        self.setextlab.setMaximumSize(150, 40)
        self.progresslab.setMaximumSize(40, 40)
        self.messagelab.setMaximumSize(self.width1 / 2, 90)
        self.newlab.setMaximumSize(600, 550)
        self.qtool.setMaximumSize(self.width1 / 2, self.height1 - 100)
        self.qtool.setStyleSheet("QToolBox{background:rgb(150,140,150);font-weight:Bold;color:rgb(0,0,0);}")
        self.layout.addWidget(self.messagelab, 0, 11, 4, 10)
        self.layout.addWidget(self.progresslab, 3, 2, 1, 1)
        self.layout.addWidget(self.setextlab, 3, 3, 1, 4)
        self.layout.addWidget(self.newlab, 4, 0, 10, 10)
        self.layout.addWidget(self.qtool, 4, 11, 10, 10)
        self.messagelab.setText("提示!\n\t" + "操作时,请用手指指在操作命令方框中!")
        self.movie = QMovie("../datas/progress_bar.gif")
        self.setextlab.setText("正在识别操作中．．")
        self.progresslab.setMovie(self.movie)
        self.movie.start()
        self.progresslab.setScaledContents(True)  # 让图片自适应label大小