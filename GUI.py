# importing modules used here
from PyQt5.QtWidgets import QApplication, QMainWindow

# passing empty list because we are not using command line arguments
app = QApplication([])

# creating a window and showing it
window = QMainWindow()
window.show()

# Start the event loop.
app.exec_()
