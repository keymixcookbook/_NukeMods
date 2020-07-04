'''
nuke panel widget for testing modules with a click of button
buit for ones whom use external IDE, saves time to copy and paste to nuke script editor

@TianlunJiang2020
https://www.linkedin.com/in/tianlunjiang/
https://github.com/tianlunjiang
'''




import os
import sys
import nukescripts
import nuke
import json
from Qt import QtWidgets, QtGui, QtCore
import re


def joinPath(*paths):
    '''joining path to fix windows and OSX symlink to '/' uniformly'''
    try:
        p = os.path.join(*paths).replace('\\', '/')
        return p
    except ValueError:
        pass


def _version_():
    ver = '''

    version 0.0
	- nukescript panel for testing modules

    version 1.0
    - save a log with recent test and auto load on start

    version 2.0
    - change core function to compile()
    - adding option to call a function on execute

	'''
    return ver



#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




USER_NUKE = joinPath(os.getenv('HOME'),'.nuke/')
LOG_FILE = joinPath(USER_NUKE, 'TestFlight_log.json')




#------------------------------------------------------------------------------
#-Supporting Functions
#------------------------------------------------------------------------------




def listFiles(dirpath):
    '''list files in the given dir'''

    path_draft = dirpath.replace('\\', '/')
    ls_files = [p for p in os.listdir(path_draft) if p.endswith('.py')]

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
        self.path.editingFinished.connect(self.onPathChanged)
        self.browse = QtWidgets.QPushButton("Browse")
        self.browse.clicked.connect(self.browseDir)
        self.title_file = QtWidgets.QLabel("file to test")
        self.file = QtWidgets.QComboBox()
        self.file.currentIndexChanged.connect(self.onFileChanged)
        self.title_func = QtWidgets.QLabel("function to call")
        self.func = QtWidgets.QLineEdit()
        self.func.setPlaceholderText("a single-line expression to evaluate. ie. 'foo()' or 'print foo()'")
        self.func.setToolTip("a single-line expression to evaluate")
        self.func.editingFinished.connect(self.make_callable)
        self.test = QtWidgets.QPushButton('Test')
        self.test.clicked.connect(self.takeoff)

        self.master_layout = QtWidgets.QVBoxLayout()

        self.file_layout = QtWidgets.QGridLayout()
        self.file_layout.addWidget(self.title_path, 1, 0)
        self.file_layout.addWidget(self.path, 1, 1)
        self.file_layout.addWidget(self.browse, 1, 2)
        self.file_layout.addWidget(self.title_file, 2, 0)
        self.file_layout.addWidget(self.file, 2, 1)
        self.file_layout.addWidget(self.title_func, 3, 0)
        self.file_layout.addWidget(self.func, 3, 1)

        self.master_layout.addWidget(self.title)
        self.master_layout.addLayout(self.file_layout)
        self.master_layout.addSpacing(10)
        self.master_layout.addWidget(self.test)
        self.master_layout.addStretch(1)

        self.setLayout(self.master_layout)
        self.setWindowTitle("Test Flight v2.0")
        self.setDefault()

    def setDefault(self):
        '''set default value when instancing'''
        self.read_log()

    def onPathChanged(self):
        '''when path to files is edited'''
        self.file.clear()
        self.file.addItems(listFiles(self.path.text()))

    def onFileChanged(self):
        '''when file combobox is changed'''
        self.set_funcCompleter(self.get_lsFunc())

    def make_callable(self):
        '''adding () to end of the string'''
        _t = self.func.text()
        if len(_t)>0 and '()' not in _t:
            self.func.blockSignals(True)
            self.func.setText(_t+'()')
            self.func.setCursorPosition(len(_t))
            self.func.blockSignals(False)

    def save_log(self):
        '''save latest test log as JSON file'''
        _path = self.path.text()
        _file = self.file.currentText()
        _func = self.func.text()

        _recent = [_path, _file, _func]
        with open(LOG_FILE,'w') as f:
            f.write(json.dumps(_recent))

    def read_log(self):
        '''read latest test log'''
        if os.path.isfile(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                _recent = json.load(f)
                self.path.setText(_recent[0])
                self.file.clear()
                self.file.addItems(listFiles(self.path.text()))
                self.file.setCurrentIndex(self.file.findText(_recent[1]))
                self.func.setText(_recent[2])
        else:
            _recent = [USER_NUKE, "", "foo()"]
            with open(LOG_FILE,'w') as f:
                f.write(json.dumps(_recent))
            self.path.setText(USER_NUKE)
            self.file.clear()
            self.file.addItems(listFiles(self.path.text()))

    def run(self):
        '''run panel instance'''
        self.show()

    def takeoff(self):
        debug_path = self.path.text()
        debug_file = self.file.currentText()
        debug_func = self.func.text()

        if debug_path and debug_file:
            pyString = open(joinPath(debug_path,debug_file), 'r').read()
            callFunc = '\n'+ debug_func
            pyString += callFunc
            compiled = compile(pyString, '<string>', 'exec')
            exec(compiled, globals())
            self.save_log()
        else:
            nuke.message("Fail to load file")

    def get_lsFunc(self):
        '''get functions defined in the file
        return: list of functions, (list)
        '''

        debug_path = self.path.text()
        debug_file = self.file.currentText()
        f = joinPath(debug_path, debug_file)

        ls_func = []
        try:
            with open(f, 'r') as pyString:
                for l in pyString:
                    if l.strip().endswith('():') and re.search('def\s', l):
                        l=l.strip('def ')
                        l=l.replace(':\n', '')
                        ls_func.append(l)
        except: pass
        return ls_func

    def set_funcCompleter(self, ls_func):
        '''sets the function completer
        @ls_func: list of functions to set completer with (list)
        '''
        _thisCompleter = QtWidgets.QCompleter(ls_func)
        self.func.setCompleter(_thisCompleter)
        self.func.setToolTip("list of suggested functions:\n\n- "+'\n- '.join(ls_func))

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




nukescripts.registerWidgetAsPanel('mod_TestFlight.Core_TestFlight', 'Test Flight v1.0', 'kp.mod_TestFlight')
