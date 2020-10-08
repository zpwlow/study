import sqlite3
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserInterface import Function_win, User_amend_win


class User_Myself():
    def __init__(self, win):
        super(User_Myself, self).__init__()
        self.window = win
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_date where number=(?)", (UserOperation.number,))
        self.data = c.fetchall()[0]
        c.close()
        conn.close()

    # 识别手指指的操作命令
    def finger_camera(self, image):
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
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：修改密码\n\t操作成功")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, User_amend_win.User_amend_win())

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()
