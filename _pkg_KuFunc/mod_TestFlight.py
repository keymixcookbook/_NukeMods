'''

nukescript panel for testing modules

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import platform
import os
import sys
import nukescripts
import nuke
import json
from Qt import QtWidgets, QtGui, QtCore
import mod_StudioLoad
import re
from kputl import joinPath




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '3.1'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "TestFlight v%s" % __VERSION__



def _version_():
	ver = '''

	version 3.1
	- add reload button
	- filter out `.pyc` files

	version 3.0
	- change core function to compile()
	- adding option to call a function on execute

	version 2.0
	- save a log with recent test and auto load on start

	version 1.0
	- nukescript panel for testing modules

	'''
	return ver




#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




USER_NUKE = joinPath(os.getenv('HOME'),'.nuke/')
LOG_FILE = joinPath(USER_NUKE, 'TestFlight_log.json')




#-------------------------------------------------------------------------------
#-Core Class
#-------------------------------------------------------------------------------




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
		self.test = QtWidgets.QPushButton('Take Off')
		self.test.clicked.connect(self.onTakeoff)
		self.reload = QtWidgets.QPushButton('Reload')
		self.reload.clicked.connect(self.onReload)
		self.reload.setMaximumWidth(100)

		self.master_layout = QtWidgets.QVBoxLayout()

		self.file_layout = QtWidgets.QGridLayout()
		self.file_layout.addWidget(self.title_path, 1, 0)
		self.file_layout.addWidget(self.path, 1, 1)
		self.file_layout.addWidget(self.browse, 1, 2)
		self.file_layout.addWidget(self.title_file, 2, 0)
		self.file_layout.addWidget(self.file, 2, 1)
		self.file_layout.addWidget(self.title_func, 3, 0)
		self.file_layout.addWidget(self.func, 3, 1)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.setContentsMargins(0,0,0,0)
		self.button_layout.addWidget(self.test)
		self.button_layout.addWidget(self.reload)

		self.master_layout.addWidget(self.title)
		self.master_layout.addLayout(self.file_layout)
		self.master_layout.addSpacing(10)
		self.master_layout.addLayout(self.button_layout)
		self.master_layout.addStretch(1)

		self.setLayout(self.master_layout)
		self.setWindowTitle(__TITLE__)
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
			_recent = [USER_NUKE, "", "()"]
			with open(LOG_FILE,'w') as f:
				f.write(json.dumps(_recent))
			self.path.setText(findDraftDir())
			self.file.clear()
			self.file.addItems(listFiles(self.path.text()))

	def run(self):
		'''run panel instance'''
		self.show()

	def onTakeoff(self):
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
	
	def onReload(self):
		debug_path = self.path.text()
		debug_file = self.file.currentText()
		debug_func = self.func.text()

		if debug_path and debug_file:
			exec( "import {f}\nreload({f})".format(f=debug_file.split('.')[0]) )
		else:
			nuke.message("Fail to load file")

		self.save_log()

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
		# print(ls_func)


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
	ls_files = [p for p in os.listdir(path_draft) if p.startswith('upt_') or p.startswith('mod_') or p.startswith('dft_')]
	ls_files = [f for f in ls_files if f.endswith('.py')]

	return ls_files





#-------------------------------------------------------------------------------
#-Register
#-------------------------------------------------------------------------------





nukescripts.registerWidgetAsPanel('mod_TestFlight.Core_TestFlight', __TITLE__, 'kp.mod_TestFlight')

# if 'upt_' in __file__:
#     app = QtWidgets.QApplication(sys.argv)
#     TestFlight = Core_TestFlight()
#     TestFlight.run()
#     app.exec_()
# else:
# TestFlight = Core_TestFlight()
# TestFlight.run()
