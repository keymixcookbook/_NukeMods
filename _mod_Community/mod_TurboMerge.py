# TurboNode5000
# version 1.1.1

    # added checkbox option to create a new node instead of modifying the selected one
    # fixed creation of new layers in turboShuffle. turns out the official documentation is wrong :thinking_face:
    # fixed windows losing focus if mouse wasn't over them
    # turbo shuffle now ignores blank inputs

#love, matt

import nuke

#backwards compatibility
try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
    from PySide.QtGui import QStringListModel

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets
    from PySide2.QtGui import QStringListModel

def thisActualGroup(debug=False):
    groupName = nuke.thisGroup().fullName()
    if not nuke.thisGroup().fullName() == 'root':
        groupName = 'root.'+groupName
    if debug == True:
        nuke.tprint(groupName)
    return nuke.toNode(groupName)

def centerWindow(widget):
    frameGeo = widget.frameGeometry()
    screen = QtGuiWidgets.QApplication.desktop().screenNumber(QtGuiWidgets.QApplication.desktop().cursor().pos())
    center = QtGuiWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGeo.moveCenter(center)
    widget.move(frameGeo.topLeft())


class autocompleter(QtGuiWidgets.QLineEdit): #easily reusable lineEdits with autocomplete

    def __init__(self, list, prefill=None):
        super(autocompleter, self).__init__()
        self.list = list
        self.prefillObject = prefill
        self.alreadyPrefilled = False
        self.qList = QStringListModel()
        self.qList.setStringList(self.list)
        self.fakeEnterFlag = False
        self.completer = QtGuiWidgets.QCompleter()
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setModel(self.qList)
        self.confirmText = ''
        self.setCompleter(self.completer)
        self.updateList(list)

    def updateList(self, list):
        #update Qcompleter model
        self.list = list
        self.qList.setStringList(self.list)

    def event(self, event):
        #override tab and enter/return behaviour
        if self.completer.popup().isVisible():
            self.completer.highlighted.connect(self.setConfirmText)
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Tab:
                    if self.confirmText == '' or self.text() not in self.list:
                        self.setText(self.completer.currentCompletion())
                    else:
                        self.setText(self.confirmText)
                    self.fakeEnterFlag = True
                    QtCore.QCoreApplication.postEvent(self, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier))
                if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                    self.setText(self.completer.currentCompletion())
                    QtCore.QCoreApplication.postEvent(self, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier))
        else:
            self.confirmText = ''
        if event.type() == QtCore.QEvent.FocusIn:
            if self.alreadyPrefilled == False:
                if not self.prefillObject == None:
                    self.setText(self.prefillObject.text())
                    self.alreadyPrefilled = True
        return QtGuiWidgets.QLineEdit.event(self, event)

    def setConfirmText(self, text): #store the currently highlighted value to use in tab completion
        self.confirmText = text


class labelledLineEdit(QtGuiWidgets.QWidget): #just mushing a label and lineEdit together

    def __init__(self, label, lineEdit, mode=0, parent=None):
        super(labelledLineEdit, self).__init__()
        self.label = label
        self.lineEdit = lineEdit
        if mode == 0:
            self.setLayout(QtGuiWidgets.QVBoxLayout())
            self.layout().setSpacing(0)
        else:
            self.setLayout(QtGuiWidgets.QHBoxLayout())
            self.layout().setSpacing(5)
        self.layout().setContentsMargins(-1,0,-1,0)
        self.layout().addWidget(label)
        self.layout().addWidget(lineEdit)

    def label(self):
        return self.label

    def lineEdit(self):
        return self.lineEdit


