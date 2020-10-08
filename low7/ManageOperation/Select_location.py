from PyQt5.QtWidgets import QMessageBox


class Select_location:
    def __init__(self, win):
        super(Select_location, self).__init__()
        self.select = win
        self.select.typebox.currentIndexChanged.connect(self.fun1)
        self.select.sure.clicked.connect(self.surefun)

    def fun1(self):
        self.select.greadebox.clear()
        self.select.coursebox.clear()
        if self.select.typebox.currentText() == "小学":
            self.select.greadebox.addItems(['', '一年级上册', '一年级下册', '二年级上册', '二年级下册', '三年级上册', '三年级下册',
                                            '四年级上册', '四年级下册', '五年级上册', '五年级下册', '六年级上册', '六年级下册'])
            self.select.coursebox.addItems(['', '语文', '数学', '英语'])
        elif self.select.typebox.currentText() == "初中":
            self.select.greadebox.addItems(['', '初一上册', '初一下册', '初二上册', '初二下册', '初三上册', '初三下册', ])
            self.select.coursebox.addItems(['', '语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理'])
        elif self.select.typebox.currentText() == "高中":
            self.select.greadebox.addItems(['', '必修一', '必修二', '必修三', '必修四', '必修五',
                                            '选修一', '选修二', '选修三', '选修四', '选修五'])
            self.select.coursebox.addItems(['', '语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理'])

    def fun2(self):
        self.select.greadebox.clear()
        self.select.coursebox.clear()
        self.select.typebox.clear()
        self.select.typebox.addItems(['', '小学', '初中', '高中'])

    def surefun(self):
        if (self.select.greadebox.currentText() == ""):
            QMessageBox.about(self.select, "提示", '年级的选项框不能为空!!')
            return
        elif (self.select.typebox.currentText() == ""):
            QMessageBox.about(self.select, "提示", '学习阶段的选项框不能为空!!')
            return
        elif (self.select.coursebox.currentText() == ""):
            QMessageBox.about(self.select, "提示", '科目的选项框不能为空!!')
            return
        elif (self.select.greadebox.currentText()[:3] != "一年级"):
            QMessageBox.about(self.select, "抱歉", '目前只能添加小学一年级的课件!!')
            return
        else:
            self.select.close()
            self.select.dow.surefun()

    def gettype(self):
        return self.select.typebox.currentText()

    def getgrade(self):
        return self.select.greadebox.currentText()

    def getcourse(self):
        return self.select.coursebox.currentText()
