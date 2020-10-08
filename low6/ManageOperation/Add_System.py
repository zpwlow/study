from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
import ManageOperation
from ManageOperation import Select_location,Addcufile,Max_widget
from ManageInterface.Add_System_win import Add_System_win,AddsystemQlist



class Add_System(QFrame):
    def __init__(self,data):
        super(Add_System, self).__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.add = Add_System_win()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.add)

        self.data = data
        self.location = Select_location.Select_location(self)
        self.returnbut.clicked.connect(self.returnfun)
        self.doubleselect.clicked.connect(self.doublefun)
        self.location.show()

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0,Addcufile.Addcufile(self.data))

    def surefun(self):
        self.qtool.removeItem(0)
        greade  = self.location.getgrade()
        course  = self.location.getcourse()
        self.window = AddsystemQlist(self, self.data,greade,course)
        self.qtool.addItem(self.window, "系统文件")

    def doublefun(self):
        self.location.fun2()
        self.location.show()

    def clicked(self):
        self.max = Max_widget.Max_widget()
        self.max.show()