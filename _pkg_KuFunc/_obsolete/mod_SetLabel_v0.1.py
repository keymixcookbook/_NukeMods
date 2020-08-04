def _version_():
	ver='''

	version 1.0
	- adding multiline support
	- adding group node context

	version 0:
	- Basically working, when run(), prompt a frameless popup with line edit field

	version 0.1:
	- replace with Qt


	'''




import nuke, nukescripts
from Qt import QtWidgets, QtGui, QtCore


class Core_SetLabel(QtWidgets.QDialog):
	def __init__(self):
		super(Core_SetLabel,self).__init__()

		self.lineInput = QtWidgets.QTextEdit()
		# self.lineInput.setAlignment(QtCore.Qt.AlignCenter)
		self.lineInput.setMaximumHeight(25)
		# self.lineInput.returnPressed.connect(self.onPressed)
		self.title = QtWidgets.QLabel("<b>Set Label</b>")
		self.subtitle = QtWidgets.QLabel()
		self.subtitle.setStyleSheet("font-size: 7pt")
		self.keytip = QtWidgets.QLabel("Ctl+Enter to confirm")
		self.keytip.setAlignment(QtCore.Qt.AlignRight)
		self.keytip.setStyleSheet("font-size: 7pt")

		self.lineInput.installEventFilter(self)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.subtitle)
		self.layout.addWidget(self.lineInput)
		self.layout.addWidget(self.keytip)
		self.setLayout(self.layout)
		self.resize(200,50)
		self.setWindowTitle("Set Label")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()

	def eventFilter(self, widget, event):
		'''change even when key combo is pressed'''
		if isinstance(event, QtGui.QKeyEvent):
			if event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.ControlModifier:
				_newLabel = self.lineInput.toPlainText()
				self.set_Label(self.sel_nodes,_newLabel)
				self.close()
				
	def set_Label(self,nodes,newLabel):
		'''sets the label
		@node: node (list of objs)
		@newLabel: new label from input (str)
		'''
		for n in nodes:
			nuke.toNode(n)['label'].setValue(newLabel)

	def get_Nodes(self):
		'''get selected node with context
		return: list of node names (list of str)
		'''
		_rootDAG = "Node Graph"
		cursor = QtGui.QCursor.pos()
		try:
			dag = QtWidgets.QApplication.instance().widgetAt(cursor).parent().windowTitle()

			if dag == "Node Graph":
				context = nuke.root()
			else:
				context = nuke.toNode('root.' + dag.replace(" Node Graph", ""))
				
			with context:
				self.sel_nodes = [n.fullName() for n in nuke.selectedNodes()]
				return True
		except:
			return
		return False
		
	def setDefault(self):
		'''get the existing label of selected nodes'''

		self.sel_nodes = []
		self.get_Nodes()
		_cur_label = nuke.toNode(self.sel_nodes[0])['label'].value()
		self.lineInput.setText(_cur_label)
		self.subtitle.setText(', '.join(self.sel_nodes))

	def run(self):
		'''rerun instance'''
		self.setDefault()
		self.move(QtGui.QCursor.pos()+QtCore.QPoint(-100,-12))
		self.raise_()
		self.lineInput.setFocus()
		self.lineInput.selectAll()
		self.show()


SetLabel = Core_SetLabel()
