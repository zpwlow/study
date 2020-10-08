import cv2
import time
from PyQt5.QtGui import QPixmap
import UserOperation
from UserInterface import Function_win
from UserOperation import AnswerJob
from UserOperation.FingerDetection import figer_number


class Question():
    def __init__(self, win):
        super(Question, self).__init__()
        self.window = win

    # 识别手指指的操作命令
    def finger_camera(self, image, face):
        self.face = face
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 125 < x < 225 and 300 < y < 370:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())
                elif 375 < x < 475 and 300 < y < 370:
                    # 查看答案
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：查看答案\n\t操作成功")
                    self.contrast_answer()

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()

    def contrast_answer(self):
        self.window.timer_next.stop()
        imgpath = "./datas/wen/test1.jpg"
        self.window.setextlab.setText("正在识别输入中．．")
        self.window.progresslab.setMovie(self.window.movie)
        self.window.movie.start()
        time.sleep(1)
        cv2.imwrite(imgpath, self.face)
        self.answerjob = AnswerJob.AnswerJob(imgpath)
        self.answerjob.updated.connect(self.right_answer)
        self.answerjob.start()

    def right_answer(self):
        self.window.movie.stop()
        self.window.progresslab.clear()
        self.window.progresslab.setPixmap(QPixmap("./datas/movie.jpg"))
        self.window.progresslab.setScaledContents(True)  # 让图片自适应label大小
        self.window.setextlab.clear()
        answers = self.answerjob.getanswer()
        data = ''
        x = 0
        for answer in answers:
            if x == 0:
                data = answer
            else:
                data = data + '\n=' + answer
            x = 1
        self.window.answerlab.setText(data)
        self.window.timer_next.start(200)
