'''

UI for quick expression entries

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import platform
import os
from Qt import QtWidgets, QtGui, QtCore
import nuke, nukescripts
import re




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '1.3'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "ExprPrompt v%s" % __VERSION__



def _version_():
	ver='''
	
	version 1.3
	- Restructure code
	- fix connection prob when edit the node
	- add AOV Mask preset
	- '$ly' sub when getting previous expression

	version 1.2
	- create off branch

	version 1.1
	- add preset buttons and input autocomplet presets
	- add button to cycle channels

	version 1.0
	- Expression node with prompt options
	- string replace keys ('$ly': layer, '$ch': channels)
	- input field completer with layers
	- Create Expression node if non-Expression node selected, auto fill LineEdit if Expression node selected

	'''
	return ver



#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




PRESET_LINE = [
	'max(r,g,b)', 'min(r,g,b)', 'a>0',
	'r', 'g', 'b',
	'r/g', 'r/b', 'g/r', 'g/b', 'b/r', 'b/g',
	'isinf($ch)?$ch(x+1,y):$ch','isnan($ch)?$ch(x-1,y):$ch',
	'$ly.red', '$ly.green', '$ly.blue'
]

PRESET_BTN = {
	'STMap': [
		('expr0','(x+0.5)/width'),
		('expr1','(y+0.5)/height')
		],
	'AOV Mask': [
		('expr3', '<layer>.<channel>'),
		],
	'Raw Lighting': [
		('expr0', 'rgba.red/<albeto>.red'),
		('expr1', 'rgba.green/<albeto>.green'),
		('expr2', 'rgba.blue/<albeto>.blue')
		],
	'Depth Normalize': [
		('channel0', 'depth'),
		('expr0', 'depth.Z==0?0:1/depth.Z')
		]
}

COL = {
	'red': 2130706687,
	'green': 679411967,
	'blue': 4816895
}



#------------------------------------------------------------------------------
#-Core Class
#------------------------------------------------------------------------------




class Core_ExprPrompt(QtWidgets.QWidget):
	def __init__(self):
		super(Core_ExprPrompt, self).__init__()
		# set
		self.ls_layers = PRESET_LINE

		# Left Widgets
		self.title = QtWidgets.QLabel("<h3>%s</h3>" % __TITLE__)
		self.st_expr = QtWidgets.QLineEdit()
		self.st_expr.setPlaceholderText('$ly: layer (Id06), $ch: channel (red)')
		self.st_expr.returnPressed.connect(self.onPressed)
		self.st_expr.textChanged.connect(self.onTextChanged)
		self.layer_box = QtWidgets.QComboBox()
		self.layer_box.setEnabled(False)
		self.ck_ch_r = QtWidgets.QCheckBox('r')
		self.ck_ch_g = QtWidgets.QCheckBox('g')
		self.ck_ch_b = QtWidgets.QCheckBox('b')
		self.ck_ch_a = QtWidgets.QCheckBox('alpha')
		self.bt_ch_all = QtWidgets.QPushButton('all')
		self.bt_ch_all.clicked.connect(self.set_channels)
		self.ck_clamp = QtWidgets.QCheckBox('clamp')
		self.ck_invert = QtWidgets.QCheckBox('invert')
		self.bt_set = QtWidgets.QPushButton('Set!')
		self.bt_set.clicked.connect(self.onPressed)

		# Completer
		self.completer = QtWidgets.QCompleter(self.ls_layers)
		self.completer.setCompletionMode(self.completer.PopupCompletion)
		self.st_expr.setCompleter(self.completer)

		# Right Widgets
		for idx, p in enumerate(PRESET_BTN.keys()):
			exec("self.presetBtn%s=QtWidgets.QPushButton('%s')" % (idx, p))
			exec("self.presetBtn%s.clicked.connect(self.set_preset)" % (idx))

		self.ls_ch_layer = [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_ch_a]
		self.ls_wrapper = [self.ck_clamp, self.ck_invert]

		# define layouts
		self.layout_master = QtWidgets.QHBoxLayout()
		self.layout_main = QtWidgets.QVBoxLayout()
		self.layout_expr = QtWidgets.QHBoxLayout()
		self.preset_group = QtWidgets.QGroupBox('presets:')
		self.layout_right = QtWidgets.QVBoxLayout()
		self.preset_group.setLayout(self.layout_right)
		self.layout_channels = QtWidgets.QHBoxLayout()
		self.layout_wrappers = QtWidgets.QHBoxLayout()
		self.layout_wrappers.setAlignment(QtCore.Qt.AlignLeft)

		# add widgets and set layouts
		for m in [self.st_expr, self.layer_box]:
			self.layout_expr.addWidget(m)
		for c in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b,self.ck_ch_a, self.bt_ch_all]:
			self.layout_channels.addWidget(c)
		for w in [self.ck_clamp, self.ck_invert]:
			self.layout_wrappers.addWidget(w)

		# Main Layout
		self.layout_main.addWidget(self.title)
		self.layout_main.addLayout(self.layout_expr)
		self.layout_main.addLayout(self.layout_channels)
		self.layout_main.addLayout(self.layout_wrappers)
		self.layout_main.addWidget(self.bt_set)

		# Right Layout
		# self.layout_right.addStretch()
		for idx, p in enumerate(PRESET_BTN.keys()):
			eval('self.layout_right.addWidget(self.presetBtn%s)' % idx)
		self.layout_right.addStretch()

		# Master Layout
		self.layout_master.addLayout(self.layout_main)
		self.layout_master.addWidget(self.preset_group)
		self.setLayout(self.layout_master)

		self.setMaximumWidth(400)
		self.layer_box.setMaximumWidth(70)

		self.setWindowTitle(__TITLE__)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()

	def onPressed(self):
		'''when enter-key is pressed on expression line edit'''
		self.set_expr(self.node, self.get_selectedValues())
		self.close()

	def onTextChanged(self):
		'''if string key are in line edit, enable combobox'''
		if '$ly' in self.st_expr.text():
			self.layer_box.setEnabled(True)
		else:
			self.layer_box.setEnabled(False)

	def run(self):
		'''run the instance'''

		self.setDefault()

		node_expr, node_sel = self.get_node()
		self.set_layer_box(node_expr, node_sel)
		ls = PRESET_LINE + self.ls_layers
		self.completer.model().setStringList(ls)
		self.set_prevExpr(node_expr, node_sel)

		self.st_expr.selectAll()
		self.move(QtGui.QCursor.pos())
		self.show()

	def setDefault(self):
		'''set default value when instansing'''
		self.layer_box.clear()
		for k in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_clamp, self.ck_invert]:
			k.setChecked(False)
		self.ck_ch_a.setChecked(True)
		self.st_expr.setFocus()
		self.layer_box.setEditable(False)
		
	def get_node(self):
		'''
		find out the node_sel and node_expr
		return: [node_expr, node_sel] (list of objs)

		nothing selected: node_sel = None, node_expr = New Expression
		one non-Expression selected: node_sel = selected node, node_expr = New Expression
		one Expression selected: node_sel = None, node_expr = selected expression
		'''

		sel = nuke.selectedNodes()
		node_sel, node_expr = None, None

		if len(sel)<=0:
			node_sel = None
			node_expr = nuke.nodes.Expression()
			
		elif len(sel) == 1:
			if sel[0].Class() != 'Expression':
				node_sel = sel[0]
				node_expr = nuke.nodes.Expression()
			elif sel[0].Class() == 'Expression':
				node_sel = None # Expression node doesn't return any layer channels
				node_expr = sel[0]
		
		node_pos = node_under_cursor()
		node_pos = (node_pos[0]-node_expr.screenWidth()/2, node_pos[1]-node_expr.screenHeight()/2)

		if node_sel or len(sel)==0:
			node_expr.setInput(0, node_sel)
			node_expr.setXYpos(*node_pos)

		node_expr['label'].setValue('a::[value expr3]')
		self.node = node_expr

		return [node_expr, node_sel]

	def set_prevExpr(self, node_expr, node_sel):
		'''previously expression, none if nothing selected
		@node_expr: expressions to add (str)
		@node_sel: nodes selected (list of obj)
		return: prevExpr (str)

		nothing selected: node_sel = None, node_expr = New Expression
		one non-Expression selected: node_sel = selected node, node_expr = New Expression
		one Expression selected: node_sel = None, node_expr = selected expression
		'''

		self.prevExpr = None
		
		try:
			if nuke.selectedNode():
				if node_sel == None and nuke.selectedNodes()[0] == node_expr:
					self.prevExpr = node_expr['expr3'].value()
		except:
			pass

		if self.prevExpr: self.st_expr.setText( re.sub('\w+\.', '$ly.', self.prevExpr) )

		return self.prevExpr

	def get_selectedValues(self):
		'''get values for the checkboxs and comboboxs
		return: [sel_layer, sel_channel, sel_wrapper] (list of lists)
		'''
		sel_layer = self.layer_box.currentText() # 'Id06'

		sel_channel, sel_wrapper = [],[]

		for idx,c in enumerate(self.ls_ch_layer):
			if c.isChecked():
				sel_channel.append('expr%s' % idx) # ['expr1', 'expr2']
		for w in self.ls_wrapper:
			if w.isChecked():
				sel_wrapper.append(w.text()) # ['clamp', 'invert']

		return [sel_layer, sel_channel, sel_wrapper]

	def set_expr(self, node, sel):
		'''get string from expression line edit
		@node: node to set expression (obj)
		@sel: values to set expressions with (list of lists)
		'''

		sel_layer, sel_channel, sel_wrapper = sel

		knob_to_ch = {'expr0':'red', 'expr1': 'green', 'expr2': 'blue', 'expr3': 'alpha'}

		expr_in = self.st_expr.text()
		expr_mid = expr_in
		expr_mid = '1-(%s)' % expr_mid if 'invert' in sel_wrapper else expr_mid
		expr_mid = 'clamp(%s)' % expr_mid if 'clamp' in sel_wrapper else expr_mid
		expr_out = expr_mid

		key_layer = '$ly'
		key_channel = '$ch'

		# convert 'alpha' to 'a' and remove '.' if input channel is selected to 'rgba'
		if sel_layer in ['rgb','rgba'] and '$ly' in expr_out:
			sel_layer = ''
			try:
				expr_out = expr_out.replace('.','',1)
			except:
				expr_out

			expr_out = re.sub('red','r', expr_out)
			expr_out = re.sub('green','g', expr_out)
			expr_out = re.sub('blue','b', expr_out)
			expr_out = re.sub('alpha','a', expr_out)

		for k in sel_channel:
			expr_out = expr_out.replace(key_layer,sel_layer)
			node[k].setValue(expr_out.replace(key_channel,knob_to_ch[k]))
		
		node['tile_color'].setValue(0)

	def set_channels(self):
		'''when set channel button is pressed, cycle all, rgba, alpha'''
		btn = self.sender()
		ls_state = ['all', 'rgb', 'alpha']
		dic_state = {
			'all': ['r', 'g', 'b', 'alpha'],
			'rgb': ['r', 'g', 'b'],
			'alpha': ['alpha']
			}

		cur_state = btn.text()
		idx = ls_state.index(cur_state)

		if idx < 2: idx += 1
		else: idx = 0

		btn.setText(ls_state[idx])

		for k in self.ls_ch_layer:
			if k.text() in dic_state[cur_state]:
				k.setChecked(True)
			else:
				k.setChecked(False)

	def set_layer_box(self,node_expr,node_sel):
		'''get layers from root or selected node
		return: ls_layers (list of str)
		'''
		if node_sel:
			self.ls_layers = nuke.layers(node_sel)
		elif node_expr.dependencies() != []:
			self.ls_layers = nuke.layers(node_expr)
		else:
			self.ls_layers = nuke.layers()

		self.layer_box.clear()
		self.layer_box.addItems(self.ls_layers)

		return self.ls_layers # ['rgba', 'Id06']

	def set_preset(self):
		'''Called when preset button is pressed'''
		thisBtn=self.sender().text()
		thisPreset=PRESET_BTN[thisBtn]
		thisNode=self.node

		if thisBtn=='Raw Lighting':
			p=nuke.Panel('Select the albeto pass')
			p.addEnumerationPulldown('aov', ' '.join(nuke.layers()))
			if p.show():
				albeto=p.value('aov')
				for k in thisPreset:
					self.set_knobValue(k, '<albeto>', albeto)
		elif thisBtn == 'AOV Mask':
			p=AOVMaskBox()
			_mask = p.run(self.ls_layers)
			if _mask:
				self.node['expr3'].setValue('%s.%s' % (_mask[0], _mask[1]))
				self.node['tile_color'].setValue(COL[_mask[1]])
				self.node['label'].setValue('matte::[value expr3]')
		else:
			for k in thisPreset:
				self.set_knobValue(k)

		# self.node['label'].setValue(thisBtn)
		self.close()

	def set_knobValue(self, kvPaire, *strSub):
		'''set knob value
		@kvPaire: (<knob>, <value>)
		@*strSub: string to replace if any, (replaceThis, withThis)
		'''
		print(kvPaire)
		pKnob, pValue = kvPaire
		if len(strSub)>0 and len(strSub)==2:
			pValue=re.sub(strSub[0], strSub[1], pValue)
		else:
			pValue

		self.node[pKnob].setValue(pValue)



#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------






def node_under_cursor():
	dag_widget = get_DAG_widget()
	dag_center = QtCore.QPoint(*nuke.center())
	cursor_pos = QtGui.QCursor().pos()
	dag_widget_center = QtCore.QPoint((dag_widget.size().width()/ 2), (dag_widget.size().height()/2) )
	cursor_pos_in_dag = dag_widget.mapFromGlobal(cursor_pos)

	new_node_pos = ((cursor_pos_in_dag - dag_widget_center) / nuke.zoom() + dag_center)

	return list(new_node_pos.toTuple())


def get_DAG_widget():
	stack = QtWidgets.QApplication.topLevelWidgets()
	while stack:
		widget = stack.pop()
		for c in widget.children():
			if c.objectName() == 'DAG.1':
				return c
		stack.extend(c for c in widget.children() if c.isWidgetType())




#-------------------------------------------------------------------------------
#-Widgets
#-------------------------------------------------------------------------------




class AOVMaskBox(QtWidgets.QDialog):
	"""Popup box for selecting AOV mask"""

	def __init__(self):
		super(AOVMaskBox, self).__init__()
		self.mask = None

		self.label = QtWidgets.QLabel("Select AOV for mask")
		self.layer_combobox = QtWidgets.QComboBox()
		self.layer_combobox.setEditable(True)
		self.channel_combobox = QtWidgets.QComboBox()
		self.channel_combobox.addItems(['red','green','blue'])
		self.btn_set = QtWidgets.QPushButton("Set Mask")
		self.btn_set.clicked.connect(self.onConfirm)

		self.layout_master = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout_master)
		self.layout_mask = QtWidgets.QHBoxLayout()
		self.layout_mask.setContentsMargins(0,0,0,0)

		self.layout_master.addWidget(self.label)
		self.layout_master.addLayout(self.layout_mask)
		self.layout_master.addWidget(self.btn_set)

		self.layout_mask.addWidget(self.layer_combobox)
		self.layout_mask.addWidget(self.channel_combobox)

		self.setWindowTitle("AOV Mask Select")
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
	
	def onConfirm(self):
		"""When button is clicked"""

		self.mask = [self.layer_combobox.currentText(), self.channel_combobox.currentText()]
		self.close()

	def run(self, ls_layers):
		"""Run and execute"""

		self.layer_combobox.clear()
		self.layer_combobox.addItems(ls_layers)
		self.exec_()

		return self.mask




#------------------------------------------------------------------------------
#-Instancing
#------------------------------------------------------------------------------




ExprPrompt = Core_ExprPrompt()
