#-------------------------------------------
# 从视频序列中分割手部区域
#-------------------------------------------

# 导入库
import cv2
import imutils
import numpy as np

# 全局变量
bg = None

#--------------------------------------------------
# 在后台查找背景图的平均值
#--------------------------------------------------
def run_avg(image, aWeight):
    global bg
    # 初始化背景
    if bg is None:
        bg = image.copy().astype("float")

        return

    # 计算加权平均数，累加并更新背景
    cv2.accumulateWeighted(image, bg, aWeight)


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

#-----------------
# 主函数
#-----------------
if __name__ == "__main__":
    # 初始化平均运行重量
    aWeight = 0.5

    # 获取网络摄像头的参考
    camera = cv2.VideoCapture(0)

    # 设置感兴趣区域（ROI）坐标
    top, right, bottom, left = 10, 350, 225, 590

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

        # 将roi转换为灰度并使其模糊
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)


        # 为了得到背景，继续寻找直到达到阈值，这样我们的加权平均模型就得到了校准
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # 分割手部区域
            hand = segment(gray)

            # 检查手部区域是否被分割
            if hand is not None:
                # 如果是，则解压缩阈值图像和分割区域
                (thresholded, segmented) = hand

                #绘制分割区域并显示框架
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

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