from UserOperation.FingerDetection import figer_number
import UserOperation
from UserOperation.User_report import User_report
from UserOperation import Record,My_Course,Question,User_report,User_Myself

class Function():
    def __init__(self,win):
        super(Function, self).__init__()
        self.window = win


    # 识别手指指的操作命令
    def finger_camera(self,image):
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (600 / 800)
            y = fingers[2] * (550 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if x > 75 and x < 175 and y > 150 and y < 220:
                    # 查看课程
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：查看课程\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, My_Course.My_Course())
                elif x > 250 and x < 350 and y > 150 and y < 220:
                    #问问题
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：问问题\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Question.Question())
                elif x > 425 and x < 525 and y > 150 and y < 220:
                    # 学习记录
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：学习记录\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_report())
                elif x > 75 and x < 175 and y > 330 and y < 400:
                    # 我的
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：我的\n\t操作成功！！")
                    try:
                        self.window.timer_next.stop()
                        self.window.timer_camera.stop()
                        self.window.self_cap.release()  # 释放视频流
                    except:
                        pass
                    self.window.newlab.clear()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_Myself.User_Myself())

                elif x > 250 and x < 350 and y > 330 and y < 400:
                    # 退出登录
                    self.window.messagelab.setText("提示!\n\t" +
                                                     "本次操作为：退出登录\n\t操作成功！！")
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Record.Record())
                elif x > 425 and x < 525 and y > 330 and y < 400:
                    # 退出程序
                    pass

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()
