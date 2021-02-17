'''

UI elements for MODNAME (Replace MODNAME for actual name)

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import sys
from Qt import QtWidgets, QtCore, QtGui




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
        '''ui setup
        @core: (object) Input object for setting up
        '''

        # Define Widgets and Properties

        # Define Layouts

        # Assign Widgets to Layouts

        # Window
        core.setLayout(self.layout_master)
        core.setWindowTitle()
        core.setWindowFlags()

    def run(self):
        '''main run function'''
        
        core.show()
        core.raise_()




#------------------------------------------------------------------------------
#-Run Instance
#------------------------------------------------------------------------------




if __name__ == '__main__':
    print("="*10)
    print("\nTest UI for MODNAME\n")
    print("="*10)

    app = QtWidgets.QApplication(sys.argv)
    
    # Test Widgets
    core=QtWidgets.QWidget()
    # Test Mod
    Ui_MODNAME = Ui_MODNAME()
    Ui_MODNAME.setupUi(core)
    # Test Run
    Ui_MODNAME.run()
    
    app.exec_()
