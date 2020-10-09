from UserInterface import My_Course_win
import sqlite3
from UserOperation.FingerDetection import figer_number
import UserOperation
from UserInterface import Function_win, AddCourse_win, Course_news_win


class My_Course():
    def __init__(self, win):
        super(My_Course, self).__init__()
        self.window = win
        self.sign = 0
        conn = sqlite3.connect('./datas/database/Information.db')
        c = conn.cursor()
        c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                  from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                   where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                    and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                    and Join_Course.number=(?)", (UserOperation.number,))
        self.datas = c.fetchall()
        c.close()
        conn.close()
        self.window1 = My_Course_win.Coursewindow(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, "我的课程")

    # 识别手指指的操作命令
    def finger_camera(self, image):
        fingers = figer_number(image)
        if fingers is not None:
            x = fingers[1] * (450 / 800)
            y = fingers[2] * (450 / 600)
            print(fingers, x, y)
            if fingers[0] == 1:
                if 45 < x < 125 and 60 < y < 130:
                    # 返回
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：返回\n\t操作成功！！")
                    self.clear_cap()
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Function_win.Function_win())
                elif 170 < x < 250 and 60 < y < 130:
                    # 添加课程
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：添加课程\n\t操作成功！！")
                    self.clear_cap()
                    self.add = AddCourse_win.AddCourse_win()
                    # 接受子窗口传回来的信号  然后调用主界面的函数
                    self.add.my_Signal.connect(self.changfun)
                    self.add.show()
                elif 45 < x < 125 and 190 < y < 260:
                    # 上一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：上一页\n\t操作成功！！")
                    self.cut_images()
                elif 170 < x < 250 and 190 < y < 260:
                    # 下一页
                    self.window.timer_next.stop()
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：下一页\n\t操作成功！！")
                    self.add_images()
                elif 45 < x < 125 and 320 < y < 390:
                    # 课程一
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：课程一\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 0][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news_win.Course_news_win(data))
                elif 170 < x < 250 and 320 < y < 390 and (self.sign + 1) < len(self.datas):
                    # 课程二
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：课程二\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 1][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news_win.Course_news_win(data))
                elif 295 < x < 375 and 320 < y < 390 and (self.sign + 2) < len(self.datas):
                    # 课程三
                    self.window.messagelab.setText("提示!\n\t" + "本次操作为：课程三\n\t操作成功！！")
                    self.clear_cap()
                    data = self.datas[self.sign + 2][:3]
                    UserOperation.win.splitter.widget(0).setParent(None)
                    UserOperation.win.splitter.insertWidget(0, Course_news_win.Course_news_win(data))

    # 暂停计时器,关闭视频流
    def clear_cap(self):
        try:
            self.window.timer_next.stop()
            self.window.timer_camera.stop()
            self.window.self_cap.release()  # 释放视频流
        except:
            pass
        self.window.newlab.clear()

    # 上一页课程
    def cut_images(self):
        self.sign = self.sign - 3
        if self.sign < 0:
            self.sign = 0
        self.window.qtool.removeItem(0)
        self.window1 = My_Course_win.Coursewindow(self.datas, self.sign)
        self.window.qtool.addItem(self.window1, '我的课程')
        self.window.timer_next.start(200)

    # 下一页课程
    def add_images(self):
        self.equal = 1
        self.sign = self.sign + 3
        n = len(self.datas)
        if n > self.sign:
            self.window.qtool.removeItem(0)
            self.window1 = My_Course_win.Coursewindow(self.datas, self.sign)
            self.window.qtool.addItem(self.window1, '我的课程')
        else:
            self.sign = self.sign - 3
        self.window.timer_next.start(900)

    # 添加完课程后更新课程列表
    def changfun(self):
        if not self.window.timer_camera.isActive():  # 若定时器未启动
            flag = self.window.self_cap.open(self.window.self_CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if not flag:  # flag表示open()成不成功
                self.window.messagelab.setText("提示!\n\t" + "请检查相机于电脑是否连接正确")
            else:
                self.window.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.window.timer_next.start(200)
                self.equal = 0
                self.window.qtool.removeItem(0)
                conn = sqlite3.connect('./datas/database/Information.db')
                c = conn.cursor()
                c.execute("select Course.Cno,Controller_data.number,Course.name,Controller_data.name,total,filename \
                                         from Course,Course_image,Teacher_Course,Join_Course,Controller_data \
                                          where Course.Cno=Course_image.Cno and Course.Cno=Teacher_Course.Cno \
                                           and Join_Course.Cno=Course.Cno and Teacher_Course.number=Controller_data.number \
                                           and Join_Course.number=(?)", (UserOperation.number,))
                self.datas = c.fetchall()
                c.close()
                conn.close()
                self.window1 = My_Course_win.Coursewindow(self.datas, self.sign)
                self.window.qtool.addItem(self.window1, '我的课程')
