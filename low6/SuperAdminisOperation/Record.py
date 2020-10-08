from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame,QMessageBox
from PyQt5.QtGui import QPixmap
from captcha.image import ImageCaptcha
import random,sqlite3
import SuperAdminisOperation
from SuperAdminisOperation import Logon,Forget,Function
from SuperAdminisInterface.Record_win import Record_win



#登录
class Record(QFrame):
    def __init__(self):
        super(Record, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.record = Record_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.record)

        self.record.okBtn.clicked.connect(self.accept)
        self.record.forgetbtn.linkActivated.connect(self.forgetfun)  # 连接管理员忘记密码界面
        self.record.logonbtn.linkActivated.connect(self.logonfun)  # 连接管理员注册界面
        self.record.usrLineEdit.returnPressed.connect(self.enterPress1)  # 输入结束后按回车键跳到下一个控件
        self.record.pwdLineEdit.returnPressed.connect(self.enterPress2)
        self.record.change_code.linkActivated.connect(self.renovate_code)
        self.renovate_code()

    def renovate_code(self):  # 生成验证码图片
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        self.code = ''
        for num in range(1, 5):
            self.code = self.code + list[random.randint(0, 61)]
        image = ImageCaptcha().generate_image(self.code)
        image.save("./datas/wen/code.png")
        self.record.codebel.setPixmap(QPixmap("./datas/wen/code.png"))
        self.record.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 登录时检验号码是否没有注册
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
        for variate in c.fetchall():
            if variate[0] == self.record.usrLineEdit.text():
                return False
        c.close()
        conn.close()
        return True

    def enterPress1(self):  # 登录回车确定时判断文字框是否有输入
        if len(self.record.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.record.usrLineEdit.setFocus()
        elif len(self.record.usrLineEdit.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.record.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
        else:
            self.record.pwdLineEdit.setFocus()

    def enterPress2(self):  # 登录回车确定时判断文字框是否有输入
        if len(self.record.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.record.pwdLineEdit.setFocus()
        else:
            self.record.codeLineEdit.setFocus()

    def accept(self):  # 登录时判断密码是否正确
        if len(self.record.usrLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.record.usrLineEdit.setFocus()
        elif len(self.record.usrLineEdit.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.record.usrLineEdit.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
        elif len(self.record.pwdLineEdit.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.record.pwdLineEdit.setFocus()
        elif self.code.lower() != self.record.codeLineEdit.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.record.codeLineEdit.setText("")
            self.record.codeLineEdit.setFocus()
        else:
            sqlpath = './datas/database/Information.db'
            conn = sqlite3.connect(sqlpath)
            c = conn.cursor()
            c.execute("select * from SuperController")
            d = 0
            for variate in c.fetchall():
                if variate[0] == self.record.usrLineEdit.text() \
                        and variate[2] == self.record.pwdLineEdit.text():
                    d = 1
                    break
            c.close()
            conn.close()
            if d == 1:  # 连接主界面函数
                SuperAdminisOperation.number = self.record.usrLineEdit.text()
                SuperAdminisOperation.win.splitter.widget(0).setParent(None)
                SuperAdminisOperation.win.splitter.insertWidget(0, Function.Function())
            else:
                QMessageBox.about(self, "提示!", "账号或密码输入错误")

    def forgetfun(self):  # 连接超级管理员忘记密码界面
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        Forget.Forget().renovate_code()
        SuperAdminisOperation.win.splitter.insertWidget(0, Forget.Forget())

    def logonfun(self):  # 连接超级管理员注册界面
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        Logon.Logon().renovate_code()
        SuperAdminisOperation.win.splitter.insertWidget(0, Logon.Logon())