class turboShuffle5000Widget(QtGuiWidgets.QWidget): #shuffle/shuffleCopy widget

    def __init__(self, parent=None):
        super(turboShuffle5000Widget, self).__init__()

        self.setLayout(QtGuiWidgets.QVBoxLayout())
        self.layout().setSpacing(5)
        self.setWindowTitle('TurboNode5000')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.context = nuke.toNode('root')
        self.extras = ['none', '']

        self.title = QtGuiWidgets.QLabel()
        self.title.setText('TurboNode 5000')
        self.title.setStyleSheet('font:bold')

        self.subtitle = QtGuiWidgets.QWidget()
        self.subtitle.setLayout(QtGuiWidgets.QHBoxLayout())
        self.subtitle.layout().setSpacing(5)
        self.subtitle.layout().setContentsMargins(0,0,0,0)
        self.subtitleText = QtGuiWidgets.QLabel()
        self.modifyNodeCheckBox = QtGuiWidgets.QCheckBox()
        self.modifyNodeCheckBox.stateChanged.connect(self.updateSubtitle)
        self.subtitle.layout().addWidget(self.modifyNodeCheckBox)
        self.subtitle.layout().addWidget(self.subtitleText, QtCore.Qt.AlignLeft)

        self.typeCheckbox = QtGuiWidgets.QCheckBox('Shuffle&Copy')
        self.typeCheckbox.stateChanged.connect(self.updateSubtitle)

        self.in1 = labelledLineEdit(QtGuiWidgets.QLabel('in 1'), autocompleter([]))
        self.out1 = labelledLineEdit(QtGuiWidgets.QLabel('out 1'), autocompleter([]))
        self.in2 = labelledLineEdit(QtGuiWidgets.QLabel('in 2'), autocompleter([]))
        self.out2 = labelledLineEdit(QtGuiWidgets.QLabel('out 2'), autocompleter([]))

        self.line1Widget = QtGuiWidgets.QWidget()
        self.line1Widget.setLayout(QtGuiWidgets.QHBoxLayout())
        self.line1Widget.layout().setContentsMargins(-1,0,-1,0)
        self.line1Widget.layout().addWidget(self.in1)
        self.line1Widget.layout().addWidget(self.out1)

        self.line2Widget = QtGuiWidgets.QWidget()
        self.line2Widget.setLayout(QtGuiWidgets.QHBoxLayout())
        self.line2Widget.layout().setContentsMargins(-1,0,-1,0)
        self.line2Widget.layout().addWidget(self.in2)
        self.line2Widget.layout().addWidget(self.out2)

        self.okButton = QtGuiWidgets.QPushButton('Yeah!')
        self.okButton.clicked.connect(self.confirm)
        self.cancelButton = QtGuiWidgets.QPushButton('Nah')
        self.cancelButton.clicked.connect(self.cancel)

        self.buttonWidget = QtGuiWidgets.QWidget()
        self.buttonWidget.setLayout(QtGuiWidgets.QHBoxLayout())
        self.buttonWidget.layout().setContentsMargins(0,0,0,0)
        self.buttonWidget.layout().addWidget(self.okButton)
        self.buttonWidget.layout().addWidget(self.cancelButton)

        self.layout().addWidget(self.title)
        self.layout().addWidget(self.subtitle)
        self.layout().addWidget(self.line1Widget)
        self.layout().addWidget(self.line2Widget)
        self.layout().addWidget(self.typeCheckbox)
        self.layout().addWidget(self.buttonWidget)

        self.reinitialise()

    def reinitialise(self):
        #reset all the panels to default state when reopened
        self.node = None
        self.in1Value = 'rgba'
        self.out1Value = 'rgba'
        self.in2Value = 'none'
        self.out2Value = 'none'
        try:
            with self.context:
                if not len(nuke.selectedNodes()) > 1:
                    if nuke.selectedNode().Class() == 'Shuffle':
                        self.typeCheckbox.setChecked(False)
                        self.node = nuke.selectedNode()
                    if nuke.selectedNode().Class() == 'ShuffleCopy':
                        self.typeCheckbox.setChecked(True)
                        self.node = nuke.selectedNode()
                    self.in1Value = self.node.knobs()['in'].value()
                    self.out1Value = self.node.knobs()['out'].value()
                    self.in2Value = self.node.knobs()['in2'].value()
                    self.out2Value = self.node.knobs()['out2'].value()
        except:
            pass
        self.in1.lineEdit.setText(self.in1Value)
        self.in1.lineEdit.updateList(nuke.layers()+self.extras)
        self.out1.lineEdit.setText(self.out1Value)
        self.out1.lineEdit.updateList(nuke.layers()+self.extras)
        self.in2.lineEdit.setText(self.in2Value)
        self.in2.lineEdit.updateList(nuke.layers()+self.extras)
        self.out2.lineEdit.setText(self.out2Value)
        self.out2.lineEdit.updateList(nuke.layers()+self.extras)

        self.in1.lineEdit.setFocus()
        self.in1.lineEdit.selectAll()

        self.modifyNodeCheckBox.setChecked(True)
        self.modifyNodeCheckBox.setVisible(True)
        self.updateSubtitle()

    def event(self, event):
        #setting enter/return and escape behaviour
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                self.confirm()
            if event.key() == QtCore.Qt.Key_Escape:
                self.cancel()
        return QtGuiWidgets.QWidget.event(self, event)

    def checkFakeEnter(self):
        #the autocompleters simulate enter key as part of tab completion
        #this checks whether the keypress was real or not
        self.check = False
        for x in [self.in1, self.out1, self.in2, self.out2]:
            if x.lineEdit.fakeEnterFlag == True:
                self.check = True
                x.lineEdit.fakeEnterFlag = False
        return self.check

    def updateSubtitle(self):

        if self.node == None:
            self.modifyNodeCheckBox.setChecked(False)
            self.modifyNodeCheckBox.setVisible(False)
            if self.typeCheckbox.isChecked():
                self.subtitleText.setText('new ShuffleCopy:')
            else:
                self.subtitleText.setText('new Shuffle:')
            self.typeCheckbox.setVisible(True)
            self.subtitleText.setStyleSheet('')
        else:
            self.typeCheckbox.setVisible(False)
        if self.modifyNodeCheckBox.isChecked():
            self.subtitleText.setText(self.node.name()+':')
            self.subtitleText.setStyleSheet('color:orange')
            self.typeCheckbox.setVisible(False)
        else:
            if self.typeCheckbox.isChecked():
                self.subtitleText.setText('new ShuffleCopy:')
            else:
                self.subtitleText.setText('new Shuffle:')
            self.typeCheckbox.setVisible(True)
            self.subtitleText.setStyleSheet('')

    def confirm(self):
        if self.checkFakeEnter() == False:
            self.answerList = [self.in1.lineEdit.text(), self.out1.lineEdit.text(), self.in2.lineEdit.text(), self.out2.lineEdit.text()]
            self.createList = []
            for x in self.answerList:
                if not x in nuke.layers() and not x in self.extras:
                    self.createList.append(x)
            if not self.createList == []:
                self.hide()
                if nuke.ask('''<font left>The following layers don't exist. Do you want to create them?

<i>%s</i>''' %'''
'''.join(self.createList)):
                    for l in self.createList:
                        nuke.Layer(l, ['%s.red' %l, '%s.green' %l, '%s.blue' %l, '%s.alpha' %l])
                self.show()
            if self.node == None or not self.modifyNodeCheckBox.isChecked():
                with self.context:
                    if self.typeCheckbox.isChecked():
                        node = nuke.createNode('ShuffleCopy')
                    else:
                        node = nuke.createNode('Shuffle')
            else:
                node = self.node
            node['in'].setValue(self.answerList[0])
            node['out'].setValue(self.answerList[1])
            node['in2'].setValue(self.answerList[2])
            node['out2'].setValue(self.answerList[3])
            self.close()

    def cancel(self):
        self.close()

    def open(self):
        self.context = thisActualGroup() #this is outside the reinitialise method to prevent errors before the gui has loaded
        self.reinitialise()
        self.show()
        centerWindow(self)


