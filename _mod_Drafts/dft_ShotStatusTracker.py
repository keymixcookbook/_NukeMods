import nuke, nukescripts
try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtWidgets

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets



class Table_SSS(QtWidgets.QTableWidget):
    def __init__(self):
        super(Table_SSS, self).__init__()


    def getData(self):
        '''craw data from json file'''


class Core_ShotStatusTracker(QtWidgets.QWidget):
    def __init__(self):
        super(ShotStatusTracker, self).__init__()

        self.title = QtWidgets.QLabel('Shot Status Traker')


    def setDefault(self):
        '''set default value when instancing'''


    def run(self):
        '''run panel instance'''
        self.show()


# Show the panel
ShotStatusTracker = Core_ShotStatusTracker()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ShotStatusTracker.run()
    app.exec_()
else:
    ShotStatusTracker.run()
