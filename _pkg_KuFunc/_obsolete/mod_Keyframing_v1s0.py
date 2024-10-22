'''

sets keyframes in one go for a knob

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts
from Qt import QtWidgets, QtGui, QtCore
import platform, os




#-------------------------------------------------------------------------------
#-Header
#-------------------------------------------------------------------------------




__VERSION__		= '1.0'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "Keyframing v%s" % __VERSION__


def _version_():
	ver='''

	version 1.0
	- sets keyframes in one go for a knob

	'''
	return ver




#-------------------------------------------------------------------------------
#-Core Class
#-------------------------------------------------------------------------------




class Core_Keyframing(QtWidgets.QWidget):
	def __init__(self):
		super(Core_Keyframing, self).__init__()

		# Widgets
		self.node_name = QtWidgets.QLabel("Node1")
		self.node_name.setStyleSheet("font: bold")
		self.knob_pick_label = QtWidgets.QLabel("knob")
		self.knob_pick = QtWidgets.QComboBox()
		self.knob_pick.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
		self.knob_pick.sizePolicy().setHorizontalStretch(0)
		self.knob_pick.setEditable(True)
		self.keylist = QtWidgets.QTableWidget()
		self.keylist_btn = RowEditingButtons()
		self.btn_set = QtWidgets.QPushButton('Set Keyframes')

		# Signals
		self.keylist_btn.add.clicked.connect(self.edit_row)
		self.keylist_btn.remove.clicked.connect(self.edit_row)
		self.btn_set.clicked.connect(self.set_keyframes)

		# Layout
		self.layout_master = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout_master)

		self.layout_node = QtWidgets.QHBoxLayout()
		self.layout_keylist = QtWidgets.QVBoxLayout()
		self.layout_keylist.setContentsMargins(0,0,0,0)

		self.layout_node.addWidget(self.node_name)
		# self.layout_node.addSpacing(24)
		self.layout_node.addWidget(self.knob_pick_label)
		self.layout_node.addWidget(self.knob_pick)
		# self.layout_node.addStretch()
		self.layout_keylist.addWidget(self.keylist)
		self.layout_keylist.addWidget(self.keylist_btn)

		self.layout_master.addLayout(self.layout_node)
		self.layout_master.addSpacing(24)
		self.layout_master.addLayout(self.layout_keylist)
		self.layout_master.addWidget(self.btn_set)

		# Widget attributes
		self.setWindowTitle(__TITLE__+' v'+__VERSION__)

		self.setDefault()

	def setDefault(self):
		'''set default value when instancing'''

		self.keylist.setColumnCount(2)
		self.keylist.setHorizontalHeaderLabels(['frame', 'values'])
		self.keylist.setRowCount(4)
		self.keylist.horizontalHeader().setStretchLastSection(True)
		self.keylist.setAlternatingRowColors(True)
	
	def run(self):
		'''run panel instance'''

		if nuke.selectedNode():
			
			node_name = nuke.selectedNode().name()
			self.node_name.setText(node_name)

			self.knob_pick.clear()
			self.knob_pick.addItems(getKeyableKnobs(nuke.toNode(node_name)))
			self.keylist.clear()
			self.keylist.setItem(0,0, QtWidgets.QTableWidgetItem(str(nuke.frame())))
			# self.get_existingKeys()
			centerWindow(self)
			self.show()
			self.raise_()
	
	def get_keylist(self):
		'''get the frame/value pair
		return: (dict) {frame: value}
		'''

		_keyframes = {}
		_table = self.keylist
		_row = _table.rowCount()

		for r in range(_row):
			if _table.item(r, 0):
				_curFrame = _table.item(r, 0).text()
				_curValue = _table.item(r, 1).text()
				_keyframes[_curFrame]=_curValue

		print(_keyframes)
		return _keyframes

	def get_existingKeys(self):
		'''get the exist keyframes and sets keylist on run
        (currently for debuging process)
        '''

		# node = nuke.toNode(self.node_name.text())
		# knob = node.knob(self.knob_pick.currentText())

		_list = {1001: 45, 1002: 86, 1005: 120, 1021: 45}
		_table = self.keylist
		_table.clearContents()
		_table.setRowCount(0)
		_table.setRowCount(len(_list.keys()))

		for r, f in enumerate(_list.keys()):
			print r, f, _list[f]
			_curFrameItem = QtWidgets.QTableWidgetItem(str(f))
			_curValueItem = QtWidgets.QTableWidgetItem(str(_list[f]))
			_table.setItem(r, 0,_curFrameItem)
			_table.setItem(r, 1,_curValueItem)

	def set_keyframes(self):
		'''set keyframes in nuke'''

		node = nuke.toNode(self.node_name.text())
		knob = node.knob(self.knob_pick.currentText())


		print("set keyframes for %s.%s" % (node.name(), knob.name()))

		_keyframes = self.get_keylist()
		for k in _keyframes.keys():
			_thisValue = eval(_keyframes[k])
			knob.setAnimated()
			knob.setValueAt(_thisValue ,int(k))
			print('%s - %s' % (k, _thisValue))

		self.close()

	def edit_row(self):
		'''add remove rows'''
		_sender = self.sender()
		_table = self.keylist

		if _sender is self.keylist_btn.add:
			_table.setRowCount(_table.rowCount()+1)
		elif _sender is self.keylist_btn.remove:
			_table.setRowCount(_table.rowCount()-1)
	




#------------------------------------------------------------------------------
#-Supporting Class
#------------------------------------------------------------------------------



class RowEditingButtons(QtWidgets.QWidget):
	def __init__(self):
		super(RowEditingButtons, self).__init__()

		self.add = QtWidgets.QPushButton('+')
		self.remove = QtWidgets.QPushButton('-')

		self.layout = QtWidgets.QHBoxLayout()
		self.setLayout(self.layout)
		self.layout.setContentsMargins(0,0,0,0)
		self.layout.addWidget(self.add)
		self.layout.addWidget(self.remove)




#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------




def getKeyableKnobs(n):
	'''get the keyable knobs from a node
	n: (obj) node object
	return: (list) list of keyable knobs
	'''
	_knobs_all =set([k for k in n.knobs()])
	_knobs_remove = set(['layer', 'invert_mask', 'help', 'dope_sheet', 'hide_input', 'xpos', 'crop', 'channels', 'note_font_color', 'onCreate', 'quality', 'updateUI', 'knobChanged', 'note_font', 'tile_color', 'bookmark', 'selected', 'autolabel', 'process_mask', 'label', 'onDestroy', 'inject', 'indicators', 'icon', 'channel', 'maskFrom', 'maskChannelMask', 'enable', 'maskChannelInput', 'Mask', 'ypos', 'postage_stamp_frame', 'postage_stamp', 'lifetimeStart', 'maskChannel', 'panel', 'lifetimeEnd', 'maskFromFlag', 'name', 'cached', 'fringe', 'mask', 'note_font_size', 'filter', 'useLifetime', 'gl_color']) 
	_knobs_filter = ['_panelDropped', 'enable', 'unpremult', 'clamp']
	_knobs_filtered = sorted(list(_knobs_all - _knobs_remove), reverse=True)

	for f in _knobs_filter:
		for k in _knobs_filtered:
			if f in k:
				_knobs_filtered.remove(k)

	return _knobs_filtered


def centerWindow(widget):
    frameGeo = widget.frameGeometry()
    thisDesktop = QtWidgets.QApplication.desktop()
    screen =thisDesktop.screenNumber(thisDesktop.cursor().pos())
    center =thisDesktop.screenGeometry(screen).center()
    frameGeo.moveCenter(center)
    widget.move(frameGeo.topLeft())



#-------------------------------------------------------------------------------
#-Instancing
#-------------------------------------------------------------------------------




Keyframing = Core_Keyframing()
