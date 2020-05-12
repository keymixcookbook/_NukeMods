def _version_():
	ver='''

	version 1.1
	- add preset buttons and input autocomplet presets
	- add button to cycle channels

	version 0.0
	- Expression node with prompt options
	- string replace keys ('$ly': layer, '$ch': channels)
	- input field completer with layers
	- Create Expression node if non-Expression node selected, auto fill LineEdit if Expression node selected

	'''
	return ver




#------------------------------------------------------------------------------
#-imports
#------------------------------------------------------------------------------




import nuke, nukescripts

from Qt import QtCore, QtGui, QtWidgets
import re




#------------------------------------------------------------------------------
#-Variable
#------------------------------------------------------------------------------




PRESET_LINE = [
	'rgb', 'rgba', 'alpha', 'max(r,g,b)', 'min(r,g,b)', 'a>0',
	'r/g', 'r/b', 'g/r', 'g/b', 'b/r', 'b/g',
	'isinf($ch)?$ch(x+1,y):$ch','isnan($ch)?$ch(x-1,y):$ch',
]

PRESET_BTN = {
	'STMap': [
		('expr0','(x+0.5)/width'),
		('expr1','(y+0.5)/height')
		],
	'Luma-Rec709': [
		('expr0', 'r*0.2126+g*0.7152+b*0.0722'),
		('channel0','rgb')
		],
	'Raw Lighting': [
		('expr0', 'rgba.red/<albeto>.red'),
		('expr1', 'rgba.green/<albeto>.green'),
		('expr2', 'rgba.blue/<albeto>.blue')
		],
	'Depth Normalize': [
		('channel0', 'depth'),
		('expr0', 'z==0?0:1/z')
		]
}

TITLE = "ExprPrompt"




#------------------------------------------------------------------------------
#-Core Class
#------------------------------------------------------------------------------




