from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Course_news,Addexfilewin
from ManageInterface.Addexfile_win import Addexfile_win
import glob


class Addexfile(QFrame):
    def __init__(self, data):
        super(Addexfile, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.addexfile = Addexfile_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.addexfile)

        self.data = data
        self.addexfile.returnbut.clicked.connect(self.returnfun)
        self.addexfile.addfile.clicked.connect(self.select_fun1)
        self.addexfile.addmufile.clicked.connect(self.select_fun2)
        self.addexfile.addsystem.clicked.connect(self.select_fun3)


    def returnfun(self):
        dow = Course_news.Course_news(self.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, dow)

    def select_fun1(self):
        QMessageBox.about(self, "提示", '抱歉！！\n该功能暂时未实现!!')


    def select_fun2(self):
        fname = QFileDialog.getExistingDirectory(self, 'open file', '/')
        if fname:
            try:
                files = glob.glob(fname + r'/*')
                pa = files[0]
                self.dow = Addexfilewin.Addexfilewin(self.data, fname)
                self.dow.show()
            except:
                QMessageBox.about(self, "提示", '您选择的文件夹没有任何文件!!')
        else:
            QMessageBox.about(self, "提示", '您没有选择任何文件!!')

    def select_fun3(self):
        QMessageBox.about(self, "提示", '抱歉！！\n该功能暂时未实现!!')