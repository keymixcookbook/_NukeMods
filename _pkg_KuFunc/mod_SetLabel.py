



# ------------------------------------------------------------------------------
# Module Import
# ------------------------------------------------------------------------------




import nuke, nukescripts
import platform
from Qt import QtWidgets, QtGui, QtCore




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__='1.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__WEBSITE__="jiangovfx.com"
__COPYRIGHT__="copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__=__name__.split('_')[1].split('.')[0]


def _version_():
	ver="""

	version 2.0
	- Add preset buttons for frames and knob values

	version 1.0
	- adding multiline support
	- adding group node context

	version 0:
	- Basically working, when run(), prompt a frameless popup with line edit field

	version 0.1:
	- replace with Qt


	"""




# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------




KNOB_IGNORE = set(['layer', 'invert_mask', 'help', 
					'dope_sheet', 'hide_input', 'xpos',
					'crop', 'channels', 'note_font_color',
					'onCreate', 'quality', 'updateUI',
					'knobChanged', 'note_font', 'tile_color',
					'bookmark', 'selected', 'autolabel',
					'process_mask', 'label', 'onDestroy',
					'inject', 'indicators', 'icon',
					'channel', 'maskFrom', 'maskChannelMask',
					'enable', 'maskChannelInput', 'Mask',
					'ypos', 'postage_stamp_frame', 'postage_stamp',
					'lifetimeStart', 'maskChannel', 'panel',
					'lifetimeEnd', 'maskFromFlag',
					'name', 'cached', 'fringe',
					'mask', 'note_font_size', 'filter', 
					'useLifetime', 'gl_color'])

KNOB_IGNORE_KEYWORDS = ['_panelDropped', 'enable', 'unpremult', 'clamp']



# ------------------------------------------------------------------------------
# Core Class
# ------------------------------------------------------------------------------




class Core_SetLabel(QtWidgets.QDialog):
	def __init__(self):
		super(Core_SetLabel,self).__init__()

		self.lineInput = QtWidgets.QLineEdit()
		self.lineInput.setAlignment(QtCore.Qt.AlignCenter)
		self.lineInput.returnPressed.connect(self.onPressed)
		self.title = QtWidgets.QLabel("<b>Set Label</b>")
		self.title.setAlignment(QtCore.Qt.AlignHCenter)
		self.btn_frame = QtWidgets.QPushButton("Current Frame")
		self.btn_frame.clicked.connect(self.onPreset)
		self.knoblist = QtWidgets.QComboBox()
		self.knoblist.setEditable(True)
		self.btn_knob = QtWidgets.QPushButton("Knob Value")
		self.btn_knob.clicked.connect(self.onPreset)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout_knobs = QtWidgets.QHBoxLayout()
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.lineInput)
		self.layout.addWidget(self.btn_frame)
		self.layout_knobs.addWidget(self.knoblist)
		self.layout_knobs.addWidget(self.btn_knob)

		self.layout.addLayout(self.layout_knobs)
		self.setLayout(self.layout)
		self.resize(200,50)
		self.setWindowTitle("Set Label")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()

	def onPressed(self):
		"""change label with enter-key is pressed"""
		newLabel = self.lineInput.text()
		for n in nuke.selectedNodes():
			n['label'].setValue(newLabel)
		self.close()

	def onPreset(self):
		"""When preset button is pressed"""
		_sender = self.sender()

		if _sender is self.btn_frame:
			for n in nuke.selectedNodes():
				n['label'].setValue('x%s' % nuke.frame())
		elif _sender is self.btn_knob:
			sel_knob = self.knoblist.currentText()
			n = nuke.selectedNode()
			n['label'].setValue('[value %s]' % sel_knob)

		self.close()

	def setDefault(self):
		"""get the existing label of selected nodes"""
		sel_nodes = nuke.selectedNodes()
		if sel_nodes:
			self.lineInput.show()
			self.title.setText("<b>Set Label</b>")
			self.lineInput.setText(sel_nodes[0]['label'].value())

			n = sel_nodes[0]
			knobs = filterKnobs(n.knobs())

			self.knoblist.clear()
			self.knoblist.addItems(knobs)
		else:
			self.lineInput.hide()
			self.title.setText("<b>Errpr:<br>No Node Selected</b>")

	def run(self):
		"""rerun instance"""
		self.setDefault()
		self.move(QtGui.QCursor.pos()+QtCore.QPoint(-100,-12))
		self.raise_()
		self.lineInput.setFocus()
		self.lineInput.selectAll()
		self.show()




# ------------------------------------------------------------------------------
# Supporting Fucntions
# ------------------------------------------------------------------------------




def filterKnobs(knobs):
	"""filter knobs for labels
	@knobs: (list) list of knobs
	return: (list) filtered list of knobs
	"""
	ls_ignored = list( set(knobs)-KNOB_IGNORE )
	ls_filtered = []

	for k in ls_ignored:
		count = 0
		for f in KNOB_IGNORE_KEYWORDS:
			if f not in k: count += 1
		if count == len(KNOB_IGNORE_KEYWORDS): ls_filtered.append(k)

	return sorted(ls_filtered)





# ------------------------------------------------------------------------------
# Instancing
# ------------------------------------------------------------------------------




SetLabel = Core_SetLabel()
