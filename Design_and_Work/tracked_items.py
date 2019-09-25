from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QVBoxLayout, QPushButton, QMessageBox, QGroupBox, QGridLayout
from PyQt5 import QtGui, QtCore
import mysql.connector


class TrackedItem(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Items on Tracked'
        self.left = 200
        self.top = 100
        self.width = 900
        self.height = 400
        self.icon = 'resources\\app.ico'

        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.create_table_and_show_data()
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

    def set_color_row(self, table):
        """To change the color of rows in the table widget."""

        for i in range(table.rowCount()):
            if i % 2 == 0:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(252, 252, 252))
            else:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(232, 225, 225))

    def create_table_and_show_data(self):

        conn = self.create_connection()
        my_cursor = conn.cursor()
        columns = ['ID', 'Product Name', 'Actual Price', 'User Price']

        try:
            self.setFixedSize(920, 500)
            self.vbox = QVBoxLayout()
            query = 'SELECT * FROM track_tbl'
            my_cursor.execute(query)
            result = my_cursor.fetchall()

            if result:

                self.table = QTableWidget(self)
                self.table.setRowCount(10)
                self.table.setColumnCount(4)
                self.table.setFixedSize(900, 400)
                self.vbox.addWidget(self.table)
                header = self.table.horizontalHeader()
                header.setVisible(False)
                vertical = self.table.verticalHeader()
                vertical.setVisible(False)
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.Stretch)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.table.setEditTriggers(QTableWidget.NoEditTriggers)

                self.create_buttons()

                self.table.setRowCount(0)

                for row_number, row_data in enumerate(result):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.set_color_row(self.table)

                for row in range(0, 1):
                    self.table.insertRow(row)
                    for key, item in enumerate(columns):
                        self.table.setItem(row, key, QTableWidgetItem(columns[key]))

                # When any cell clicked on table, it automatically let us grab the item on that location by passing row
                # and column as parameters in the triggered function.
                self.table.cellClicked.connect(self.get_cell_item)

            else:
                self.setFixedSize(900, 400)
                tracked_product_unavailable = QLabel('You have not set any product on track. Start adding by searching your favourite product ', self)
                tracked_product_unavailable.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
                tracked_product_unavailable.move(120, 100)
                tracked_product_unavailable.setFixedSize(900, 200)

                product_unavailable_image = QtGui.QPixmap('resources\product_unavailable.png')
                image_lbl = QLabel(self)
                image_lbl.setPixmap(product_unavailable_image)
                image_lbl.move(380, -100)
                image_lbl.setFixedSize(400, 400)

                ok_btn = QPushButton('Okay', self)
                ok_btn.move(350, 300)
                ok_btn.setFixedSize(200, 50)
                ok_btn.setStyleSheet('background-color: #1c1d21; color: #ffffff; font-size: 14px; border-radius: 10px')
                ok_btn.clicked.connect(self.hide)

        except Exception as e:
            print(str(e))

    def create_buttons(self):

        modify_btn = QPushButton('Modify Price', self)
        modify_btn.setFont(QtGui.QFont('Calibri', 12))
        modify_btn.clicked.connect(self.modify)
        modify_btn.setStyleSheet('background-color: #1c1d21; color: #ffffff; font-size: 14px; border-radius: 10px')
        modify_btn.setFixedSize(900, 30)
        self.vbox.addWidget(modify_btn)

        delete_btn = QPushButton('Remove Product', self)
        delete_btn.setFont(QtGui.QFont('Calibri', 12))
        delete_btn.clicked.connect(self.delete)
        delete_btn.setStyleSheet('background-color: #1c1d21; color: #ffffff; font-size: 14px; border-radius: 10px')
        delete_btn.setFixedSize(900, 30)
        self.vbox.addWidget(delete_btn)

    def get_cell_item(self, row, column):

        print("Row %d and Column %d was clicked" % (row, column))
        item_name = self.table.item(row, column)
        self.product_name = item_name.text()

    def modify(self):

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT title, actual_price FROM track_tbl WHERE title = %s', (self.product_name, ))
            product_details = cur.fetchone()
            if product_details is not None:
                self.product_modification = ProductModification(product_details)
                self.hide()
            else:
                QMessageBox.warning(self, 'error', 'Please Select on a product name to modify.')
                return

        except Exception as err:
            QMessageBox.warning(self, 'error', 'Please Select on a product name to modify.')

        finally:
            cur.close()
            conn.close()

    def delete(self):

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM track_tbl WHERE title = %s', (self.product_name, ))
            conn.commit()
            QMessageBox.warning(self, 'deleted', f"Product '{self.product_name}' deleted successfully")
            self.hide()
        except:
            QMessageBox.warning(self, 'failed', 'Something went wrong while deleting.')
        finally:
            cur.close()
            conn.close()


