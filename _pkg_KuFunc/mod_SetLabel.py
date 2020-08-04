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


# Source: http://www.nukepedia.com/python/nodegraph/ku_labler
# Tweaks to make it work with multiline by Erwan Leroy

import nuke
from Qt import QtWidgets, QtGui, QtCore


class Core_SetLabel(QtWidgets.QDialog):
	def __init__(self):
		super(Core_SetLabel,self).__init__()
		self.nodes = []

		self.text_edit = QtWidgets.QTextEdit()
		self.text_edit.setAlignment(QtCore.Qt.AlignCenter)
		self.text_edit.setMaximumHeight(50)
		self.title = QtWidgets.QLabel("<b>Set Label</b>")
		self.title.setAlignment(QtCore.Qt.AlignHCenter)

		self.help = QtWidgets.QLabel('<span style=" font-size:7pt; color:gray;">Ctrl+Enter to confirm</span>')
		self.help.setAlignment(QtCore.Qt.AlignRight)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.text_edit)
		self.layout.addWidget(self.help)
		self.setLayout(self.layout)
		self.resize(200,50)
		self.setWindowTitle("Set Label")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.text_edit.installEventFilter(self)


	def eventFilter(self, widget, event):
		if isinstance(event, QtGui.QKeyEvent):
			if event.key() == QtCore.Qt.Key_Return and  event.modifiers() == QtCore.Qt.ControlModifier:
				'''change label with enter-key is pressed'''
				newLabel = self.text_edit.toPlainText()
				for n in self.nodes:
					n['label'].setValue(newLabel)
				self.close()
				self.nodes = []
				return True
		return False


	def getNodes(self, dag):
		'''get the existing label of selected nodes'''
		print dag
		if dag == "Node Graph":
			context = nuke.root()
		else:
			context = nuke.toNode('root.' + dag.replace(" Node Graph", ""))
			if not context:
				return False
		with context:
			self.nodes = nuke.selectedNodes()
			if self.nodes:
				self.title.setText("<b>Set Label</b>")
				self.text_edit.setText(self.nodes[0]['label'].value())
				return True
		return False

	def run(self):
		'''rerun instance'''
		cursor = QtGui.QCursor.pos()
		try:
			dag = QtWidgets.QApplication.instance().widgetAt(cursor).parent().windowTitle()
		except:  # TODO: Figure out what kind of error could happen
			return
		if self.getNodes(dag):
			avail_space = QtWidgets.QDesktopWidget().availableGeometry(cursor)
			# QDesktopWidget will be deprecated in a later version of QT, use the following line instead
			# avail_space = QtWidgets.QApplication.instance().screenAt(QtGui.QCursor.pos()).availableGeometry()
			posx = min(max(cursor.x()-100, avail_space.left()), avail_space.right()-200)
			posy = min(max(cursor.y()-12, avail_space.top()), avail_space.bottom()-200)
			self.move(QtCore.QPoint(posx, posy))
			self.raise_()
			self.text_edit.setFocus()
			self.text_edit.selectAll()
			self.show()


SetLabel = Core_SetLabel()