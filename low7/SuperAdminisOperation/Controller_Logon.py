
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
from captcha.image import ImageCaptcha
import random, sqlite3
import SuperAdminisOperation
from ManageInterface import Controller_informent_win
from SuperAdminisInterface import Controller_news_win


class Controller_Logon:
    def __init__(self, win):
        super(Controller_Logon, self).__init__()
        self.logon = win
        self.logon.usrLine.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.logon.usrnameLine.returnPressed.connect(self.enterPress2)
        self.logon.pwdLineEdit1.returnPressed.connect(self.enterPress3)
        self.logon.pwdLineEdit2.returnPressed.connect(self.enterPress4)
        self.logon.returnBtn.clicked.connect(self.returnfun)  # 返回
        self.logon.okBtn.clicked.connect(self.accept)
        self.logon.change_code.linkActivated.connect(self.renovate_code)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("./datas/wen/code.png")
        self.logon.codebel.setPixmap(QPixmap("./datas/wen/code.png"))
        self.logon.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 注册时输入的号码检验是否已经注册过的
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from Controller")
        for variate in c.fetchall():
            if variate[0] == self.logon.usrLine.text():
                return True
        c.close()
        conn.close()
        return False

    def save_data(self):  # 登录时密码在数据库中保存过来
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        a = self.logon.usrLine.text()
        b = self.logon.usrnameLine.text()
        c = self.logon.pwdLineEdit1.text()
        conn.execute("INSERT INTO Controller VALUES(?,?,?)", (a, b, c))
        conn.commit()
        conn.close()

    def enterPress1(self):  # 注册-》用户框回车确定时判断文字框是否有输入
        if len(self.logon.usrLine.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "号码不能为空！")
            self.logon.usrLine.setFocus()
        elif len(self.logon.usrLine.text()) != 11:
            QMessageBox.about(self.logon, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.logon.usrLine.setFocus()
        elif self.checking1():
            QMessageBox.about(self.logon, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.logon.usrLine.setText("")
        else:
            self.logon.usrnameLine.setFocus()

    def enterPress2(self):  # 注册-》用户名框回车确定时判断文字框是否有输入
        if len(self.logon.usrnameLine.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "用户名不能为空！")
            self.logon.usrnameLine.setFocus()
        else:
            self.logon.pwdLineEdit1.setFocus()

    def enterPress3(self):  # 注册-》密码框回车确定时判断文字框是否有输入
        if len(self.logon.pwdLineEdit1.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "密码不能为空！")
            self.logon.pwdLineEdit1.setFocus()
        else:
            self.logon.pwdLineEdit2.setFocus()

    def enterPress4(self):  # 注册-》确认密码框回车确定时判断文字框是否有输入
        if len(self.logon.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "密码不能为空！")
            self.logon.pwdLineEdit2.setFocus()
        elif self.logon.pwdLineEdit1.text() != self.logon.pwdLineEdit2.text():
            QMessageBox.about(self.logon, "提示!", "您输入的密码前后不相同！！")
        else:
            self.logon.codeLineEdit.setFocus()

    def accept(self):  # 注册时将账号密码保存并登录。
        if len(self.logon.usrLine.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "号码不能为空！")
            self.logon.usrLine.setFocus()
        elif len(self.logon.usrLine.text()) != 11:
            QMessageBox.about(self.logon, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.logon.usrLine.setFocus()
        elif self.checking1():
            QMessageBox.about(self.logon, "提示!", "您输入的号码已注册！\n请您换一个号码注册！")
            self.logon.usrLine.setText("")
        elif len(self.logon.usrnameLine.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "用户名不能为空！")
            self.logon.usrnameLine.setFocus()
        elif len(self.logon.pwdLineEdit1.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "密码不能为空！")
            self.logon.pwdLineEdit1.setFocus()
        elif len(self.logon.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self.logon, "提示!", "确认密码不能为空！")
            self.logon.pwdLineEdit2.setFocus()
        elif self.logon.pwdLineEdit1.text() != self.logon.pwdLineEdit2.text():
            QMessageBox.about(self.logon, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.logon.codeLineEdit.text().lower():
            QMessageBox.about(self.logon, "提示!", "验证码输入错误")
            self.renovate_code()
            self.logon.codeLineEdit.setText("")
            self.logon.codeLineEdit.setFocus()
        else:
            self.save_data()
            dow = Controller_informent_win.Controller_informent_win(self.logon.usrLine.text())
            SuperAdminisOperation.win.splitter.widget(0).setParent(None)
            SuperAdminisOperation.win.splitter.insertWidget(0, dow)

    def returnfun(self):  # 连接用户登录界面
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Controller_news_win.Controller_news_win())
