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




class Core__PySidePanel_(QtWidgets.QWidget):
    def __init__(self):
        super(_PySidePanel_, self).__init__()


    def setDefault(self):
        '''set default value when instancing'''


    def run(self):
        '''run panel instance'''
        self.show()


# Show the panel
_PySidePanel_ = Core__PySidePanel_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    _PySidePanel_.run()
    app.exec_()
else:
    _PySidePanel_.run()
