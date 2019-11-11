from Qt import QtWidgets, QtGui, QtCore
import sys, time, os, json




########## SUPPORTING FUNCTION/CLASS ##########




class MarkerButton(QtWidgets.QPushButton):
    def __init__(self, id, frame, label):
        super(MarkerButton, self).__init__()

        self.id = id
        self.frame = frame
        self.label = label

        self.setMinimumWidth(48)
        self.setFixedHeight(48)


class MarkerAdd(QtWidgets.QDialog):
    '''
    GUI for adding markers
    data to be stored:frame, tooltip, id(<SHOW>-<timestamp>, PHX-12345678)
    '''
    def __init__(self, layout_obj, frame):
        super(MarkerAdd, self).__init__()

        # cur_frame = nuke.frame()
        cur_frame = frame
        self.thisLayout = layout_obj
        self.m_title_frame = QtWidgets.QLabel('Frame: ')
        self.m_title_label = QtWidgets.QLabel('Label: ')
        self.m_frame = QtWidgets.QSpinBox()
        self.m_frame.setMaximum(3000)
        self.m_frame.setPrefix('x')
        self.m_frame.setValue(cur_frame)
        self.m_label = QtWidgets.QLineEdit()
        self.m_label.setText('x%s' % cur_frame)
        self.m_label.setPlaceholderText("Keep it short")
        self.m_add = QtWidgets.QPushButton('Add Marker')
        self.m_add.clicked.connect(self.add)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.m_title_frame, 0,0, QtCore.Qt.AlignRight)
        self.layout.addWidget(self.m_frame, 0,1)
        self.layout.addWidget(self.m_title_label, 1,0, QtCore.Qt.AlignRight)
        self.layout.addWidget(self.m_label, 1,1)
        self.layout.addWidget(self.m_add,2,0,1,2)
        # self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Frame Marker")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.m_label.setFocus()
        self.m_label.selectAll()


    def add(self):
        '''add button'''
        thisFrame = int(self.m_frame.text().replace('x', ''))
        thisId = int(time.time())
        thisLabel = self.m_label.text()
        thisMarker = MarkerButton(thisId, thisFrame, thisLabel)
        # thisMarker.customContextMenuRequested.connect(Core_TimelineMarker.removeMarker)

        label_button = self.m_label.text() if len(self.m_label.text())<=5 else self.m_label.text()[:5]+'...'
        thisMarker.setText(label_button)
        thisMarker.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)" % (thisMarker.frame, thisMarker.label, thisMarker.id) )
        self.thisLayout.addWidget(thisMarker)
        self.close()




########## MAIN FUNCTION/CLASS ##########




class Core_TimelineMarker(QtWidgets.QWidget):
    def __init__(self):
        super(Core_TimelineMarker, self).__init__()

        self.data_file = self.getJSONPath()

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
        self.group_markers.setContentsMargins(0,0,0,0)
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
        self.layout_reload.setSpacing(0)

        self.layout_master.addLayout(self.layout_editMarkers)
        self.layout_master.addWidget(self.group_markers)
        self.layout_master.addStretch()
        self.layout_master.addLayout(self.layout_reload)
        self.setLayout(self.layout_master)
        self.setMinimumWidth(1000)
        self.setContentsMargins(0,0,0,0)

        self.reloadMarkers()


    def getJSONPath(self):
        '''
        reutrn file path for the json file
        Naming convension:
        <HOME Dir>/.nuke/TimelineMarker/<SHOW>/<SHOT>_TMDataset.json
        /Users/Tianlun/.nuke/TimelineMarker/PHX/str050_1010_TMDataset.json
        '''
        # Get pipline enviroment variables
        data_SHOW = os.getenv('PL_SHOW') if os.getenv('PL_SHOW') else 'KUHQ'
        data_SHOT = os.getenv('PL_SHOT') if os.getenv('PL_SHOT') else 'ku66_8686'

        data_folder = os.path.join(os.getenv('HOME'), '.nuke','TimelineMarker')
        data_filename = "%s_TMDataset.json" % data_SHOT
        data_file = os.path.join(data_folder, data_SHOW, data_filename)

        if not os.path.isdir(os.path.dirname(data_file)):
            os.makedirs(os.path.dirname(data_file))

        return data_file


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
        self.p = MarkerAdd(self.layout_markers, 1001)
        self.p.exec_()
        # add connect signal to the last widgets
        newWidget = self.layout_markers.itemAt(self.layout_markers.count()-1).widget()
        newWidget.clicked.connect(self.setFrame)
        newWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        newWidget.customContextMenuRequested.connect(self.removeMarker_RClicked)


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
            self.layout_markers.removeWidget(thisWidget)
            thisWidget.deleteLater()
        except:
            print "no markers to be removed"


    def reloadMarkers(self):
        '''reload from json file and rebuild MarkerButtons'''
        thisFile = self.data_file

        if not os.path.exists(thisFile):
            print "No TMDataset.json file found"
        else:
            # Clear Widgets
            num_widgets = self.layout_markers.count()
            all_widgets = [self.layout_markers.itemAt(n).widget() for n in range(num_widgets)]
            for w in all_widgets:
                self.layout_markers.removeWidget(w)
                w.deleteLater()
                print "Markers Removed: %s" % w.label

            # Find data
            thisData = []
            with open(self.data_file, 'r') as f:
                thisData = json.load(f)
            print "loaded: %s" % thisFile
            # Rebuild Widgets
            for w in thisData:
                thisFrame = w['frame']
                thisId = w['id']
                thisLabel = w['label']
                thisMarker = MarkerButton(thisId, thisFrame, thisLabel)

                label_button = thisLabel if len(thisLabel)<=5 else thisLabel[:5]+'...'
                thisMarker.setText(label_button)
                thisMarker.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)" % (thisMarker.frame, thisMarker.label, thisMarker.id) )
                thisMarker.clicked.connect(self.setFrame)
                thisMarker.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                thisMarker.customContextMenuRequested.connect(self.removeMarker_RClicked)
                self.layout_markers.addWidget(thisMarker)

            self.group_markers.setTitle('SHOT: ' + os.path.basename(self.data_file).split('_TMDataset.json')[0])
            print "Markers added: %s" % self.layout_markers.count()


    def loadFromFile(self):
        '''load buttons from a json file'''
        sel_json = QtWidgets.QFileDialog().getOpenFileName(self,"Select a TMDataset json file", os.path.join(os.getenv('HOME'), '.nuke'), 'JSON files (*.json)')[0]
        if sel_json:
            self.data_file = sel_json
            self.reloadMarkers()
        else:
            print "Inviald file path"


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
