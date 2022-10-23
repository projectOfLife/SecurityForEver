from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi("../GUI/Test.ui", self) # Load Design File

        self.show() # GUI window



app = QtWidgets.QApplication(sys.argv) # Start App
window = MainWindow()
app.exec() # Exit app when Press X