class Core_ExprPrompt(QtWidgets.QWidget):
	def __init__(self):
		super(Core_ExprPrompt, self).__init__()
		# set
		self.ls_layers = PRESET_LINE

		# Left Widgets
		self.title = QtWidgets.QLabel("<h3>%s</h3>" % TITLE)
		self.st_expr = QtWidgets.QLineEdit()
		self.st_expr.setPlaceholderText('$ly: layer (Id06), $ch: channel (red)')
		self.st_expr.returnPressed.connect(self.onPressed)
		self.st_expr.setCompleter(QtWidgets.QCompleter(self.ls_layers))
		self.st_expr.textChanged.connect(self.onTextChanged)
		self.mu_layers = QtWidgets.QComboBox()
		self.mu_layers.setEnabled(False)
		self.ck_ch_r = QtWidgets.QCheckBox('r')
		self.ck_ch_g = QtWidgets.QCheckBox('g')
		self.ck_ch_b = QtWidgets.QCheckBox('b')
		self.ck_ch_a = QtWidgets.QCheckBox('alpha')
		self.bt_ch_all = QtWidgets.QPushButton('all')
		self.bt_ch_all.clicked.connect(self.setChannels)
		self.ck_clamp = QtWidgets.QCheckBox('clamp')
		self.ck_invert = QtWidgets.QCheckBox('invert')
		self.bt_set = QtWidgets.QPushButton('Set!')
		self.bt_set.clicked.connect(self.onPressed)

		# Right Widgets
		for idx, p in enumerate(PRESET_BTN.keys()):
			exec("self.presetBtn%s=QtWidgets.QPushButton('%s')" % (idx, p))
			exec("self.presetBtn%s.clicked.connect(self.setPreset)" % (idx))


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
		for m in [self.st_expr, self.mu_layers]:
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
		self.mu_layers.setMaximumWidth(70)

		self.setWindowTitle(TITLE)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()

	def setDefault(self):
		'''set default value when instansing'''
		self.mu_layers.addItems(self.ls_layers)
		for k in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_clamp, self.ck_invert]:
			k.setChecked(False)
		self.ck_ch_a.setChecked(True)
		self.st_expr.setFocus()
		self.mu_layers.setEditable(False)

	def onTextChanged(self):
		'''if string key are in line edit, enable combobox'''
		if '$ly' in self.st_expr.text():
			self.mu_layers.setEnabled(True)
		else:
			self.mu_layers.setEnabled(False)

	def extendCompleter(self, sel_layer):
		'''extend the completer with layers'''
		layer_extended = sel_layer
		thisCompleter = QtWidgets.QCompleter(layer_extended)
		thisCompleter.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
		self.st_expr.setCompleter(thisCompleter)

	def setPrevExpr(self, node_expr, node_sel):
		'''previously expression, none if nothing selected
		@node_expr: expressions to add (str)
		@node_sel: nodes selected (list of obj)
		return: prevExpr (str)

		nothing selected: node_sel = None, node_expr = New Expression
		one non-Expression selected: node_sel = selected node, node_expr = New Expression
		one Expression selected: node_sel = None, node_expr = selected expression
		'''
		if node_sel == None and nuke.selectedNodes()[0] == node_expr:
			self.prevExpr = node_expr['expr3'].value()
		else:
			self.prevExpr = None

		self.st_expr.setText(self.prevExpr)
		# print self.prevExpr

		return self.prevExpr

	def getSelected(self):
		'''get values for the checkboxs and comboboxs
		return: [sel_layer, sel_channel, sel_wrapper] (list of lists)
		'''
		sel_layer = self.mu_layers.currentText() # 'Id06'

		sel_channel, sel_wrapper = [],[]

		for idx,c in enumerate(self.ls_ch_layer):
			if c.isChecked():
				sel_channel.append('expr%s' % idx) # ['expr1', 'expr2']
		for w in self.ls_wrapper:
			if w.isChecked():
				sel_wrapper.append(w.text()) # ['clamp', 'invert']

		return [sel_layer, sel_channel, sel_wrapper]

	def setExpr(self, node, sel):
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

	def onPressed(self):
		'''when enter-key is pressed on expression line edit'''
		self.setExpr(self.node, self.getSelected())
		self.close()

	def setChannels(self):
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
		if idx < 2:
			idx += 1
		else:
			idx = 0
		btn.setText(ls_state[idx])

		for k in self.ls_ch_layer:
			if k.text() in dic_state[cur_state]:
				k.setChecked(True)
			else:
				k.setChecked(False)

	def setLayers(self,node_expr,node_sel):
		'''get layers from root
		return: ls_layers (list of str)
		'''
		self.mu_layers.clear()
		self.ls_layers if node_sel == None else self.ls_layers.extend(nuke.layers(node_sel))
		self.mu_layers.addItems(self.ls_layers)

		return self.ls_layers # ['rgba', 'Id06']

	def getNode(self):
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
			node_expr = nuke.createNode('Expression')
		elif len(sel) == 1:
			if sel[0].Class() != 'Expression':
				node_sel = sel[0]
				node_expr = nuke.createNode('Expression')
			elif sel[0].Class() == 'Expression':
				node_sel = None # Expression node doesn't return any layer channels
				node_expr = sel[0]

		self.node = node_expr
		return [node_expr, node_sel]


	def setPreset(self):
		'''Called when preset button is pressed'''
		thisBtn=self.sender().text()
		thisPreset=PRESET_BTN[thisBtn]
		thisNode=self.node

		def setKnobValue(kvPaire, *strSub):
			'''set knob value
			@kvPaire: (<knob>, <value>)
			@*strSub: string to replace if any, (replaceThis, withThis)
			'''
			pKnob, pValue = kvPaire
			if len(strSub)>0 and len(strSub)==2:
				pValue=re.sub(strSub[0], strSub[1], pValue)
			else:
				pValue

			self.node[pKnob].setValue(pValue)

		if thisBtn=='Raw Lighting':
			p=nuke.Panel('Select the albeto pass')
			p.addEnumerationPulldown('aov', ' '.join(nuke.layers()))
			if p.show():
				albeto=p.value('aov')
				for k in thisPreset:
					setKnobValue(k, '<albeto>', albeto)
		else:
			for k in thisPreset:
				setKnobValue(k)

		self.node['label'].setValue(thisBtn)
		self.close()


	def run(self):
		'''run the instance'''

		self.setDefault()
		node_expr, node_sel = self.getNode()
		ls_layers = self.setLayers(node_expr, node_sel)
		self.extendCompleter(ls_layers)
		self.setPrevExpr(node_expr, node_sel)
		self.st_expr.selectAll()
		self.move(QtGui.QCursor.pos())
		self.show()




#------------------------------------------------------------------------------
#-Instancing
#------------------------------------------------------------------------------




ExprPrompt = Core_ExprPrompt()
if 'upt_' in __file__:
	ExprPrompt.run()
