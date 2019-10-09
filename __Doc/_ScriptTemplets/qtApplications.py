from PySide.QtGui import *
from PySide.QtCore import *
import sys


class PysidePanelApp(QWidget):
    def __init__(self):
        super(PysidePanelApp, self).__init__()




# Show the panel
panel = PysidePanelApp()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel.show()
    app.exec_()
else:
    panel.show()
