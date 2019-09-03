from PyQt5.QtWidgets import QMainWindow, QLineEdit, QCompleter, QApplication, QAction, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import mysql.connector
from Design_and_Work.product_page import ProductPage


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Web on Mind [Home]'
        self.left = 200
        self.top = 100
        self.width = 900
        self.height = 400
        self.icon = 'resources\\app.ico'

        self.init_window()

    def create_connection(self):
        """Creating connection to server and returning."""

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )

        return conn

    def get_product_name(self):
        """"
        Retrieving product names of all categories from all tables
        for adding them to QCompleter for auto completion.
        """

        games_name = []  # To hold game names.
        shoes_name = []  # To hold shoe names.
        products = []  # To hold all category product names.

        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name_of_game FROM ps4_tbl')
        games = cursor.fetchall()
        for each_game in games:
            games_name.append(each_game[0].lower())

        cursor.execute('SELECT name_of_shoe FROM shoes_tbl')
        shoes = cursor.fetchall()
        for each_shoe in shoes:
            shoes_name.append(each_shoe[0].lower())

        products.extend(games_name)
        products.extend(shoes_name)

        cursor.close()
        conn.close()

        return products

    def init_window(self):
        """Window with default components after clicked.connect."""

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_menu_bar()
        self.create_toolbar()
        self.main_layout()

        self.get_product_name()

        self.show()

    def create_menu_bar(self):

        main_menu = self.menuBar()
        site_menu = main_menu.addMenu('Sites')

        self.amazon = QAction(QtGui.QIcon('resources\\amazonico.ico'), 'Amazon', self)
        site_menu.addAction(self.amazon)
        self.ebay = QAction(QtGui.QIcon('resources\\ebayico.ico'), 'Ebay', self)
        site_menu.addAction(self.ebay)
        self.daraz = QAction('Daraz', self)
        site_menu.addAction(self.daraz)

    def create_toolbar(self):

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(self.amazon)
        toolbar.addAction(self.ebay)

    def main_layout(self):

        products = self.get_product_name()

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search any thing')
        self.search_bar.setCompleter(QCompleter(products))
        self.search_bar.setGeometry(QtCore.QRect(20, 100, 850, 50))
        self.search_bar.setFont(QtGui.QFont('Arial', 20))

        self.search_btn = QPushButton('Search', self)
        self.search_btn.setGeometry(QtCore.QRect(300, 300, 200, 40))
        self.search_btn.clicked.connect(self.product_page)

        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setGeometry(QtCore.QRect(500, 300, 200, 40))
        self.clear_btn.clicked.connect(self.clear_string)

    def clear_string(self):
        """Clear search bar string and set back the focus."""

        self.search_bar.clear()
        self.search_bar.setFocus()

    def product_page(self):
        """
        Get the text from search bar and check in the database for a match.
        if a match occurs showing that product page window with product details.
        """

        product = self.search_bar.text()

        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ps4_tbl")
        games = cursor.fetchall()
        cursor.execute("SELECT * FROM shoes_tbl")
        shoes = cursor.fetchall()

        for each_category in range(2):
            if each_category == 0:
                category = 1
                for each_game in games:
                    if product == each_game[0].lower():
                        self.product_page = ProductPage(each_game, category)
                        break
            else:
                category = 2
                for each_shoe in shoes:
                    if product == each_shoe[0].lower():
                        self.product_page = ProductPage(each_shoe, category)
                        break


App = QApplication(sys.argv)
root = Home()
sys.exit(App.exec())
