import ManageOperation
from ManageInterface import Addcufile_win, Max_widget_win, Selsect_location_win
from ManageInterface.Add_System_win import AddsystemQlist


class Add_System:
    def __init__(self, win):
        super(Add_System, self).__init__()
        self.window = win
        self.location = Selsect_location_win.Select_location_win(self)

    def returnfun(self):
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Addcufile_win.Addcufile_win(self.window.data))

    def surefun(self):
        self.window.qtool.removeItem(0)
        greade = self.location.getgrade()
        course = self.location.getcourse()
        self.window = AddsystemQlist(self, self.window.data, greade, course)
        self.window.qtool.addItem(self.window, "系统文件")

    def doublefun(self):
        self.location.fun2()
        self.location.show()

    def clicked(self):
        self.max = Max_widget_win.Max_widget_win()
        self.max.show()
