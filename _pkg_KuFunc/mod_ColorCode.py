'''

Add Color code to backdrops

'''




# ------------------------------------------------------------------------------
# Import Modules
# ------------------------------------------------------------------------------




import nuke, nukescripts
import random
import platform
from kputl import hsv2rgb, nukeColor
from Qt import QtWidgets, QtGui, QtCore




# ------------------------------------------------------------------------------
# Header
# ------------------------------------------------------------------------------




__VERSION__		= '3.0'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "ColorCode v%s" % __VERSION__



def _version_():
	ver='''

	version 3.0
	- move colorcode button to prompted UI
	- switch UI to Qt

	version 2.1
	- replace html tag for note_font_size with integer number

	version 2.0
	- more Color options (Random)
	- Header Size options

	version 1.1
	- Fixing error when cancel nuke panel
	- Fixing Default value of backdrop label
	- Output -> Transform

	version 1.0
	- Inherit nukescripts.autobackdrop()
	- Adding Color Scheme selection buttons for groups:
	- Groups include: CG, Plate, Grade, Key, Despill, Output, 2D Elem, Ref, End Comp, Precomp

	'''
	return ver




# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------



BLK = '&#9608;'

# Type: [font, tile, button]
HEX_GROUP = {
			'CG': 			['CCC0C0', '5C3737', '7D5F5F'],
			'Key/Roto': 	['C2CCC0', '3E5C37', '657d5f'],
			'Precomp': 		['CAC0CC', '55375C', '775f7d'],
			'EndComp': 		['CCCCCC', '5C5C5C', '7D7D7D'],
			'LensFX': 		['C2C0CC', '3E375C', '655f7d'],
			'Transform': 	['CCC7C0', '5C4625', '7D6B51'],
			'Despill': 		['C0CCC5', '2E5C40', '587d66'],
			'Grade': 		['C0CCCC', '2E5C5C', '587d7d'],
			'Elem2D': 		['CACCC0', '535C2E', '757d58'],
			'Plate': 		['BFC5CC', '2E405C', '58667d'],
			'*Random': 		[]
			}
HEADER_FONT_SIZE = {'h1': 200, 'h2': 96, 'h3': 48}




# ------------------------------------------------------------------------------
# Core Class
# ------------------------------------------------------------------------------




