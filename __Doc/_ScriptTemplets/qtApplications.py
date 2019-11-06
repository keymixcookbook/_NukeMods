import nuke, nukescripts
from Qt import QtWidgets, QtGui, QtCore





class Core__PySidePanel_(QtWidgets.QWidget):
    def __init__(self):
        super(_PySidePanel_, self).__init__()


    def setDefault(self):
        '''set default value when instancing'''


    def run(self):
        '''run panel instance'''
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    _PySidePanel_ = Core__PySidePanel_()
    _PySidePanel_.run()
    app.exec_()
else:
    _PySidePanel_ = Core__PySidePanel_()
    _PySidePanel_.run()
