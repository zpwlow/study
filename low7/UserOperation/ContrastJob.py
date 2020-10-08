from PyQt5 import QtCore
import tr


class ContrastJob(QtCore.QThread):
    updated = QtCore.pyqtSignal()

    def __init__(self, path):
        super(ContrastJob, self).__init__()
        self.path = path
        self.answer = ''

    def run(self):
        try:
            self.answer = tr.recognize(self.path)
            print(self.answer)
            self.updated.emit()
        except:
            pass

    def getanswer(self):
        return self.answer
