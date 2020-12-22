'''

Simple floating panel to create nodes

'''


import platform


__VERSION__='1.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__COPYRIGHT__="copyright %s" % __AUTHOR__

__TITLE__=__file__.split('_')[1].split('.')[0]


def _version_():
	ver='''

	version 1.0
	- UI Panel to quickly create often used nodes

	'''
	return ver




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts
from Qt import QtWidgets, QtGui, QtCore 



#-------------------------------------------------------------------------------
#-DATA
#-------------------------------------------------------------------------------



# 'label': ['nodeclass', 'nodename', 'knob value']
NODES = {
	'Union': ['ChannelMerge','AlphaMerge', 'operation union'],
	'Stencil': ['ChannelMerge','AlphaMerge', 'operation stencil'],
	'Mask': ['ChannelMerge','AlphaMerge', 'operation mask'],
	'Max': ['ChannelMerge','AlphaMerge', 'operation max'],
	'Keymix': ['Keymix','AlphaKeymix', 'channels alpha'],
	'Grade': ['Grade','AlphaGrade', 'channels alpha'],
	'Curve': ['ColorLookup','AlphaCurve', 'channels alpha']
	}

TITLE = "QuickNode v%s" % __VERSION__

AUTOLABEL = "nuke.thisNode().name() + '\\n' +'('+nuke.thisNode()['%s'].value()+')'"




#-------------------------------------------------------------------------------
#-Core Class
#-------------------------------------------------------------------------------




class Core_QuickNode(QtWidgets.QWidget):
	def __init__(self):
		super(Core_QuickNode, self).__init__()

		self.title = QtWidgets.QLabel(TITLE)
		
		self.tab0 = QtWidgets.QTabWidget()
		self.tab_layout = QtWidgets.QVBoxLayout()
		self.tab_widget = QtWidgets.QWidget()
		self.tab_widget.setLayout(self.tab_layout)
		
		self.layout = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout)

		self.tab0.addTab(self.tab_widget, 'Alpha Ops')

		self.layout.addWidget(self.title)
		self.layout.addWidget(self.tab0)

		for k in NODES:
			exec("self.bt_%s=QtWidgets.QPushButton('%s')" % (k,k))
			exec("self.bt_%s.clicked.connect(self.createNode)" % (k))
			exec("self.tab_layout.addWidget(self.bt_%s)" % (k))

		self.setWindowTitle(TITLE)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()

	def setDefault(self):
		'''set default value when instancing'''

	def createNode(self):
		'''create the node when button pushed'''
		bt = self.sender().text()
		thisKey = NODES[bt]
		thisKnob = NODES[bt][2].split(' ')
		
		thisNode = nuke.createNode(thisKey[0], inpanel=False)
		thisNode.setName(thisKey[1])
		thisNode[thisKnob[0]].setValue(thisKnob[1])
		thisNode['note_font'].setValue('bold')
		thisNode['note_font_color'].setValue(4294967295)

		if thisKey[0] == 'ChannelMerge':
			thisNode['autolabel'].setValue(AUTOLABEL % 'operation')
		if thisKey[0] == 'ColorLookup':
			for c in ['master', 'red', 'green', 'blue']:
				thisNode['lut'].delCurve(c)
			thisNode['lut'].fromScript('alpha {curve C 0 x0.5 0.5 x1 1}')

		self.close()


	def run(self):
		'''run panel instance'''
		self.move(QtGui.QCursor.pos()-QtCore.QPoint(self.frameGeometry().width()/2,self.frameGeometry().height()/2))
		self.show()






#-------------------------------------------------------------------------------
#-Instancing
#-------------------------------------------------------------------------------




QuickNode = Core_QuickNode()