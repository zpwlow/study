from PyQt5.QtWidgets import QHBoxLayout,QLabel,QHeaderView,QAbstractItemView
from PyQt5.QtWidgets import QFrame,QTableWidgetItem
import ManageOperation
from ManageInterface import Statistics_class_win
from ManageOperation import Statistics_class
from ManageInterface.User_report_win import User_report_win
import datetime,sqlite3


class User_report:
    def __init__(self, win):
        super(User_report, self).__init__()
        self.report = win
        self.report.returnBtn.clicked.connect(self.return_fun)
        self.information()

    def information(self):
        new = datetime.datetime.now()
        abcd = '%Y-%m-%d %H:%M:%S'
        a1 = datetime.datetime.strptime(self.report.da1[2], abcd)
        a = (new - a1).days + 1
        self.day1 = QLabel(str(a) + "天")
        ab = self.report.da1[3]
        if (ab / 3600) > 1:
            ac = str(int(ab / 3600)) + '时' + str(round((ab / 3600 - int(ab / 3600)) * 60, 2)) + "分"
        else:
            ac = str(round(ab / 60, 2)) + "分"
        self.learntime1 = QLabel(ac)
        ad = ab / a
        if (ad / 3600) > 1:
            ae = str(int(ad / 3600)) + '时' + str(round((ad / 3600 - int(ad / 3600)) * 60, 2)) + "分"
        else:
            ae = str(round(ad / 60, 2)) + "分"
        self.avglearn1 = QLabel(ae)
        self.day1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.learntime1.setStyleSheet(
            "QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.avglearn1.setStyleSheet("QLabel{color:rgb(0,255,0);font-size:20px;font-weight:Bold;font-family:'宋体';}")
        self.report.table.setStyleSheet("QTableWidget{background-color:rgb(255,255,255);font:13pt '宋体';font-weight:Bold;};");
        self.report.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        sqlpath = "./datas/database/SQ" + self.report.da1[0] + "L.db"
        conn = sqlite3.connect(sqlpath)
        c = conn.cursor()
        c.execute("select * from User_data where Cno=(?)",(self.report.da2,))
        data = c.fetchall()
        b = len(data)
        self.report.table.setRowCount(b)
        self.report.table.setColumnCount(5)
        self.report.table.setHorizontalHeaderLabels(['开始学习时间', '文件类型', '文件名', '结束时间', '学习时长'])
        i = 0
        for variate in data:
            self.report.table.setItem(i, 0, QTableWidgetItem(variate[0]))
            self.report.table.setItem(i, 1, QTableWidgetItem(variate[2]))
            self.report.table.setItem(i, 2, QTableWidgetItem(variate[3]))
            self.report.table.setItem(i, 3, QTableWidgetItem(variate[4]))
            min = (datetime.datetime.strptime(variate[4], abcd) - datetime.datetime.strptime(variate[0], abcd)).seconds
            if (min / 3600) > 1:
                ac = str(int(min / 3600)) + '时' + str(round((min / 3600 - int(min / 3600)) * 60, 2)) + "分"
            else:
                ac = str(round(min / 60, 2)) + "分"
            self.report.table.setItem(i, 4, QTableWidgetItem(ac))
            i += 1
        self.day1.setMaximumSize(150, 40)
        self.learntime1.setMaximumSize(150, 40)
        self.avglearn1.setMaximumSize(150, 40)
        self.layout.addWidget(self.day1, 0, 4, 1, 1)
        self.layout.addWidget(self.learntime1, 0, 7, 1, 1)
        self.layout.addWidget(self.avglearn1, 0, 10, 1, 1)
        self.layout.addWidget(self.report.table, 3, 0, 1, 12)

    def return_fun(self):
        da = [self.report.da2,self.report.da1[1]]
        ManageOperation.win.splitter.widget(0).setParent(None)
        ManageOperation.win.splitter.insertWidget(0, Statistics_class_win.Statistics_class_win(da))