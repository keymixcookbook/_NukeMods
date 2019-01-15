import Qt
from Qt import QtGui
from Qt import QtCore
from Qt.QtGui import *
from Qt.QtCore import *
import nuke


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(4);


class CustomButton(QPushButton):
    def __init__(self,_text, parent = None):
        super(CustomButton, self).__init__()
        self.setText(_text)
        self.setAcceptDrops(True)
        self.mineData = None
        self._parent = parent

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            self.mineData = e.mimeData().text()
            self.setFlat(False)
            e.accept()
        else:
            e.ignore()

    def dragLeaveEvent(self,e):
        self.setFlat(True)

    def dropEvent(self, e):
        #self.animateClick()
        self._parent.addHotkey(self.mineData)
        self.setFlat(True)


class TimeHotkeysButton(QPushButton):
    def __init__(self, _timeIn,_timeOut,_globalIn,_globalOut,_timeLock,_frame,_node,_text,_reference=None, parent = None):
        super(TimeHotkeysButton, self).__init__()
        self.timeIn=_timeIn
        self.timeOut=_timeOut
        self.globalIn=_globalIn
        self.globalOut=_globalOut
        self.timeLock=_timeLock
        self.node=_node
        self.frame=_frame
        self.setText(_text)
        self.knobdata = []
        self.refNode = None
        if _reference:
            if _reference.__class__==nuke.Node or _reference.__class__==nuke.Group:
                self.refNode = _reference
                for knob in _reference.allKnobs():
                    self.knobdata.append([knob.name(),knob.toScript()])
            else:
                self.refNode = _reference.node()
                self.knobdata.append([_reference.name(),_reference.toScript()])


###===============================================================================
###        CustomTableWidget
###===============================================================================
class TimeHotkeys(QDialog):
    def __init__(self):
        super(TimeHotkeys, self).__init__()
        self.generalLayout = QHBoxLayout(self)
        self.generalLayout.setMargin(0)
        self.generalLayout.setSpacing(0);
        self.addShortcutButton = CustomButton("+",self)
        self.addShortcutButton.clicked.connect(self.addHotkey)
        self.addShortcutButton.setFixedWidth(30)
        self.addShortcutButton.setToolTip('Add a timeline shortcut')
        self.addShortcutButton.setFlat(True)

        self.generalLayout.addWidget(self.addShortcutButton)


    def addHotkey(self,_mime=None):
        viewer_node = nuke.activeViewer().node()
        viewerrange = viewer_node['frame_range'].value().split("-")
        timeLock     = viewer_node['frame_range_lock'].value()
        timeIn       = viewerrange[0]
        timeOut      = viewerrange[1]
        globalIn     = nuke.root()['first_frame'].value()
        globalOut    = nuke.root()['last_frame'].value()
        frame        = None
        iText        = "%s - %s"%(timeIn,timeOut)
        node         = None
        reference    = None


        p = nuke.Panel('Save Hotkey')
        p.addSingleLineInput('Set shortcut name', "%s - %s"%(timeIn,timeOut))
        p.addBooleanCheckBox('Save Frame Range', 1)
        p.addBooleanCheckBox('Save Current Frame', 1)
        p.addBooleanCheckBox('Save Viewed Node', 0)
        if _mime:
            p.addEnumerationPulldown('Save Data From', 'Knob Node')

        p.addButton('Cancel')
        p.addButton('Ok')
        ret = p.show()
        if ret:
            iText = p.value('Set shortcut name')
            if p.value('Save Viewed Node'):
                try:
                    node  = viewer_node.input(nuke.activeViewer().activeInput())
                except:
                    node = None
            if p.value('Save Current Frame'):
                frame=nuke.frame()
            if _mime: #If the user did a knob drop
                strSplit = _mime.split(":")[-1].split(".")
                if p.value('Save Data From') == "Knob":
                    reference = nuke.toNode(".".join(strSplit[0:-1]))[strSplit[-1]]
                else:
                    reference = nuke.toNode(".".join(strSplit[0:-1]))

            hotkeyButton = TimeHotkeysButton(timeIn,timeOut,globalIn,globalOut,timeLock,frame,node,iText,reference)
            hotkeyButton.clicked.connect(self.pressedHotkey)
            hotkeyButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            hotkeyButton.customContextMenuRequested.connect(self.rightclicked)
            self.generalLayout.addWidget(hotkeyButton)


    def pressedHotkey(self):
        _sender = self.sender()
        viewer_node = nuke.activeViewer().node()
        viewer_node['frame_range_lock'].setValue(_sender.timeLock)
        viewer_node['frame_range'].setValue("%s-%s"%(_sender.timeIn,_sender.timeOut))
        nuke.root()['first_frame'].setValue(_sender.globalIn)
        nuke.root()['last_frame'].setValue(_sender.globalOut)
        if _sender.node:
            activeInput = nuke.activeViewer().activeInput()
            if not activeInput:
                activeInput = 0
                nuke.activeViewer().node().setInput(activeInput,_sender.node)
                nuke.activeViewer().activateInput(0)
            nuke.activeViewer().node().setInput(activeInput,_sender.node)

        if _sender.frame:
            nuke.frame(_sender.frame)

        if _sender.refNode:
            for knob in _sender.knobdata:
                _sender.refNode[knob[0]].fromScript(knob[1])


    def rightclicked(self):
        _sender = self.sender()
        self.generalLayout.removeWidget(_sender)
        _sender.deleteLater()
        _sender=None



def find_viewer():

    for widget in QtGui.QApplication.allWidgets():
        if widget.windowTitle() == nuke.activeViewer().node().name():
            return widget
    return False

def find_framerange(qtObject): #thanks Erwan Leroy =)
    for c in qtObject.children():
        found = find_framerange(c)
        if found:
            return found
        try:
            tt = c.toolTip().lower()
            if tt.startswith("frameslider range"):
                framerange=TimeHotkeys()
                wdgets = c.parentWidget().children()
                if len(wdgets) >= 3:
                    for x in range(3,len(wdgets)):
                        c.parentWidget().layout().removeWidget(c.parentWidget().children()[x])
                        c.parentWidget().children()[len(wdgets)-1].deleteLater()
                        c.parentWidget().children()[len(wdgets)-1]=None
                c.parentWidget().layout().addWidget(framerange)
                return c
        except:
            pass

cam_menu = find_framerange(find_viewer())
