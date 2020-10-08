from UserOperation.FingerDetection import figer_number
import UserOperation
from UserInterface import Function_win


class User_report:
    def __init__(self, win):
        super(User_report, self).__init__()
        self.window = win

    # 识别手指指的操作命令
    def finger_camera(self, image):
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 150 < x < 250 and 200 < y < 270:
                    # 返回
                    try:
                        self.window.timer_next.stop()
                        self.window.timer_camera.stop()
                        self.window.self_cap.release()  # 释放视频流
                        self.window.report.newlab.clear()
                    except:
                        pass
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())
