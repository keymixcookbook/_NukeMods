def _version_():
    ver='''

    version 0:
    - Basically working, when run(), prompt a frameless popup with line edit field


    '''




import nuke, nukescripts
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


class Core_SetLabel(QtGui.QDialog):
    def __init__(self):
        super(Core_SetLabel,self).__init__()

        self.lineInput = QtGui.QLineEdit()
        self.lineInput.setAlignment(QtCore.Qt.AlignCenter)
        self.lineInput.returnPressed.connect(self.onPressed)
        self.title = QtGui.QLabel("<b>Set Label</b>")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.layout = QtGui.QVBoxLayout()
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
        self.show()
        self.move(QtGui.QCursor.pos()+QtCore.QPoint(-100,-12))


SetLabel = Core_SetLabel()