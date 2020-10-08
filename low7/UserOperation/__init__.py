import sys, os
import cv2

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

self_cap = cv2.VideoCapture()  # 视频流
self_CAM_NUM = 1  # 为0时表示视频流来自笔记本内置摄像头,为１时表示外置摄像头
bgModel = None
hand_hist = None
self_sign = 0
number = 15812904182
win = None
