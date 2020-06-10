import nuke, nukescripts,sys
from Qt import QtWidgets, QtGui, QtCore





class Core_PYSIDEPANEL(QtWidgets.QWidget):
    def __init__(self):
        super(Core_PYSIDEPANEL, self).__init__()


    def setDefault(self):
        '''set default value when instancing'''


    def run(self):
        '''run panel instance'''
        self.show()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    PYSIDEPANEL = Core_PYSIDEPANEL()
    PYSIDEPANEL.run()
    app.exec_()
else:
    PYSIDEPANEL = Core_PYSIDEPANEL()
    PYSIDEPANEL.run()
