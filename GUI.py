# importing modules used here
import sys
from PyQt5.QtWidgets import QApplication

# passing empty list because we are not using command line arguments
app = QApplication(sys.argv)

# Start the event loop.
app.exec_()
