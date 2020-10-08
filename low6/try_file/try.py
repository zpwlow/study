#-------------------------------------------
# 从视频序列中分割手部区域
#-------------------------------------------

# 导入库
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import copy
import math

# 全局变量
bg = None
cap_region_x_begin=0.5  # 起点/总宽度
cap_region_y_end=0.8  # 终点/总宽度
bgSubThreshold = 50
threshold = 25
blurValue = 7
learningRate = 0
sign = 1

hand_hist = None
total_rectangle = 9
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

# 变量
isBgCaptured = 0   # 布尔，背景是否被捕获
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

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)


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
    fgmask = bgModel.apply(frame, learningRate=learningRate)
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
    print(extreme_top[0], extreme_top[1])  # 顶点坐标

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

    return count

#-----------------
# 主函数
#-----------------
if __name__ == "__main__":
    # 初始化平均运行重量
    aWeight = 0.5

    # 获取网络摄像头的参考
    camera = cv2.VideoCapture(0)

    # 设置感兴趣区域（ROI）坐标
    top, right, bottom, left = 0, 0, 520, 695

    # 初始化帧数
    num_frames = 0

    # 继续循环，直到中断
    while(True):
        # 获取当前帧
        (grabbed, frame) = camera.read()

        # 调整框架大小
        frame = imutils.resize(frame, width=700)

        # 翻转框架，使其不是镜像视图
        frame = cv2.flip(frame, 1)

        # 克隆帧
        clone = frame.copy()

        # 获取框架的高度和宽度
        (height, width) = frame.shape[:2]

        # 获得 ROI
        roi = frame[top:bottom, right:left]

        # 为了得到背景，继续寻找直到达到阈值，这样我们的加权平均模型就得到了校准
        if isBgCaptured == 1:
            # 分割手部区域
            hand = segment(roi)
            # 检查手部区域是否被分割
            if hand is not None:
                cv2.imshow("hand", hand)
                hist_mask_image = hist_masking(hand, hand_hist)
                cv2.imshow("hist_mask_image", hist_mask_image)
                # 如果是，则解压缩阈值图像和分割区域
                gray = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
                thresholded = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)[1]
                (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # 如果未检测到轮廓，则返回“无”
                if len(cnts) == 0:
                    pass
                else:
                    # 根据轮廓面积，求出手的最大轮廓
                    segmented = max(cnts, key=cv2.contourArea)
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                    cv2.imshow("Thesholded", thresholded)
                    # 数数手指的数目
                    fingers = count(thresholded, segmented)
                    cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



        # 画分段的手
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        #获取肤色
        if sign == 1:
            clone = draw_rect(clone)

        # 用分段的手显示框架
        cv2.imshow("Video Feed", clone)

        # 观察用户的按键
        keypress = cv2.waitKey(1) & 0xFF

        # 如果用户按下“q”，则停止循环
        if keypress == ord("q"):
            break
        elif keypress == ord('b'):  # 按“b”捕捉背景
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            isBgCaptured = 1
            print('!!!Background Captured!!!')
        elif keypress & 0xFF == ord('z'):
            sign = 0
            hand_hist = hand_histogram(frame)
            print(hand_hist)
        elif keypress  == ord('r'):  # 按“r”重置背景
            bgModel = None
            triggerSwitch = False
            isBgCaptured = 0
            print('!!!Reset BackGround!!!')


# 释放内存
camera.release()
cv2.destroyAllWindows()