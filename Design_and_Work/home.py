from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Web on Mind [Home]'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 400
        self.icon = 'resources\\app.ico'

        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setGeometry(self.left, self.top, self.width, self.height)
