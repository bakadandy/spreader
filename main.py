import sys
import GUI
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI.LoginWindow()
    window.show()
    sys.exit(app.exec_())
