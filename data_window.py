import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import sqlite3

class data_window(QDialog):
    def __init__(self):
        super(data_window, self).__init__()
        loadUi("main.ui", self)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setHorizontalHeaderLabels(["State", "Grads", "Jobs"])
        self.loaddata()

    def loaddata(self):
        connection = sqlite3.connect("college_data.sqlite")
        sqlquery = '''SELECT state_abbrev, grads AS Grads, sum(tot_emp) AS Jobs FROM jobs_data
inner join state_lookup ON jobs_data.area_title = state_lookup.state_name
inner join (SELECT state, sum(size_2019)/4 AS grads
FROM college_data GROUP BY state) grads ON state_lookup.state_abbrev = grads.state
WHERE job_id NOT LIKE '3%'  AND job_id NOT LIKE '4%'
GROUP BY area_title;'''
        result = connection.execute(sqlquery)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(580)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")