# this file is responsible for all the graphics
# importing modules used here
import sys
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Studierendenverwaltung")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)

   window = MainWindow()

   window.show()

   sys.exit(app.exec_())
