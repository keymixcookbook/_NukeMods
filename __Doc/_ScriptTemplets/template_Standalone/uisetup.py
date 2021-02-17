'''

UI elements for ui_MODNAME

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import sys
from Qt import QtWidgets, QtCore, QtGui




#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




UI=True




#------------------------------------------------------------------------------
#-UI
#------------------------------------------------------------------------------




class ui_MODNAME(object):
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
    ui_MODNAME = ui_MODNAME()
    ui_MODNAME.setupUi(core)
    # Test Run
    ui_MODNAME.run()
    
    app.exec_()
