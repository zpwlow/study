from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen


class MyLabel(QLabel):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    def __init__(self):
        super().__init__()
        self.lab1 = QLabel(self)
        self.data = []

    # 绘制 手指点击的区域
    def setxy(self, x1, y1, x2, y2, text):
        self.lab1 = QLabel(self)
        self.lab1.setText(text)
        self.lab1.setStyleSheet("QLabel{color:rgb(255,0,0);\
                                 font-size:18px;font-family:Arial;background:transparent;}")
        self.lab1.move(x1, y1)
        data = [x1, y1, x2, y2, self.lab1]
        self.data.append(data)

    # 绘制 ocr 图像输入区
    def setocr(self, x1, y1, x2, y2, text):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lab1.setText(text)
        self.lab1.setStyleSheet("QLabel{color:rgb(0,0,255);\
                                 font-size:18px;font-family:Arial;background:transparent;}")
        self.lab1.move(x1, y1)

    # 绘制矩形区域
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        rect = QRect(self.x1, self.y1, abs(self.x2 - self.x1), abs(self.y2 - self.y1))
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)
        for data in self.data:
            rect = QRect(data[0], data[1], abs(data[2] - data[0]), abs(data[3] - data[1]))
            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
            painter.drawRect(rect)
        painter.end()
