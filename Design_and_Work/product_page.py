from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QGroupBox, QLineEdit, QMessageBox, QPushButton, QGridLayout
from PyQt5 import QtGui, QtCore
from urllib.request import urlopen
import mysql.connector


class ProductPage(QWidget):
    def __init__(self, product_details, category):
        super().__init__()

        self.title = 'Product'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 300
        self.icon = 'resources\\app.ico'
        self.product_details = product_details
        self.category = category

        self.init_window()

    def init_window(self):

        try:
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)
            self.product_layout()
            self.show()
        except:
            QMessageBox.warning(self, 'Internet Error', 'No Internet Connection Found!')
            return -1

    def product_traction(self):
        self.product_track = ProductTraction(self.product_details, self.category)

    def product_layout(self):

        v_box = QVBoxLayout()

        if self.category == 1:
            # url of image to open from web.
            url = self.product_details[2]
            data = urlopen(url).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            pix = QtGui.QPixmap(image)
            label = QLabel(self)
            label.setPixmap(pix)
            label.setGeometry(20, 20, 400, 300)

            product_title = QLabel(self)
            product_title.setText(self.product_details[0])
            product_title.setGeometry(200, 0, 1000, 300)
            product_title.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))

            product_price = QLabel(self)
            product_price.setText('$' + self.product_details[1])
            product_price.setGeometry(400, 100, 50, 30)
            product_price.setFont(QtGui.QFont('Arial', 20, weight=QtGui.QFont.Bold))
            product_price.setStyleSheet('color:red')

            v_box.addWidget(product_title)
            v_box.addWidget(label)
            self.setLayout(v_box)

        else:
            url = self.product_details[3]
            data = urlopen(url).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            pix = QtGui.QPixmap(image)
            label = QLabel(self)
            label.setPixmap(pix)
            label.setGeometry(20, 20, 400, 300)
            self.v_box.addWidget(label)

        track_btn = QPushButton('Track', self)
        track_btn.setGeometry(330, 230, 150, 50)
        track_btn.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
        track_btn.clicked.connect(self.product_traction)


# ---------------------------------------------------------------------------------
class ProductTraction(QDialog):
    def __init__(self, product_details, category):
        super().__init__()

        self.title = 'Product Traction'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 100
        self.product_details = product_details
        self.category = category
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

            if self.category == 1:

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
                self.actual_price = '$' + self.product_details[1]
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
            product_actual_price = int(self.actual_price[1:])
            product_user_price = int(self.user_price.text())

            if product_user_price >= product_actual_price:
                QMessageBox.warning(self, 'fix price', 'User price should not be greater or equal to actual price')
                return

            product_check = self.check_if_product_already_on_track_list(product_title)
            if product_check is not None:
                QMessageBox.warning(self, 'Product Exists', 'Product is already on tracking list.')
                return

            my_cursor = conn.cursor()
            my_cursor.execute('SELECT id FROM track_tbl ORDER BY id DESC LIMIT 1')
            record_no = my_cursor.fetchone()
            if record_no is None:
                record_no = 1
            else:
                record_no = record_no[0] + 1

            print(record_no)
            print(record_no, product_title, product_actual_price, product_user_price)

            my_cursor.execute("""INSERT INTO track_tbl VALUES (%s, %s, %s, %s)""", (
                                record_no, product_title, product_actual_price, product_user_price
                            ))
            conn.commit()
            QMessageBox.about(self, 'product track', 'Product is on tracked. We will notify you when price falls down.')

        except Exception as err:
            QMessageBox.about(self, 'error', str(err))

        finally:
            my_cursor.close()
            conn.close()

    def check_if_product_already_on_track_list(self, product_name):
        """To check if product already on track list"""

        conn = self.create_connection()
        my_cursor = conn.cursor()
        query = 'SELECT title FROM track_tbl WHERE title=%s'
        my_cursor.execute(query, (product_name,))
        result = my_cursor.fetchone()

        return result







