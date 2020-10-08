from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame,QMessageBox
from PyQt5.QtGui import QPixmap
from captcha.image import ImageCaptcha
import random,sqlite3,time
import SuperAdminisOperation
from SuperAdminisOperation import Record,Function,Logon
from SuperAdminisInterface.Forget_win import Forget_win



#忘记密码
class Forget(QFrame):
    def __init__(self):
        super(Forget, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.forget = Forget_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.forget)

        self.forget.okBtn1.clicked.connect(self.accept)
        self.forget.usrLineEdit2.returnPressed.connect(self.enterPress1)  # 用户输入框按回车判断
        self.forget.pwdLineEdit2.returnPressed.connect(self.enterPress2)  # 密码输入框按回车判断
        self.forget.pwdLineEdit3.returnPressed.connect(self.enterPress3)  # 确认密码输入框回车判断
        self.forget.returnBtn.clicked.connect(self.return_record)
        self.forget.change_code.linkActivated.connect(self.renovate_code)
        self.renovate_code()

    def return_record(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Record.Record())

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
        self.forget.codebel.setPixmap(QPixmap("./datas/wen/code.png"))
        self.forget.codebel.setScaledContents(True)  # 让图片自适应label大小

    def checking1(self):  # 忘记密码时检验号码是否没有注册
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
        for variate in c.fetchall():
            if variate[0] == self.forget.usrLineEdit2.text():
                return False
        c.close()
        conn.close()
        return True

    def savedate(self):  # 忘记密码时将新的密码在数据库中修改过来
        sqlpath = './datas/database/Information.db'
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from SuperController")
        for variate in c.fetchall():
            if variate[0] == self.forget.usrLineEdit2.text():
                SuperAdminisOperation.number = variate[0]
                conn.execute("update SuperController set password=(?) where number=(?)",
                             (self.forget.pwdLineEdit2.text(), variate[0],))
                break
        conn.commit()
        c.close()
        conn.close()

    def enterPress1(self):  # 忘记密码时回车确定时判断文字框是否有输入
        if len(self.forget.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.forget.usrLineEdit2.setFocus()
        elif len(self.forget.usrLineEdit2.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.forget.usrLineEdit2.setFocus()
        elif (self.checking1()):
            QMessageBox.about(self, "提示!", "该账号还未注册！\n请先注册！")
            time.sleep(2)
            SuperAdminisOperation.win.splitter.widget(0).setParent(None)
            SuperAdminisOperation.win.splitter.insertWidget(0, Logon.Logon())
        else:
            self.forget.pwdLineEdit2.setFocus()

    def enterPress2(self):  # 忘记密码-》密码框回车确定时判断文字框是否有输入
        if len(self.forget.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.forget.pwdLineEdit2.setFocus()
        else:
            self.forget.pwdLineEdit3.setFocus()

    def enterPress3(self):  # 忘记密码-》确认密码框回车确定时判断文字框是否有输入
        if len(self.forget.pwdLineEdit3.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.forget.pwdLineEdit3.setFocus()
        elif self.forget.pwdLineEdit2.text() != self.forget.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        else:
            self.forget.codeLineEdit1.setFocus()

    def accept(self):  # 忘记密码时验证是否可以登录
        if len(self.forget.usrLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "号码不能为空！")
            self.forget.usrLineEdit2.setFocus()
        elif len(self.forget.usrLineEdit2.text()) != 11:
            QMessageBox.about(self, "提示!", "您输入的号码是错误的！\n请重新输入")
            self.forget.usrLineEdit2.setFocus()
        elif len(self.forget.pwdLineEdit2.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.forget.pwdLineEdit2.setFocus()
        elif len(self.forget.pwdLineEdit3.text()) == 0:
            QMessageBox.about(self, "提示!", "密码不能为空！")
            self.forget.pwdLineEdit3.setFocus()
        elif self.forget.pwdLineEdit2.text() != self.forget.pwdLineEdit3.text():
            QMessageBox.about(self, "提示!", "您输入的密码前后不相同！！")
        elif self.code.lower() != self.forget.codeLineEdit1.text().lower():
            QMessageBox.about(self, "提示!", "验证码输入错误")
            self.renovate_code()
            self.forget.codeLineEdit1.setText("")
            self.forget.codeLineEdit1.setFocus()
        else:
            self.savedate()
            # 连接主窗口界面。
            SuperAdminisOperation.win.splitter.widget(0).setParent(None)
            SuperAdminisOperation.win.splitter.insertWidget(0, Function.Function())


