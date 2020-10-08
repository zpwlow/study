
#-------------------------------------------
# 从视频序列中分割手部区域
#-------------------------------------------

# 导入库
from PyQt5.QtWidgets import QWidget,QLabel,QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer,pyqtSignal
import cv2
import numpy as np
from sklearn.metrics import pairwise
import time
import UserOperation
from UserOperation import self_cap,self_CAM_NUM

# 全局变量
cap_region_x_begin=0.5  # 起点/总宽度
cap_region_y_end=0.8  # 终点/总宽度
bgSubThreshold = 50
threshold = 25
blurValue = 7
learningRate = 0

top, right, bottom, left = 0, 0, 600, 800

total_rectangle = 9
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

# 变量
triggerSwitch = False  # 如果为真，keyborad模拟器可以工作

#---------------------------------------------
# 获取手指肤色
#---------------------------------------------
def draw_rect(frame):
    rows, cols, _ = frame.shape
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y
    hand_rect_one_x = np.array(
        [6 * rows / 20, 6 * rows / 20, 6 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 12 * rows / 20,
         12 * rows / 20, 12 * rows / 20], dtype=np.uint32)

    hand_rect_one_y = np.array(
        [9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20,
         10 * cols / 20, 11 * cols / 20], dtype=np.uint32)

    hand_rect_two_x = hand_rect_one_x + 10
    hand_rect_two_y = hand_rect_one_y + 10

    for i in range(total_rectangle):
        cv2.rectangle(frame, (hand_rect_one_y[i], hand_rect_one_x[i]),
                      (hand_rect_two_y[i], hand_rect_two_x[i]),
                      (0, 255, 0), 1)

    return frame


#---
#创建肤色 ROI 直方图
#-----

def hand_histogram(frame):
    global hand_rect_one_x, hand_rect_one_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
                                          hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hists = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hists, hand_hists, 0, 255, cv2.NORM_MINMAX)

#进行肤色检测
def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)

    # thresh = cv2.dilate(thresh, None, iterations=5)

    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)

#---------------------------------------------
# 分割图像中的手部区域
#---------------------------------------------
def segment(frame):
    fgmask = UserOperation.bgModel.apply(frame, learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

# --------------------------------------------------------------
# 计算分段手区域中的手指数
# --------------------------------------------------------------
def count(thresholded, segmented):
    # 求分段手部区域的凸壳
    chull = cv2.convexHull(segmented)

    # 求凸壳中的最极值点
    extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])
    xy = [extreme_top[0], extreme_top[1]] # 顶点坐标

    # 找到掌心
    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)

    # 求手掌中心与凸包最端点之间的最大欧氏距离
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right,
                                                           extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]

    # 用得到的最大欧氏距离的80%计算圆的半径
    radius = int(0.8 * maximum_distance)

    # 求圆的周长
    circumference = (2 * np.pi * radius)

    # 取出有手掌和手指的圆形感兴趣区域
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")

    # 绘制圆形ROI
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

    # 使用圆形ROI作为掩模，在阈值手图像上使用掩模获得切割，并在阈值手之间进行位操作
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    # 计算圆形ROI中的轮廓
    (_, cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # 初始化手指计数
    count = 0

    # 在找到的轮廓中循环
    for c in cnts:
        # 计算轮廓的边界框
        (x, y, w, h) = cv2.boundingRect(c)

        # 仅当-
        # 1. 轮廓区域不是腕部（底部区域）
        # 2. 沿轮廓的点数不超过圆形ROI周长的25%
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count,xy

#给出图像计算手指数和指尖坐标.
def figer_number(frame):
    if UserOperation.self_sign == 1:
        frame = cv2.resize(frame, (800, 600))  # 把读到的帧的大小重新设置为 600x500
        #frame = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        # 翻转框架，使其不是镜像视图
        cv2.flip(frame, -1, frame)  #翻转镜像--->对角翻转.
        # 获得 ROI
        roi = frame[top:bottom, right:left]
        # 分割手部区域
        hand = segment(roi)
        # 检查手部区域是否被分割
        if hand is not None:
            hist_mask_image = hist_masking(hand, UserOperation.hand_hist)  # 背景减除后的图像进行肤色检测
            # 如果是，则解压缩阈值图像和分割区域
            gray = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            thresholded = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)[1]
            (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 如果未检测到轮廓，则返回“无”
            if len(cnts) == 0:
                return None
            else:
                # 根据轮廓面积，求出手的最大轮廓
                segmented = max(cnts, key=cv2.contourArea)
                # 数数手指的数目
                fingers, xy = count(thresholded, segmented)
                data = [fingers,xy[0],xy[1]]
                return data
    else:
        return None



class Finger_win(QWidget):
    def __init__(self):
        super(Finger_win, self).__init__()
        self.setWindowTitle("low_User")
        self.setWindowIcon(QIcon("./datas/logo.ico"))
        self.label = QLabel(self)
        self.resize(800, 600)
        self.label.resize(800,600)
        self.desktop = QApplication.desktop()  # 获取屏幕分辨率
        self.screenRect = self.desktop.screenGeometry()
        # 窗口移动至中心
        self.move((self.screenRect.width() - 800) / 2, (self.screenRect.height() - 600) / 2)
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        # 设置感兴趣区域（ROI）坐标
        self.top, self.right, self.bottom, self.left = 0, 0, 600, 800

        # 计算时间
        self.time_start = time.time()
        self.n = 5
        self.a = 6
        self.i = 5
        self.timer_camera.timeout.connect(self.show_camera)
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self_cap.open(self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                pass
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示

    def show_camera(self):
        # 获取当前帧
        (grabbed, frame) = self_cap.read()  # 从视频流中读取
        frame = cv2.resize(frame, (800, 600))  # 把读到的帧的大小重新设置为 600x500

        # 翻转框架，使其不是镜像视图
        frame = cv2.flip(frame, 1)

        # 克隆帧
        clone = frame.copy()

        # 获得 ROI
        roi = frame[self.top:self.bottom, self.right:self.left]

        time_end = time.time()
        if (time_end - self.time_start) < 5:
            cv2.putText(clone, "Please put your fingers in the green box!",
                        (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            clone = draw_rect(clone)

        if (time_end - self.time_start) >=5 and (time_end - self.time_start) < 9:
            if (time_end - self.time_start) > self.i:
                self.i = self.i + 1
                self.n = self.n - 1
            cv2.putText(clone, "Skin color detection after " + str(self.n) + " seconds",
                        (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            clone = draw_rect(clone)

        # 获取肤色
        if self.n == 1:
            print(12)
            UserOperation.hand_hist = hand_histogram(frame)
            print(UserOperation.hand_hist)
            self.n = 5

        if (time_end - self.time_start) >= 9 and (time_end - self.time_start) < 14:
            if (time_end - self.time_start) > self.i:
                self.i = self.i + 1
                self.a = self.a - 1
            cv2.putText(clone, "Get the background in " + str(self.a) + " seconds",
                        (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if (time_end - self.time_start) >= 14:
            UserOperation.bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            UserOperation.self_sign = 1
            #figer_number(frame)
            self.timer_camera.stop()
            self.close()

        clone = cv2.cvtColor(clone, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QImage(clone.data, clone.shape[1], clone.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()




'''
#主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Finger_win()
    win.show()
    sys.exit(app.exec_())
'''


