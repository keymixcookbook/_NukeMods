from Qt import QtWidgets, QtGui, QtCore
import sys, time, os, json


class MarkerAdd(QtWidgets.QDialog):
    '''
    GUI for adding markers
    data to be stored:frame, tooltip, id(<SHOW>-<timestamp>, PHX-12345678)
    '''
    def __init__(self, layout_obj):
        super(MarkerAdd, self).__init__()

        # cur_frame = nuke.frame()
        cur_frame = 1001
        self.thisLayout = layout_obj
        self.m_frame = QtWidgets.QSpinBox()
        self.m_frame.setMaximum(3000)
        self.m_frame.setPrefix('x')
        self.m_frame.setValue(cur_frame)
        self.m_frame.selectAll()
        self.m_label = QtWidgets.QLineEdit()
        self.m_label.setPlaceholderText("Keep it short")
        self.m_add = QtWidgets.QPushButton('Add Marker')
        self.m_add.clicked.connect(self.add)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.m_frame)
        self.layout.addWidget(self.m_label)
        self.layout.addWidget(self.m_add)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Frame Marker")


    def add(self):
        '''add button'''
        thisFrame = int(self.m_frame.text().replace('x', ''))
        thisId = int(time.time())
        thisLabel = self.m_label.text()
        thisMarker = MarkerButton(thisId, thisFrame, thisLabel)
        # thisMarker.customContextMenuRequested.connect(Core_TimelineMarker.removeMarker)

        label_button = self.m_label.text() if len(self.m_label.text())<=10 else self.m_label.text()[:10]+'...'
        thisMarker.setText(label_button)
        thisMarker.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)" % (thisMarker.frame, thisMarker.label, thisMarker.id) )
        self.thisLayout.addWidget(thisMarker)
        self.close()

        #self.onSave()


    def onSave(self):
        '''save buttons when clicked'''
        num_widget = layout_obj.count()
        self.saveMarkers()


class MarkerButton(QtWidgets.QPushButton):
    def __init__(self, id, frame, label):
        super(MarkerButton, self).__init__()

        self.id = id
        self.frame = frame
        self.label = label


class Core_TimelineMarker(QtWidgets.QWidget):
    def __init__(self):
        super(Core_TimelineMarker, self).__init__()

        self.data_folder = "/Users/Tianlun/Desktop/_NukeTestScript"
        self.data_filename = "TimelineMarker_dataset.json"
        self.data_file = os.path.join(self.data_folder, self.data_filename)

        self.bt_add = QtWidgets.QPushButton('+')
        self.bt_add.clicked.connect(self.addMarker)
        self.bt_add.setStyle(QtGui.QFont().setBold(True))
        self.bt_remove = QtWidgets.QPushButton('-')
        self.bt_remove.clicked.connect(self.removeMarker)
        self.bt_save = QtWidgets.QPushButton('save')
        self.bt_save.clicked.connect(self.saveMarkers)
        self.bt_reload = QtWidgets.QPushButton('reload')
        self.bt_reload.clicked.connect(self.reloadMarkers)
        self.bt_reloadFile = QtWidgets.QPushButton('reload from file')
        self.bt_reloadFile.clicked.connect(self.loadFromFile)

        self.layout_master = QtWidgets.QHBoxLayout()
        self.layout_editMarkers = QtWidgets.QVBoxLayout()
        self.layout_editMarkers.setAlignment(QtCore.Qt.AlignLeft)
        self.layout_editMarkers.setContentsMargins(0,0,0,0)

        self.layout_markers = QtWidgets.QHBoxLayout()
        self.group_markers = QtWidgets.QGroupBox('Markers')
        self.group_markers.setLayout(self.layout_markers)
        self.group_markers.setAlignment(QtCore.Qt.AlignLeft)

        self.layout_reload = QtWidgets.QVBoxLayout()
        self.layout_reload.setAlignment(QtCore.Qt.AlignRight)
        self.layout_reload.setContentsMargins(0,0,0,0)

        self.layout_editMarkers.addWidget(self.bt_add)
        self.layout_editMarkers.addWidget(self.bt_remove)
        self.layout_editMarkers.setSpacing(0)
        self.layout_reload.addWidget(self.bt_save)
        self.layout_reload.addWidget(self.bt_reload)
        self.layout_reload.addWidget(self.bt_reloadFile)

        self.layout_master.addLayout(self.layout_editMarkers)
        self.layout_master.addWidget(self.group_markers)
        self.layout_master.addStretch()
        self.layout_master.addLayout(self.layout_reload)
        self.setLayout(self.layout_master)
        self.setMinimumWidth(1000)
        self.setContentsMargins(0,0,0,0)



    def saveMarkers(self):
        '''save marker into json files'''
        layout_markers = self.layout_markers
        num_widget = layout_markers.count()
        json_marker = []

        for w in range(0,num_widget):
            thisData = {}
            thisWidget = layout_markers.itemAt(w).widget()
            thisData['id'] = thisWidget.id
            thisData['frame'] = thisWidget.frame
            thisData['label'] = thisWidget.label
            json_marker.append(thisData)

        with open(self.data_file, 'w') as f:
            json_data = json.dumps(json_marker, indent=2)
            f.write(json_data)


    def addMarker(self):
        '''add MarkerButton widget'''
        self.p = MarkerAdd(self.layout_markers)
        # add connect signal to the last widgets
        self.p.exec_()
        try:
            newWidget = self.layout_markers.itemAt(self.layout_markers.count()-1).widget()
            newWidget.clicked.connect(self.setFrame)
            newWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            newWidget.customContextMenuRequested.connect(self.removeMarker_RClicked)
        except:
            pass


    def removeMarker_RClicked(self):
        '''remove marker when right-clicked'''
        sender = self.sender()
        self.layout_markers.removeWidget(sender)
        sender.deleteLater()


    def removeMarker(self):
        '''remove MarkerButton widget'''
        try:
            num_widget = self.layout_markers.count()-1
            thisWidget = self.layout_markers.itemAt(num_widget).widget()
            thisWidget.setParent(None)
            self.saveMarkers()
        except:
            print "no markers to be removed"


    def reloadMarkers(self):
        '''reload from json file and rebuild MarkerButtons'''
        thisFile = self.data_file
        thisData = []
        with open(self.data_file, 'r') as f:
            thisData = json.load(f)
            print thisData

        num_widget = self.layout_markers.count()
        for w in range(num_widget):
            thisWidget = self.layout_markers.itemAt(w).widget()
            thisWidget.setParent(None)

        for w in thisData:
            thisFrame = w['frame']
            thisId = w['id']
            thisLabel = w['label']
            thisMarker = MarkerButton(thisId, thisFrame, thisLabel)

            label_button = thisLabel if len(thisLabel)<=10 else thisLabel[:10]+'...'
            thisMarker.setText(label_button)
            thisMarker.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)" % (thisMarker.frame, thisMarker.label, thisMarker.id) )
            self.layout_markers.addWidget(thisMarker)




    def loadFromFile(self):
        '''load buttons from a json file'''


    def setFrame(self):
        '''set the frame in nuke when marker is clicked'''
        # nuke.frame(thisSender.frame)
        thisSender = self.sender()
        print "%s | %s | %s" % (thisSender.id, thisSender.frame, thisSender.label)



app = QtWidgets.QApplication(sys.argv)
p = Core_TimelineMarker()
p.show()
p.raise_()
app.exec_()
