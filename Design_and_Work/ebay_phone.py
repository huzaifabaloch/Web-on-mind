from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QVBoxLayout
from PyQt5 import QtGui
import mysql.connector
from Design_and_Work.product_page import ProductPage


class Ebay(QWidget):
    """A form with amazon's playstation 4 data."""

    def __init__(self):
        super().__init__()

        self.title = 'Ebay'
        self.left = 200
        self.top = 100
        self.width = 900
        self.height = 600
        self.icon = 'resources\\app.ico'

        self.init_window()
        self.create_phone_table()
        self.create_buttons()
        self.show()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setStyleSheet('background-color: white')
        self.setGeometry(self.left, self.top, self.width, self.height)

    def create_connection(self):

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )
        return conn

    def gather_data(self):

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            query = 'SELECT name_of_phone, price FROM phone_tbl'
            cur.execute(query)
            result = cur.fetchall()
            return result
        except:
            QMessageBox.warning(self, 'connection error', 'Connection lost!')
            return
        finally:
            cur.close()
            conn.close()

    def set_color_row(self, table):
        """To change the color of rows in the table widget."""

        for i in range(table.rowCount()):
            if i % 2 == 0:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(252, 252, 252))
            else:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(232, 225, 225))

    def create_phone_table(self):

        column_names = ['Name of Phone', 'Price of Phone']

        self.vbox = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(2)
        self.table.setGeometry(10, 0, 880, 600)
        #table.setStyleSheet('color:black; background-color:white; font:bold; font-size: 14px')
        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setVisible(False)
        vertical_header = self.table.verticalHeader()
        vertical_header.setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.vbox.addWidget(self.table)

        self.table.cellClicked.connect(self.get_cell_item)

        data = self.gather_data()

        try:
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

            self.set_color_row(self.table)

            for row in range(0, 1):
                self.table.insertRow(row)
                for key, item in enumerate(column_names):
                    self.table.setItem(row, key, QTableWidgetItem(column_names[key]))
                    self.table.item(row, key).setBackground(QtGui.QColor(176, 171, 171))
                    self.table.item(row, key).setFont(QtGui.QFont('Arial', 10, weight=QtGui.QFont.Bold))


        except Exception as e:
            QMessageBox.warning(self, 'error', 'Something went wrong!' + str(e))
            return

    def create_buttons(self):

        check_product = QPushButton('See Product', self)
        check_product.setFixedHeight(40)
        check_product.setStyleSheet('background-color:#db5e5e; color:#ffffff; font: bold 12px; border: 0px;')
        check_product.clicked.connect(self.see_product)
        self.vbox.addWidget(check_product)
        close = QPushButton('Close', self)
        close.setFixedHeight(40)
        close.setStyleSheet('background-color:#c43737; color:#ffffff; font: bold 12px; border: 0px;')
        close.clicked.connect(self.hide)
        self.vbox.addWidget(close)

        self.setLayout(self.vbox)

    def get_cell_item(self, row, column):

        print("Row %d and Column %d was clicked" % (row, column))
        item_name = self.table.item(row, column)
        self.product_name = item_name.text()

    def see_product(self):

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            query = 'SELECT * FROM phone_tbl WHERE name_of_phone=%s'
            cur.execute(query, (self.product_name, ))
            product_details = cur.fetchone()
            if product_details is not None:
                self.product_page = ProductPage(product_details, 2)
            else:
                QMessageBox.warning(self, 'error', 'Please Select on a product name to modify.')
                return
        except:
            QMessageBox.warning(self, 'error', 'Please Select on a product name to modify.')
        finally:
            cur.close()
            conn.close()