class Core_ColorCode(QtWidgets.QWidget):
	def __init__(self):
		super(Core_ColorCode, self).__init__()

		self.MODE = 0 # 0:Create New Backdrop; 1: Edit Selected Backdrop

		self.title = QtWidgets.QLabel("<h3>%s</h3>" % __TITLE__)
		self.label_mode = QtWidgets.QLabel("Create New Backdrop")
		self.colors = QtWidgets.QComboBox()
		self.model = self.colors.model()
		self.headers = QtWidgets.QComboBox()
		self.headers.addItems(sorted(HEADER_FONT_SIZE.keys()))
		# self.headers.addItems(sorted(HEADER_FONT_SIZE.keys(), reverse=True))
		self.headers.setMaximumWidth(48)
		self.center = QtWidgets.QCheckBox("Center Label")
		self.label = QtWidgets.QLineEdit()
		self.label.returnPressed.connect(self.setColorCode)
		self.label.setPlaceholderText("Label for Backdrop")
		self.btn_set = QtWidgets.QPushButton("ColorCode It")
		self.btn_set.clicked.connect(self.setColorCode)

		# Add Pixmap for combobox dropdown list
		# Source: https://stackoverflow.com/questions/22887496/pyqt-how-to-customize-qcombobox-item-appearance
		for r in sorted(HEX_GROUP.keys()):
			if r != '*Random':
				item = QtGui.QStandardItem(r)
				thisColor = ('#%s' % HEX_GROUP[r][1])
				thisPixmap = QtGui.QPixmap(26,26)
				thisPixmap.fill(thisColor)
				item.setData(QtGui.QIcon(thisPixmap), QtCore.Qt.DecorationRole)
				self.model.appendRow(item)

		rand_item = QtGui.QStandardItem('*Random')
		rand_thisPixmap = QtGui.QPixmap(26,26)
		rand_thisPixmap.fill("#222")
		rand_item.setData(QtGui.QIcon(rand_thisPixmap), QtCore.Qt.DecorationRole)
		self.model.appendRow(rand_item)



		self.layout_master = QtWidgets.QVBoxLayout()
		self.layout_options = QtWidgets.QHBoxLayout()
		self.setLayout(self.layout_master)

		self.layout_options.addWidget(self.colors)
		self.layout_options.addWidget(self.headers)
		self.layout_options.addWidget(self.center)

		self.layout_master.addWidget(self.title)
		self.layout_master.addWidget(self.label_mode)
		self.layout_master.addLayout(self.layout_options)
		self.layout_master.addWidget(self.label)
		self.layout_master.addWidget(self.btn_set)

		# Set Taborder
		self.setTabOrder(self.colors, self.label)
		self.setTabOrder(self.label, self.btn_set)

		# self.setFixedWidth(150)
		self.setWindowTitle(__TITLE__)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

	def setColorCode(self):
		"""when button is pressed and to set color code"""

		color_key = self.colors.currentText()
		
		if color_key != '*Random':
			color_font, color_tile, _  = HEX_GROUP[color_key]
		else:
			rand_r, rand_g, rand_b, rand_h = randomColour()
			color_tile = nukeColor(rand_r, rand_g, rand_b)
			color_font = nukeColor(*list(hsv2rgb(rand_h,1,0.18)))

		
		header_size = HEADER_FONT_SIZE[self.headers.currentText()]
		label = self.label.text() if self.center.checkState() != QtCore.Qt.Checked else ('<center>%s' % self.label.text())

		if self.MODE == 0:
			bounds = get_backdrop_size(self.nodes_sel)
			backdrop_new = create_backdrop(
							bounds, color_font, color_tile, header_size, self.nodes_sel
							)
			backdrop_new['label'].setValue(label)
					
		elif self.MODE == 1:
			backdrop_edit = nuke.selectedNode()

			backdrop_edit['tile_color'].setValue(hex2int(color_tile))
			backdrop_edit['note_font_color'].setValue(hex2int(color_font))
			backdrop_edit['note_font_size'].setValue(header_size)

		self.close()

	def run(self):
		"""main run method"""

		self.nodes_sel = nuke.selectedNodes()
		nodes_classes = [n.Class() for n in self.nodes_sel]

		if len(self.nodes_sel)>0:
			
			# When a group of nodes are selected
			if len(self.nodes_sel) > 1:
				self.MODE = self.set_mode_new()
				most_class = max(set(nodes_classes), key=nodes_classes.count)
				self.label.setText(most_class)

			# When only a backdrop node is selected
			elif len(self.nodes_sel) == 1 and self.nodes_sel[0].Class() == "BackdropNode":
				
				self.MODE = self.set_mode_edit()
				_thisLabel = self.nodes_sel[0].knob('label').value()
				if '<center>' in _thisLabel: self.center.setCheckState(QtCore.Qt.Checked)
				else: self.center.setCheckState(QtCore.Qt.Unchecked)
				self.label.setText(_thisLabel.strip('<center>'))

			self.show()
			self.raise_()
			self.colors.setFocus()
			self.label.selectAll()
			centerWindow(self)

		else:
			self.MODE = 0
			nuke.message("No Nodes selected")

	def set_mode_new(self):
		"""set mode create new backdrop and change label"""
		self.label_mode.setText("Create New Backdrop")
		self.label.setEnabled(True)
		self.center.setEnabled(True)
		print(self.label_mode.text())
		return 0

	def set_mode_edit(self):
		"""set mode edit new backdrop and change label"""
		self.label_mode.setText("Edit Selected Backdrop")
		self.label.setEnabled(False)
		self.center.setEnabled(False)
		print(self.label_mode.text())
		return 1




# ------------------------------------------------------------------------------
# Supporting Functions
# ------------------------------------------------------------------------------