turboShuffle = turboShuffle5000Widget()


class copyLine(QtGuiWidgets.QWidget): #just so I don't have to do these 4 times

    def __init__(self, parent=None):
        super(copyLine, self).__init__()

        self.setLayout(QtGuiWidgets.QHBoxLayout())
        self.layout().setSpacing(5)
        self.layout().setContentsMargins(0,0,0,0)

        self.copyFrom = labelledLineEdit(QtGuiWidgets.QLabel('from'), autocompleter([]), 1)
        self.copyTo = labelledLineEdit(QtGuiWidgets.QLabel('to'), autocompleter([], self.copyFrom.lineEdit), 1)

        self.layout().addWidget(self.copyFrom)
        self.layout().addWidget(self.copyTo)

    def update(self, fromValue, toValue, list=None):
        self.copyFrom.lineEdit.setText(fromValue)
        self.copyTo.lineEdit.setText(toValue)
        if not list == None:
            self.copyFrom.lineEdit.updateList(list)
            self.copyTo.lineEdit.updateList(list)


class turboCopy5000Widget(QtGuiWidgets.QWidget): #copy widget

    def __init__(self, parent=None):
        super(turboCopy5000Widget, self).__init__()

        self.setLayout(QtGuiWidgets.QVBoxLayout())
        self.layout().setSpacing(5)
        self.setWindowTitle('TurboNode5000')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.context = nuke.toNode('root')

        self.title = QtGuiWidgets.QLabel()
        self.title.setText('TurboNode 5000')
        self.title.setStyleSheet('font:bold')

        self.subtitle = QtGuiWidgets.QWidget()
        self.subtitle.setLayout(QtGuiWidgets.QHBoxLayout())
        self.subtitle.layout().setSpacing(5)
        self.subtitle.layout().setContentsMargins(0,0,0,0)
        self.subtitleText = QtGuiWidgets.QLabel()
        self.modifyNodeCheckBox = QtGuiWidgets.QCheckBox()
        self.modifyNodeCheckBox.stateChanged.connect(self.updateSubtitle)
        self.subtitle.layout().addWidget(self.modifyNodeCheckBox)
        self.subtitle.layout().addWidget(self.subtitleText, QtCore.Qt.AlignLeft)

        self.channelCopy0 = copyLine()
        self.channelCopy1 = copyLine()
        self.channelCopy2 = copyLine()
        self.channelCopy3 = copyLine()

        self.layerCopy = labelledLineEdit(QtGuiWidgets.QLabel('layer copy'), autocompleter([]), 1)

        self.okButton = QtGuiWidgets.QPushButton('Yeah!')
        self.okButton.clicked.connect(self.confirm)
        self.cancelButton = QtGuiWidgets.QPushButton('Nah')
        self.cancelButton.clicked.connect(self.cancel)

        self.buttonWidget = QtGuiWidgets.QWidget()
        self.buttonWidget.setLayout(QtGuiWidgets.QHBoxLayout())
        self.buttonWidget.layout().setContentsMargins(0,0,0,0)
        self.buttonWidget.layout().addWidget(self.okButton)
        self.buttonWidget.layout().addWidget(self.cancelButton)

        self.layout().addWidget(self.title)
        self.layout().addWidget(self.subtitle)
        self.layout().addWidget(self.layerCopy)
        self.layout().addWidget(self.channelCopy0)
        self.layout().addWidget(self.channelCopy1)
        self.layout().addWidget(self.channelCopy2)
        self.layout().addWidget(self.channelCopy3)
        self.layout().addWidget(self.buttonWidget)

        self.reinitialise()

    def reinitialise(self):
        #reset all the panels to default state when reopened
        self.node = None
        self.layerCopyValue = 'none'
        self.copyFrom0Value = 'none'
        self.copyTo0Value = 'none'
        self.copyFrom1Value = 'none'
        self.copyTo1Value = 'none'
        self.copyFrom2Value = 'none'
        self.copyTo2Value = 'none'
        self.copyFrom3Value = 'none'
        self.copyTo3Value = 'none'

        try:
            with self.context:
                if not len(nuke.selectedNodes()) > 1:
                    if nuke.selectedNode().Class() == 'Copy':
                        self.node = nuke.selectedNode()
                        self.layerCopyValue = self.node.knobs()['channels'].value()
                        self.copyFrom0Value = self.node.knobs()['from0'].value()
                        self.copyTo0Value = self.node.knobs()['to0'].value()
                        self.copyFrom1Value = self.node.knobs()['from1'].value()
                        self.copyTo1Value = self.node.knobs()['to1'].value()
                        self.copyFrom2Value = self.node.knobs()['from2'].value()
                        self.copyTo2Value = self.node.knobs()['to2'].value()
                        self.copyFrom3Value = self.node.knobs()['from3'].value()
                        self.copyTo3Value = self.node.knobs()['to3'].value()
        except:
            pass
        self.layerCopy.lineEdit.setText(self.layerCopyValue)
        self.layerCopy.lineEdit.updateList(nuke.layers()+['none', 'all'])
        extras = ['none', 'red', 'green', 'blue', 'alpha']
        self.channelCopy0.update(self.copyFrom0Value, self.copyTo0Value, nuke.channels()+extras)
        self.channelCopy1.update(self.copyFrom1Value, self.copyTo1Value, nuke.channels()+extras)
        self.channelCopy2.update(self.copyFrom2Value, self.copyTo2Value, nuke.channels()+extras)
        self.channelCopy3.update(self.copyFrom3Value, self.copyTo3Value, nuke.channels()+extras)

        self.layerCopy.lineEdit.setFocus()
        self.layerCopy.lineEdit.selectAll()

        self.modifyNodeCheckBox.setChecked(True)
        self.modifyNodeCheckBox.setVisible(True)
        self.updateSubtitle()

    def event(self, event):
        #setting enter/return and escape behaviour
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                self.confirm()
            if event.key() == QtCore.Qt.Key_Escape:
                self.cancel()
        return QtGuiWidgets.QWidget.event(self, event)

    def checkFakeEnter(self):
        #the autocompleters simulate enter key as part of tab completion
        #this checks whether the keypress was real or not
        self.check = False
        for x in [self.channelCopy0, self.channelCopy1, self.channelCopy2, self.channelCopy3]:
            if x.copyFrom.lineEdit.fakeEnterFlag == True:
                self.check = True
                x.copyFrom.lineEdit.fakeEnterFlag = False
            if x.copyTo.lineEdit.fakeEnterFlag == True:
                self.check = True
                x.copyTo.lineEdit.fakeEnterFlag = False
        if self.layerCopy.lineEdit.fakeEnterFlag == True:
            self.check = True
            self.layerCopy.lineEdit.fakeEnterFlag = False
        return self.check

    def updateSubtitle(self):
        if self.node == None:
            self.modifyNodeCheckBox.setChecked(False)
            self.modifyNodeCheckBox.setVisible(False)
            self.subtitleText.setText('new Copy:')
            self.subtitleText.setStyleSheet('')
        if self.modifyNodeCheckBox.isChecked():
            self.subtitleText.setText(self.node.name()+':')
            self.subtitleText.setStyleSheet('color:orange')
        else:
            self.subtitleText.setText('new Copy:')
            self.subtitleText.setStyleSheet('')

    def confirm(self):
        if self.checkFakeEnter() == False:
            if self.node == None or not self.modifyNodeCheckBox.isChecked():
                with self.context:
                    node = nuke.createNode('Copy')
            else:
                node = self.node
            node['from0'].setValue(self.channelCopy0.copyFrom.lineEdit.text())
            node['to0'].setValue(self.channelCopy0.copyTo.lineEdit.text())
            node['from1'].setValue(self.channelCopy1.copyFrom.lineEdit.text())
            node['to1'].setValue(self.channelCopy1.copyTo.lineEdit.text())
            node['from2'].setValue(self.channelCopy2.copyFrom.lineEdit.text())
            node['to2'].setValue(self.channelCopy2.copyTo.lineEdit.text())
            node['from3'].setValue(self.channelCopy3.copyFrom.lineEdit.text())
            node['to3'].setValue(self.channelCopy3.copyTo.lineEdit.text())
            node['channels'].setValue(self.layerCopy.lineEdit.text())
            self.close()

    def cancel(self):
        self.close()

    def open(self):
        self.context = thisActualGroup()
        self.reinitialise() #this is outside the reinitialise method to prevent errors before the gui has loaded
        self.show()
        centerWindow(self)

