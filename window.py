import os
import sqlite3
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import mapping as map
import mapping2 as map2
import main as m
import sys


class jobs_window(QWidget):
    def __init__(self):
        super().__init__()
        m.add_jobs_data()
        self.setup_window()
        self.window1 = data_window()
        self.show()

    def setup_window(self):
        loadUi("welcome.ui", self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("State Employment Data")
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton("Update Data", self)
        self.pushButton.setGeometry(QRect(10, 100, 171, 71))
        self.pushButton.clicked.connect(self.getfile)
        self.pushButton_2 = QPushButton("Visualize Data", self)
        self.pushButton_2.clicked.connect(self.toggle_window1)
        self.pushButton_2.setGeometry(QRect(420, 100, 171, 71))
        self.label.setGeometry(QRect(100, 10, 391, 81))
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(10, 180, 621, 480))
        self.label_2.setPixmap(QPixmap("grad.jpg"))
        self.show()

    def getfile(self):
        this_folder = os.path.dirname(os.path.abspath(__file__))
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file',
                                                     this_folder, "Excel (*.xls *.xlsx)")
        if not fname == "":
            path = os.path.normpath(fname)
            m.drop_jobs_data()  # drop the default excel file loaded
            m.add_jobs_data('college_data.sqlite', path.split(os.sep)[-1])  # load the selected file

    def toggle_window1(self):
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.show()


class data_window(QDialog):
    def __init__(self):
        super(data_window, self).__init__()
        loadUi("main.ui", self)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setHorizontalHeaderLabels(["State", "Grads", "Jobs", "Rate"])
        self.loaddata()

    def loaddata(self):
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("State Employment Data")
        self.rename = QPushButton("Refresh", self)
        self.rename.setGeometry(QRect(200, 10, 93, 28))
        self.rename.clicked.connect(self.update_data)
        self.mapping = QPushButton("View Map", self)
        self.mapping.setGeometry(QRect(445, 10, 93, 28))
        self.mapping.clicked.connect(self.visualize)
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(310, 10, 120, 30)
        order = ["Ascending", "Descending"]
        self.combo_box.addItems(order)
        self.combo_box.setInsertPolicy(QComboBox.NoInsert)
        self.combo_box2 = QComboBox(self)
        self.combo_box2.setGeometry(550, 15, 220, 30)
        comparison = ["3 year graduate cohort declining balance percentage to the 25% salary in the state",
                      "College graduates in a state to number of jobs in that state that likely expect a college education"]
        self.combo_box2.addItems(comparison)
        self.combo_box2.setInsertPolicy(QComboBox.NoInsert)
        self.combo_box2.setSizeAdjustPolicy(self.combo_box2.AdjustToContents)
        self.combo_box2.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Fixed)

    def update_data(self):
        comboText = self.combo_box.currentText()
        comboText2 = self.combo_box2.currentText()
        connection = sqlite3.connect("college_data.sqlite")
        sqlquery = '''SELECT state_abbrev AS State, grads AS Grads, sum(tot_emp) AS Jobs, sum(tot_emp)/grads AS Rate
        FROM jobs_data inner join state_lookup ON jobs_data.area_title = state_lookup.state_name
        inner join (SELECT state, sum(size_2019)/4 AS grads
        FROM college_data GROUP BY state) grads ON state_lookup.state_abbrev = grads.state
        WHERE job_id NOT LIKE '3%'  AND job_id NOT LIKE '4%'
        GROUP BY area_title ORDER BY Rate '''
        query = '''SELECT State, round(avg(grads_repay_cohort)*100, 2)||'%' AS 'Declining Balance', 
        round(AVG(a_pct25),2) AS Wage,
        round(AVG(grads_repay_cohort)*AVG(a_pct25),2) AS Income FROM jobs_data 
        inner join state_lookup ON jobs_data.area_title = state_lookup.state_name
        inner join college_data ON state_lookup.state_abbrev = college_data.state
        GROUP BY state ORDER BY Income '''
        if comboText == "Ascending" and comboText2 == "3 year graduate cohort declining balance percentage" \
                                                      " to the 25% salary in the state":
            query += comboText[0:3] + ";"
            result = connection.execute(query)
            self.insert_data(result)
        elif comboText == "Descending" and comboText2 == "3 year graduate cohort declining balance percentage" \
                                                         " to the 25% salary in the state":
            query += comboText[0:4] + ";"
            result = connection.execute(query)
            self.insert_data(result)
        elif comboText == "Ascending" and comboText2 == "College graduates in a state to number of jobs in that state" \
                                                        " that likely expect a college education":
            sqlquery += comboText[0:3] + ";"
            result = connection.execute(sqlquery)
            self.insert_data(result)
        else:
            sqlquery += comboText[0:4] + ";"
            result = connection.execute(sqlquery)
            self.insert_data(result)
        connection.close()

    def insert_data(self, result):
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number == 3:
                    if (int(data) in range(8000, 12000)) or (data in range(0, 15)):
                        [self.tableWidget.item(row_number, c).setBackground(Qt.red) for c in range(len(row_data))]
                    elif (int(data) in range(12000, 15000)) or (data in range(15, 20)):
                        [self.tableWidget.item(row_number, c).setBackground(Qt.magenta) for c in range(len(row_data))]
                    elif (int(data) in range(15000, 20000)) or (data in range(20, 30)):
                        [self.tableWidget.item(row_number, c).setBackground(Qt.yellow) for c in range(len(row_data))]
                    elif (int(data) in range(20000, 25000)) or (data in range(30, 40)):
                        [self.tableWidget.item(row_number, c).setBackground(Qt.green) for c in range(len(row_data))]
                    elif (int(data) in range(25000, 50000)) or (data in range(40, 100)):
                        [self.tableWidget.item(row_number, c).setBackground(Qt.blue) for c in range(len(row_data))]

    def visualize(self):
        if self.combo_box2.currentText() == "3 year graduate cohort declining balance percentage" \
                                            " to the 25% salary in the state":
            map2.main()
        elif self.combo_box2.currentText() == "College graduates in a state to number of jobs in that state" \
                                              " that likely expect a college education":
            map.main()


class start_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("State Employment Data")
        self.label = QLabel()
        self.label.setPixmap(QPixmap("wait.png"))
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)
        self.setGeometry(600, 300, 320, 200)
        self.show()
        m.add_school_data()
        self.jobs_window = jobs_window()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = start_window()
    sys.exit(app.exec_())
