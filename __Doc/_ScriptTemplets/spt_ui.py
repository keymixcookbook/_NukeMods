'''

UI elements for MODNAME

'''


#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import sys
from Qt import QtWidgets, QtCore, QtGui
import platform




#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




FIELD_SIZE=60




#------------------------------------------------------------------------------
#-UI
#------------------------------------------------------------------------------




class Ui_MODNAME(object):
    '''UI elements'''

    def setupUi(self,core):
        '''ui setup'''

        # Window
        core.setWindowTitle()
        core.setWindowFlags()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    core=QtWidgets.QWidget()
    Ui_MODNAME = Ui_MODNAME()
    Ui_MODNAME.setupUi(core)
    core.show()
    core.raise_()
    app.exec_()
