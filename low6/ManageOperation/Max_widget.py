from PyQt5.QtWidgets import QHBoxLayout,QWidget,QMessageBox,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import glob
from PIL import Image
from ManageInterface.Max_widget_win import Max_widget_win



#管理员播放课件　
class Max_widget(QWidget):
    def __init__(self):
        super(Max_widget, self).__init__()
        self.pa = './datas/tupian'
        self.fileNames = glob.glob(self.pa + r'/*')
        self.a = 1
        self.max = Max_widget_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.max)
        self.screenRect = self.desktop.screenGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.resize(self.width1, self.height1)
        pa1 = self.fileNames[self.a - 1]
        pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
        img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
        out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
        out.save(pa2, 'jpeg')
        pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.max.lab2.setPixmap(pixmap)  # 在label上显示图片

    def mousePressEvent(self, event):  # 重写鼠标点击的事件
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        self.y = self.screenRect.height()
        self.x = self.screenRect.width()
        if (event.button() == Qt.LeftButton) and (event.pos().x() < self.x / 2):
            self.cut_images()
        if (event.button() == Qt.LeftButton) and (event.pos().x() > self.x / 2):
            self.add_images()

    def add_images(self):  # 下一页ppt
        self.a = self.a + 1
        try:
            pa1 = self.fileNames[self.a-1]
            pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
            img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
            out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
            out.save(pa2, 'jpeg')
            pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.max.lab2.setPixmap(pixmap)
        except:
            self.a = self.a - 1
            QMessageBox.about(self, "提示!", "这是最后一页")


    def cut_images(self):  # 上一页ppt
        self.a = self.a - 1
        pa1 = self.fileNames[self.a-1]
        pa2 = self.pa + "/image" + str(self.a) + ".jpeg"
        if self.a == 0:
            self.a = self.a + 1
            QMessageBox.about(self, "提示!", "这是第一页")
        else:
            img = Image.open(pa1)  # 将图片改变分辨率为self.lab窗口大小
            out = img.resize((self.width1, self.height1), Image.ANTIALIAS)
            out.save(pa2, 'jpeg')
            pixmap = QPixmap(pa2)  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
            self.max.lab2.setPixmap(pixmap)