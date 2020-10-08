#------------------------------------------------------------
# 从视频序列中分割、识别和计数手指
#------------------------------------------------------------

# 导入库
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise

# 全局变量
bg = None

#--------------------------------------------------
# 在后台查找背景图的平均值
#--------------------------------------------------
def run_avg(image, accumWeight):
    global bg
    # 初始化背景
    if bg is None:
        bg = image.copy().astype("float")
        return

    # 计算加权平均数，累加并更新背景
    cv2.accumulateWeighted(image, bg, accumWeight)

#---------------------------------------------
# 分割图像中的手部区域
#---------------------------------------------
def segment(image, threshold=25):
    global bg
    # 找出背景和当前帧之间的绝对差异
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # 对　diff　图像设置阈值，以便我们得到前景
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # 获取阈值图像中的轮廓
    (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 如果未检测到轮廓，则返回“无”
    if len(cnts) == 0:
        return
    else:
        # 根据轮廓面积，求出手的最大轮廓
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

#--------------------------------------------------------------
# 计算分段手区域中的手指数
#--------------------------------------------------------------
def count(thresholded, segmented):
    # 求分段手部区域的凸壳
    chull = cv2.convexHull(segmented)

    # 求凸壳中的最极值点
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])
    print(extreme_top[0],extreme_top[1]) #顶点坐标

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
# MAIN FUNCTION
#-----------------
if __name__ == "__main__":
    # 初始化平均运行重量
    accumWeight = 0.5

    # 获取网络摄像头的参考
    camera = cv2.VideoCapture(0)

    # 设置感兴趣区域（ROI）坐标
    #top, right, bottom, left = 10, 350, 225, 590
    top, right, bottom, left = 0, 0, 480, 640

    # 初始化帧数
    num_frames = 0

    # 校准指示器q
    calibrated = False

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

        # 将roi转换为灰度并使其模糊
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # 为了得到背景，继续寻找直到达到阈值，这样我们的加权平均模型就得到了校准
        if num_frames < 30:
            run_avg(gray, accumWeight)
            if num_frames == 1:
                print("[STATUS] please wait! calibrating...")
            elif num_frames == 29:
                print("[STATUS] calibration successfull...")
        else:
            # 分割手部区域
            hand = segment(gray)

            # 检查手部区域是否被分割
            if hand is not None:
                # 如果是，则解压缩阈值图像和分割区域
                (thresholded, segmented) = hand

                # 绘制分割区域并显示框架
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))


                # 数数手指的数目
                fingers = count(thresholded, segmented)

                cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                # 显示阈值图像
                cv2.imshow("Thesholded2", thresholded)

        # 画分段的手
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # 增加帧数
        num_frames += 1

        # 用分段的手显示框架
        cv2.imshow("Video Feed", clone)

        # 观察用户的按键
        keypress = cv2.waitKey(1) & 0xFF

        # 如果用户按下“q”，则停止循环
        if keypress == ord("q"):
            break

# 释放内存
camera.release()
cv2.destroyAllWindows()