def get_backdrop_size(nodes_sel):
	"""get the XYWH of backdrop nodes based on given nodes
	@nodes_sel: (list of obj) list of selected Nodes
	return: (list of int) [bdX, bdY, bdW, bdH]
	"""

	# Calculate bounds for the backdrop node.
	bdX = min([node.xpos() for node in nodes_sel])
	bdY = min([node.ypos() for node in nodes_sel])
	bdW = max([node.xpos() + node.screenWidth() for node in nodes_sel]) - bdX
	bdH = max([node.ypos() + node.screenHeight() for node in nodes_sel]) - bdY
	
	return [bdX, bdY, bdW, bdH]

def create_backdrop(bounds, font_color, tile_color, font_size, nodes_sel):
	'''
	Automatically puts a backdrop behind the selected nodes.

	The backdrop will be just big enough to fit all the select nodes in, with room
	at the top for some text in a large font.

	@bounds: (list of int) XYWH bounds
	@font_color: (str) font color in hex code 
	@font_size: (int) size of the font 
	@tile_color: (str) tile color in hex code
	@tile_color: (list of obj) list of originally selected nodes

	return: (obj) created backdrop object
	'''

	bdX, bdY, bdW, bdH = bounds

	tile_color_to_nuke = hex2int(tile_color) if type(tile_color) == str else int(tile_color)

	zOrder = 0
	selectedBackdropNodes = nuke.selectedNodes( "BackdropNode" )
	nonSelectedBackdropNodes = []
	#if there are backdropNodes selected put the new one immediately behind the farthest one
	if len( selectedBackdropNodes ) :
		zOrder = min( [node.knob( "z_order" ).value() for node in selectedBackdropNodes] ) - 1
	else :
		#otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
		nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
	for nonBackdrop in nodes_sel:
		for backdrop in nonSelectedBackdropNodes:
			if nodeIsInside( nonBackdrop, backdrop ):
				zOrder = max( zOrder, backdrop.knob( "z_order" ).value() + 1 )

	# Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
	left, top, right, bottom = (-80, -148, 80, 74)
	bdX += left
	bdY += top
	bdW += (right - left)
	bdH += (bottom - top)

	n = nuke.nodes.BackdropNode(xpos = bdX,
								bdwidth = bdW,
								ypos = bdY,
								bdheight = bdH,
								note_font='bold',
								note_font_color=hex2int(font_color),
								note_font_size=font_size,
								z_order = zOrder,
								tile_color = tile_color_to_nuke
								)

	# revert to previous selection
	n['selected'].setValue(False)
	for node in nodes_sel:
		node['selected'].setValue(True)

	return n

def nodeIsInside (node, backdropNode):
	"""Returns true if node geometry is inside backdropNode otherwise returns false"""
	topLeftNode = [node.xpos(), node.ypos()]
	topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
	bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
	bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(), backdropNode.ypos() + backdropNode.screenHeight()]

	topLeft = ( topLeftNode[0] >= topLeftBackDrop[0] ) and ( topLeftNode[1] >= topLeftBackDrop[1] )
	bottomRight = ( bottomRightNode[0] <= bottomRightBackdrop[0] ) and ( bottomRightNode[1] <= bottomRightBackdrop[1] )

	return topLeft and bottomRight

def centerWindow(widget):
	"""center widget window to desktop"""
	frameGeo = widget.frameGeometry()
	thisDesktop = QtWidgets.QApplication.desktop()
	screen =thisDesktop.screenNumber(thisDesktop.cursor().pos())
	center =thisDesktop.screenGeometry(screen).center()
	frameGeo.moveCenter(center)
	widget.move(frameGeo.topLeft())

def hex2int(hex):
	"""Convert Hex Code to nuke readable int"""

	return int('%sFF' % hex, 16)

def randomColour(sat=0.25, val=0.36):
	"""generate randome RGB values based given hue and value
	@sat=0.25: (float) saturation value
	@val=0.36: (float) value
	return: (list of int) list of 8-bit rgb values
	"""

	rand_h = random.randrange(0,360,10)
	rand_r, rand_g, rand_b = hsv2rgb(rand_h,sat,val)

	return [rand_r, rand_g, rand_b, rand_h]




# ------------------------------------------------------------------------------
# Instancing
# ------------------------------------------------------------------------------



ColorCode = Core_ColorCode()




