# this file is responsible for all the graphics
# importing modules used here
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)


if __name__ == "__main__":
    # passing empty list because we are not using command line arguments
    app = QApplication([])

    # creating a window and showing it
    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec_()
