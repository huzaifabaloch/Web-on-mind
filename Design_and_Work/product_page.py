from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout
from PyQt5 import QtGui, QtCore
import urllib.request

class ProductPage(QMainWindow):
    def __init__(self, product_details, category):
        super().__init__()

        self.title = 'Product'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 500
        self.icon = 'resources\\app.ico'
        self.product_details = product_details
        self.category = category

        self.init_window()
        self.product_layout()

    def init_window(self):
        #self.setWindowIcon(QtGui.QFont(self.icon))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


    def product_layout(self):

        v_box = QVBoxLayout()

        # url of image to open from web.
        if self.category == 1:
            url = self.product_details[2]
            #data = urllib.request.urlopen(url).read()
            #print(data)
        else:
            url = self.product_details[3]
            print(url)

