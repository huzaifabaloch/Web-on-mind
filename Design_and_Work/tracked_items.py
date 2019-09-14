from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton
from PyQt5 import QtGui, QtCore
import mysql.connector
import sys


class TrackedItem(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Tracked Items'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 500
        self.icon = 'resources\\app.ico'


        self.init_window()


    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.create_table_and_show_data()
        self.create_buttons()
        self.setLayout(self.vbox)

        self.show()

    def create_connection(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )

        return conn

    def create_table_and_show_data(self):

        self.vbox = QVBoxLayout()

        columns = ['ID', 'Product Name', 'Actual Price', 'User Price']

        table = QTableWidget(self)
        table.setRowCount(10)
        table.setColumnCount(4)
        table.setFixedSize(600, 500)
        self.vbox.addWidget(table)
        header = table.horizontalHeader()
        header.setVisible(False)
        vertical = table.verticalHeader()
        vertical.setVisible(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        conn = self.create_connection()
        my_cursor = conn.cursor()
        query = 'SELECT * FROM track_tbl'
        my_cursor.execute(query)
        result = my_cursor.fetchmany(10)
        table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        for row in range(0, 1):
            table.insertRow(row)
            for key, item in enumerate(columns):
                table.setItem(row, key, QTableWidgetItem(columns[key]))



    def create_buttons(self):

        modify_btn = QPushButton('Modify Price', self)
        modify_btn.setFont(QtGui.QFont('Calibri', 12))
        self.vbox.addWidget(modify_btn)






#App = QApplication(sys.argv)
#tracked_items = TrackedItem()
#tracked_items.init_window()
#sys.exit(App.exec())
