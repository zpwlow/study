from PyQt5.QtGui import QImage,QPixmap
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.data = []

    def setxy(self,x1,y1,x2,y2,text):

        self.lab1 = QLabel(self)
        self.lab1.setText(text)
        self.lab1.setStyleSheet("QLabel{color:rgb(0,0,255);\
                                 font-size:18px;font-family:Arial;background:transparent;}")
        self.lab1.move(x1,y1)
        self.setGeometry(QRect(x1,y1,x2,y2))
        data = [x1,y1,x2,y2]
        self.data.append(data)

    #绘制表格
    def paintEvent(self,event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        for data in self.data:
            rect = QRect(data[0], data[1], abs(data[2] - data[0]), abs(data[3] - data[1]))
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)
        painter.end()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(675, 500)
        self.move(100,50)
        self.setWindowTitle('在label中绘制矩形')
        self.lb = MyLabel() #重定义的label
        self.lb.setxy(150, 120, 250, 220, "输入区")
        #self.lb.setGeometry(QRect(150, 120, 250, 220))
        self.lb.setxy(300, 150, 400, 350, "绘图")
        #self.lb.setGeometry(QRect(300, 150, 400, 350))
        img = cv2.imread('a5.jpg')
        showImage = QImage(img.data, img.shape[1], img.shape[0],
                     QImage.Format_RGB888)  # 把读取到的图片数据变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.lb.setPixmap(QPixmap.fromImage(showImage))
        #self.lb.setCursor(Qt.CrossCursor)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.lb)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())