import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

class core_SetLabel(QDialog):
    def __init__(self,prevLabel):
        super(core_SetLabel,self).__init__()

        self.lineInput = QtGui.QLineEdit()
        self.lineInput.setText(prevLabel)
        self.lineInput.setAlignment(QtCore.Qt.AlignCenter)
        self.lineInput.returnPressed.connect(self.onPressed)
        self.title = QtGui.QLabel("<b>Set Label</b>")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.lineInput)
        self.setLayout(self.layout)
        self.move(QtGui.QCursor.pos())
        self.setWindowTitle("Set Label")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    def onPressed(self):
        # Change Values

        newLabel = self.lineInput.text()
        for n in nuke.selectedNodes():
            n['label'].setValue(newLabel)

        self.close()



class SetLabel():
    if len(nuke.selectedNodes())>0:
        prevLabel = nuke.selectedNode()['label'].getValue()
        p = core_SetLabel(prevLabel)
        p.show()
        print "shown"
    else:
        nuke.message("No node selected la")