# -----------------------------------------------------------------
class ProductModification(QWidget):
    def __init__(self, product_details):
        super().__init__()

        self.title = 'Product Modification'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 100
        self.product_details = product_details
        self.title = ''
        self.actual_price = ''
        self.user_price = ''

        self.show_dialog()

    def create_connection(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )
        return conn

    def show_dialog(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.set_track()
        self.show()

    def set_track(self):
        """To show the prompt where use is setting up a target price of a product."""

        try:
            self.group_box = QGroupBox('Product Detail')
            self.group_box.setFont(QtGui.QFont('calibri', 12, weight=QtGui.QFont.Bold))
            self.group_box.setGeometry(QtCore.QRect(0, 0, 900, 200))
            grid_box = QGridLayout()

            # HEADERS
            product_title_header = QLabel('Product Name', self)
            product_price_header = QLabel('Actual Price', self)
            product_user_price_header = QLabel('User Price', self)
            grid_box.addWidget(product_title_header, 0, 0)
            grid_box.addWidget(product_price_header, 0, 2)
            grid_box.addWidget(product_user_price_header, 0, 4)

            # VALUES
            product_title = QLabel(self)
            self.title = self.product_details[0]
            product_title.setText(self.title)
            product_title.setFont(QtGui.QFont('Arial', 12, QtGui.QFont.Bold))
            product_price = QLabel(self)
            self.actual_price = '$' + str(self.product_details[1])
            product_price.setText(self.actual_price)
            product_price.setFont(QtGui.QFont('Arial', 12, QtGui.QFont.Bold))
            product_price.setStyleSheet('color:red')
            grid_box.addWidget(product_title, 2, 0)
            grid_box.addWidget(product_price, 2, 2)

            self.user_price = QLineEdit(self)
            self.user_price.setFont(QtGui.QFont('calibri, 14', weight=QtGui.QFont.Bold))
            grid_box.addWidget(self.user_price, 2, 4)
            self.group_box.setLayout(grid_box)

            start_tracking = QPushButton('Start Tracking', self)
            start_tracking.setGeometry(0, 0, 0, 50)
            start_tracking.clicked.connect(self.add_to_track)
            grid_box.addWidget(start_tracking, 3, 1, 3, 4)

            v_box = QVBoxLayout()
            v_box.addWidget(self.group_box)
            self.setLayout(v_box)

        except Exception as err:
            QMessageBox.warning(self, 'error', str(err))
            return

    def add_to_track(self):

        conn = self.create_connection()
        my_cursor = conn.cursor()

        try:
            product_title = self.title
            product_actual_price = float(self.actual_price[1:])
            product_user_price = float(self.user_price.text())

            if product_user_price >= product_actual_price:
                QMessageBox.warning(self, 'fix price', 'User price should not be greater or equal to actual price')
                return

            my_cursor.execute('UPDATE track_tbl SET user_price = %s WHERE title = %s', (product_user_price, product_title, ))
            conn.commit()
            QMessageBox.about(self, 'product track', 'Product modified. We will notify you when price falls down.')
            self.hide()

        except Exception as err:
            QMessageBox.about(self, 'error', str(err))

        finally:
            my_cursor.close()
            conn.close()
# ------------------------------------------------------------------------------------------------


class FinishedTracking(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Items Tracked'
        self.left = 200
        self.top = 100
        self.width = 900
        self.height = 400
        self.icon = 'resources\\app.ico'

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.create_table_and_show_data()
        self.show()

    def set_color_row(self, table):
        """To change the color of rows in the table widget."""

        for i in range(table.rowCount()):
            if i % 2 == 0:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(252, 252, 252))
            else:
                for j in range(table.columnCount()):
                    table.item(i, j).setBackground(QtGui.QColor(232, 225, 225))

    def create_connection(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )
        return conn

    def create_table_and_show_data(self):

        columns = ['ID', 'Product Name', 'Actual Price', 'User Price']

        conn = self.create_connection()
        my_cursor = conn.cursor()
        query = 'SELECT * FROM finished_tracking_tbl'
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        print(result)
        if result:
            self.setFixedSize(900, 400)
            self.table = QTableWidget(self)
            self.table.setRowCount(10)
            self.table.setColumnCount(4)
            self.table.setFixedSize(900, 350)
            header = self.table.horizontalHeader()
            header.setVisible(False)
            vertical = self.table.verticalHeader()
            vertical.setVisible(False)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.table.setRowCount(0)

            empty_list_btn = QPushButton('Click here to empty the list', self)
            empty_list_btn.move(0, 350)
            empty_list_btn.setFixedSize(900, 50)
            empty_list_btn.setStyleSheet('background-color: #1c1d21; color: #ffffff; font-size: 14px')
            empty_list_btn.clicked.connect(self.delete_finished_ones)

            for row_number, row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.set_color_row(self.table)

            for row in range(0, 1):
                self.table.insertRow(row)
                for key, item in enumerate(columns):
                    self.table.setItem(row, key, QTableWidgetItem(columns[key]))

            # When any cell clicked on table, it automatically let us grab the item on that location by passing row
            # and column as parameters in the triggered function.
            #self.table.cellClicked.connect(self.get_cell_item)

        else:
            self.setFixedSize(900, 400)
            tracked_product_unavailable = QLabel('Currently, no product has been tracked. The moment any product get tracked, it will appear here.', self)
            tracked_product_unavailable.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
            tracked_product_unavailable.move(100, 180)

            product_unavailable_image = QtGui.QPixmap('resources\product_unavailable.png')
            image_lbl = QLabel(self)
            image_lbl.setPixmap(product_unavailable_image)
            image_lbl.move(380, 30)

            ok_btn = QPushButton('Okay', self)
            ok_btn.move(350, 300)
            ok_btn.setFixedSize(200, 50)
            ok_btn.setStyleSheet('background-color: #1c1d21; color: #ffffff; font-size: 14px; border-radius: 10px')
            ok_btn.clicked.connect(self.hide)

    def delete_finished_ones(self):
        """Remove the products that were tracked and stored in finished form."""

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            reply = QMessageBox.question(self, 'Delete', 'Are you sure, Do you want to empty the list', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                cur.execute('DELETE FROM finished_tracking_tbl')
                conn.commit()
                self.hide()
                QMessageBox.warning(self, 'Delete', 'All Products removed from the list.', QMessageBox.Ok)
            else:
                return
        except:
            QMessageBox.warning(self, 'error', 'Something went wrong!')
            return
        finally:
            cur.close()
            conn.close()
