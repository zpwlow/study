from PyQt5.QtWidgets import QHBoxLayout,QFileDialog,QApplication
from PyQt5.QtWidgets import QFrame,QMessageBox
from PyQt5.QtGui import QPixmap
import time
import SuperAdminisOperation
from SuperAdminisOperation import Function
from SuperAdminisInterface.Reptile_win import Reptile_win,RepliteJob,Select_Reptile



class Reptile(QFrame):
    def __init__(self):
        super(Reptile, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.reptile =  Reptile_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.reptile)

        self.job = RepliteJob(self)
        self.dow = Select_Reptile(self)
        self.reptile.Reptile_child1but1.clicked.connect(self.return_fun)
        self.reptile.Reptile_child1but2.clicked.connect(self.select_fun1)
        self.reptile.Reptile_child1but3.clicked.connect(self.select_fun2)
        self.reptile.Reptile_child1but4.clicked.connect(self.select_fun3)
        self.dow.show()

    def return_fun(self):
        SuperAdminisOperation.win.splitter.widget(0).setParent(None)
        SuperAdminisOperation.win.splitter.insertWidget(0, Function.Function())

    def select_fun3(self):
        self.window1tree.clear()
        self.dow.fun2()
        self.dow.show()

    def clicked1(self):
        self.reptile.Reptile_child1but1.setEnabled(True)
        self.reptile.Reptile_child1but2.setEnabled(True)
        self.reptile.Reptile_child1but4.setEnabled(True)

    def clicked2(self):
        self.reptile.Reptile_child1but1.setEnabled(True)
        self.reptile.Reptile_child1but4.setEnabled(True)

    def select_fun2(self):
        self.job.stop()
        QMessageBox.about(self, "提示", '暂停成功!!')
        self.reptile.Reptile_child1but3.setEnabled(False)
        time.sleep(2)


    def select_fun1(self):
        self.reptile.Reptile_child1but2.setEnabled(False)
        self.reptile.Reptile_child1but3.setEnabled(True)
        type = self.dow.gettype()
        greade = self.dow.getgrade()
        course = self.dow.getcourse()
        rely = QMessageBox.question(self, "提示!", "爬取过程需要时间比较久\n请问是否继续？", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
        if rely == 65536:
            return
        self.window1tree.setPlainText("爬取课件数据开始\n爬取过程需要时间比较久，请您耐心等待!!\n\n")
        self.job.setdata(type,greade,course)
        self.job.updated.connect(self.settext)
        self.job.start()

    def settext(self,text):
        self.window1tree.append(text)
        QApplication.processEvents()