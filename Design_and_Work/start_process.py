from PyQt5.QtWidgets import QWidget, QApplication, QProgressBar, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
import sys
from threading import Thread
from multiprocessing import Process
import os
from Design_and_Work.home import Home


class Crawler(Thread):
    # THREAD 1
    def run(self):
        print(os.getcwd())
        os.chdir('C:\\Users\sunny ahmed\Desktop\Web on mind\WebSpider')
        print(os.getcwd())
        os.system('scrapy crawl ps4bot')


class Root(QWidget, Thread):
    def __init__(self):
        super().__init__()

        self.title = 'Web on Mind'
        self.left = 400
        self.top = 200
        self.width = 500
        self.height = 200
        self.icon = 'resources\\app.ico'
        self.bar = ''

        self.init_window()

    def init_window(self):
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet('background-color:orange')
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.start_component()
        self.show()

    def start_component(self):
        self.bar = QProgressBar(self)
        self.bar.setGeometry(0, 170, 541, 30)
        btn = QPushButton('Load', self)
        btn.setStyleSheet('color:#FFFFFF')
        btn.setFont(QtGui.QFont('Arial', 10, weight=QtGui.QFont.Helvetica))
        btn.setGeometry(QtCore.QRect(190, 130, 100, 40))
        btn.clicked.connect(self.run_processes)

    def run(self):
        # THREAD 2
        counter = 0
        while counter < 100:
            counter += 0.00001
            self.bar.setValue(counter)

    def run_processes(self):
        # THREAD 1
        s = Crawler()
        s.start()

        # THREAD 2
        self.start()

        s.join()
        self.join()

        home = Home()
        home.show()
        self.hide()


App = QApplication(sys.argv)
root = Root()
sys.exit(App.exec())
