from PyQt5.QtWidgets import  QMessageBox, QFileDialog
import ManageOperation
from ManageInterface import Addexfilewin_win, Course_news_win
import glob


class Addexfile:
    def __init__(self, win):
        super(Addexfile, self).__init__()
        self.window = win

    def returnfun(self):
        dow = Course_news_win.Course_news_win(self.window.data)
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, dow)

    def select_fun1(self):
        QMessageBox.about(self.window, "提示", '抱歉！！\n该功能暂时未实现!!')

    def select_fun2(self):
        fname = QFileDialog.getExistingDirectory(self.window, 'open file', '/')
        if fname:
            try:
                files = glob.glob(fname + r'/*')
                pa = files[0]
                self.dow = Addexfilewin_win.Addexfilewin_win(self.window.data, fname)
                self.dow.show()
            except:
                QMessageBox.about(self.window, "提示", '您选择的文件夹没有任何文件!!')
        else:
            QMessageBox.about(self.window, "提示", '您没有选择任何文件!!')

    def select_fun3(self):
        QMessageBox.about(self.window, "提示", '抱歉！！\n该功能暂时未实现!!')
