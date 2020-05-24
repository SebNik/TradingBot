# this file is responsible for all the graphics
# importing modules used here
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        # setting all the important things for main window
        super(MainWindow, self).__init__(*args, **kwargs)
        # setting the variables for window
        self.left = 50
        self.right = 50
        self.width = 1700
        self.height = 1000
        # setting all paths
        self.icon_path = '/home/niklas/Desktop/TradingBot/GUI/Icon/icon1.jpg'
        # setting the full graphics up
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.setWindowTitle('My Trading App')
        self.setWindowIcon(QIcon(self.icon_path))
        print('lol')


if __name__ == "__main__":
    # passing empty list because we are not using command line arguments
    app = QApplication([])

    # creating a window and showing it
    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec_()
