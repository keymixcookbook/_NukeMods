import nuke, nukescripts
from Qt import QtWidgets, QtGui, QtCore


class Core_SetLabel(QtWidgets.QDialog):
	def __init__(self):
		super(Core_SetLabel,self).__init__()

		self.lineInput = QtWidgets.QLineEdit()
		self.lineInput.setAlignment(QtCore.Qt.AlignCenter)
		self.lineInput.returnPressed.connect(self.onPressed)
		self.title = QtWidgets.QLabel("<b>Set Label</b>")
		self.title.setAlignment(QtCore.Qt.AlignHCenter)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.lineInput)
		self.setLayout(self.layout)
		self.resize(200,50)
		self.setWindowTitle("Set Label")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

		self.setDefault()


	def onPressed(self):
		'''change label with enter-key is pressed'''
		newLabel = self.lineInput.text()
		for n in nuke.selectedNodes():
			n['label'].setValue(newLabel)
		self.close()



	def setDefault(self):
		'''get the existing label of selected nodes'''
		sel_nodes = nuke.selectedNodes()
		if sel_nodes:
			self.lineInput.show()
			self.title.setText("<b>Set Label</b>")
			self.lineInput.setText(sel_nodes[0]['label'].value())
		else:
			self.lineInput.hide()
			self.title.setText("<b>Errpr:<br>No Node Selected</b>")



	def run(self):
		'''rerun instance'''
		self.setDefault()
		self.move(QtGui.QCursor.pos()+QtCore.QPoint(-100,-12))
		self.raise_()
		self.lineInput.setFocus()
		self.lineInput.selectAll()
		self.show()


SetLabel = Core_SetLabel()



# Add to Menu/Edit

m_tab = nuke.menu("Nuke").findItem("Edit")
m_tab.addCommand("ku_labeler", ku_labeler.SetLabel.run(), 'shift+n')