turboCopy = turboCopy5000Widget()


class turboMerge5000Widget(QtGuiWidgets.QWidget): #merge widget

    def __init__(self, parent=None):
        super(turboMerge5000Widget, self).__init__()

        self.setLayout(QtGuiWidgets.QVBoxLayout())
        self.layout().setSpacing(5)
        self.setWindowTitle('TurboNode5000')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.context = nuke.toNode('root')

        self.title = QtGuiWidgets.QLabel()
        self.title.setText('TurboNode 5000')
        self.title.setStyleSheet('font:bold')

        self.subtitle = QtGuiWidgets.QWidget()
        self.subtitle.setLayout(QtGuiWidgets.QHBoxLayout())
        self.subtitle.layout().setSpacing(5)
        self.subtitle.layout().setContentsMargins(0,0,0,0)
        self.subtitleText = QtGuiWidgets.QLabel()
        self.modifyNodeCheckBox = QtGuiWidgets.QCheckBox()
        self.modifyNodeCheckBox.stateChanged.connect(self.updateSubtitle)
        self.subtitle.layout().addWidget(self.modifyNodeCheckBox)
        self.subtitle.layout().addWidget(self.subtitleText, QtCore.Qt.AlignLeft)


        self.mergeOp = labelledLineEdit(QtGuiWidgets.QLabel('operation'), autocompleter([]), 1)
        self.mergeOpValue = ''
        self.prev = 'over'

        self.okButton = QtGuiWidgets.QPushButton('Yeah!')
        self.okButton.clicked.connect(self.confirm)
        self.cancelButton = QtGuiWidgets.QPushButton('Nah')
        self.cancelButton.clicked.connect(self.cancel)

        self.buttonWidget = QtGuiWidgets.QWidget()
        self.buttonWidget.setLayout(QtGuiWidgets.QHBoxLayout())
        self.buttonWidget.layout().setContentsMargins(0,0,0,0)
        self.buttonWidget.layout().addWidget(self.okButton)
        self.buttonWidget.layout().addWidget(self.cancelButton)

        self.layout().addWidget(self.title)
        self.layout().addWidget(self.subtitle)
        self.layout().addWidget(self.mergeOp)
        self.layout().addWidget(self.buttonWidget)

        self.reinitialise()

    def reinitialise(self):
        #reset all the panels to default state when reopened
        self.node = None
        self.mergeOpValue = self.prev

        try:
            with self.context:
                if not len(nuke.selectedNodes()) > 1:
                    if nuke.selectedNode().Class() == 'Merge2':
                        self.node = nuke.selectedNode()
                        self.mergeOpValue = self.node.knobs()['operation'].value()
        except:
            pass

        refNode = nuke.nodes.Merge2() #cheeky merge to fetch the list of ops (so I don't have to write them)
        self.mergeOp.lineEdit.setText(self.mergeOpValue)
        self.mergeOp.lineEdit.updateList(refNode.knobs()['operation'].values())
        nuke.delete(refNode)

        self.mergeOp.lineEdit.setFocus()
        self.mergeOp.lineEdit.selectAll()

        self.modifyNodeCheckBox.setChecked(True)
        self.modifyNodeCheckBox.setVisible(True)
        self.updateSubtitle()

    def event(self, event):
        #setting enter/return and escape behaviour
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                self.confirm()
            if event.key() == QtCore.Qt.Key_Escape:
                self.cancel()
        return QtGuiWidgets.QWidget.event(self, event)

    def checkFakeEnter(self):
        #the autocompleters simulate enter key as part of tab completion
        #this checks whether the keypress was real or not
        #hacky but it works, promise
        self.check = False
        if self.mergeOp.lineEdit.fakeEnterFlag == True:
            self.check = True
            self.mergeOp.lineEdit.fakeEnterFlag = False
        return self.check

    def updateSubtitle(self):
        if self.node == None:
            self.modifyNodeCheckBox.setChecked(False)
            self.modifyNodeCheckBox.setVisible(False)
            self.subtitleText.setText('new Merge:')
            self.subtitleText.setStyleSheet('')
        if self.modifyNodeCheckBox.isChecked():
            self.subtitleText.setText(self.node.name()+':')
            self.subtitleText.setStyleSheet('color:orange')
        else:
            self.subtitleText.setText('new Merge:')
            self.subtitleText.setStyleSheet('')

    def confirm(self):
        if self.checkFakeEnter() == False:
            if self.node == None or not self.modifyNodeCheckBox.isChecked():
                with self.context:
                    node = nuke.createNode('Merge2')
            else:
                node = self.node
            node['operation'].setValue(str(self.mergeOp.lineEdit.text()))
            self.prev = node.knobs()['operation'].value()
            self.close()

    def cancel(self):
        self.close()

    def open(self):
        self.context = thisActualGroup() #this is outside the reinitialise method to prevent errors before the gui has loaded
        self.reinitialise()
        self.show()
        centerWindow(self)


turboMerge = turboMerge5000Widget()
