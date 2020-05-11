import os
import sys
import nukescripts
import nuke
from Qt import QtWidgets, QtGui, QtCore
import mod_StudioLoad
import importlib


def _version_():
    ver = '''

    version 1.0
    - log execute history

    version 0.0
	- nukescript panel for testing modules

	'''
    return ver




#------------------------------------------------------------------------------
#-Supporting Functions
#------------------------------------------------------------------------------




def findDraftDir():
    '''finds the mod_Draft dir as for default path'''
    slate = mod_StudioLoad.LoadSlate()
    path_draft = os.path.join(os.getenv('KU_PKG_PATH'), '_pkg_KuFunc/').replace('\\', '/')

    return path_draft


def listFiles(dirpath):
    '''list files in the given dir'''

    path_draft = dirpath.replace('\\', '/')
    ls_files = [p for p in os.listdir(path_draft) if p.startswith('upt_') or p.startswith('dft_')]

    return ls_files




#------------------------------------------------------------------------------
#-Main Functions
#------------------------------------------------------------------------------




class Core_TestFlight(QtWidgets.QWidget):
    def __init__(self):
        super(Core_TestFlight, self).__init__()

        self.title = QtWidgets.QLabel("<h3>Test Flight</h3>")
        self.title.setAlignment(QtCore.Qt.AlignTop)
        self.title_path = QtWidgets.QLabel("path to files")
        self.path = QtWidgets.QLineEdit()
        self.path.setMinimumWidth(500)
        self.browse = QtWidgets.QPushButton("Browse")
        self.browse.clicked.connect(self.browseDir)
        self.title_file = QtWidgets.QLabel("file to test")
        self.file = QtWidgets.QComboBox()
        self.title_func = QtWidgets.QLabel("function to call")
        self.func = QtWidgets.QLineEdit()
        self.test = QtWidgets.QPushButton('Test')
        self.test.clicked.connect(self.takeoff)

        self.master_layout = QtWidgets.QVBoxLayout()

        self.file_layout = QtWidgets.QGridLayout()
        self.file_layout.addWidget(self.title_path, 1, 0)
        self.file_layout.addWidget(self.path, 1, 1)
        self.file_layout.addWidget(self.browse, 1, 2)
        self.file_layout.addWidget(self.title_file, 2, 0)
        self.file_layout.addWidget(self.file, 2, 1)
        # self.file_layout.addWidget(self.title_func, 3, 0)
        # self.file_layout.addWidget(self.func, 3, 1)

        self.master_layout.addWidget(self.title)
        self.master_layout.addLayout(self.file_layout)
        self.master_layout.addSpacing(10)
        self.master_layout.addWidget(self.test)
        self.master_layout.addStretch(1)

        self.setLayout(self.master_layout)
        self.setDefault()
        self.setWindowTitle("Test Flight (beta)")

    def setDefault(self):
        '''set default value when instancing'''

        self.path.setText(findDraftDir())
        self.file.addItems(listFiles(self.path.text()))

    def run(self):
        '''run panel instance'''
        self.show()

    def takeoff(self):
        debug_path = self.path.text()
        debug_file = self.file.currentText()
        debug_func = self.func.text()
        debug_mod = debug_file.replace('.py', '')
        if debug_path and debug_file:
            if not debug_path in sys.path:
                sys.path.append(debug_path)
            m=importlib.import_module(debug_mod)
            reload(m)

        else:
            nuke.message("Fail to load file")

    def browseDir(self):
        '''open file browser for draft module location'''

        dir_browse = nuke.getFilename("Pick direcory for modules",
                                      pattern='*/', default=self.path.text())
        if dir_browse:
            self.path.setText(dir_browse)
            self.file.clear()
            self.file.addItems(listFiles(dir_browse))
        else:
            self.path
        self.raise_()



nukescripts.registerWidgetAsPanel('mod_TestFlight.Core_TestFlight', 'Test Flight (beta)', 'kp.mod_TestFlight')


'''
try:
    app = QtWidgets.QApplication(sys.argv)
    TestFlight = Core_TestFlight()
    TestFlight.run()
    app.exec_()
except:
    TestFlight = Core_TestFlight()
    TestFlight.run()
'''
