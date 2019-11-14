def _version_():
    ver='''

    version 0.0
    - Dockable nuke widget to set current frame
    - left-click to set frame, right-click to remove button
    - display current SHOW and SHOT (if ENV variable is set up)
    - can save, reload and load file from a JSON dataset

    '''
    return ver


import nuke, nukescripts



try:
    import nuke, nukescripts
except:
    pass
from Qt import QtWidgets, QtGui, QtCore
import sys, time, os, json




########## SUPPORTING FUNCTION/CLASS ##########





def set_widget_margins_to_zero(widget_object):

    if widget_object:
        target_widgets = set()
        target_widgets.add(widget_object.parentWidget().parentWidget())
        target_widgets.add(widget_object.parentWidget().parentWidget().parentWidget().parentWidget())

        for widget_layout in target_widgets:
            try:
                widget_layout.layout().setContentsMargins(0, 0, 0, 0)
            except:
                pass




class MarkerButton(QtWidgets.QPushButton):
    def __init__(self, id, frame, label):
        super(MarkerButton, self).__init__()

        self.id = id
        self.frame = frame
        self.label = label

        # self.setFixedWidth(48)

class MarkerAdd(QtWidgets.QDialog):
    '''
    GUI for adding markers
    data to be stored:frame, tooltip, id(<SHOW>-<timestamp>, PHX-12345678)
    '''
    def __init__(self, layout_obj, frame):
        super(MarkerAdd, self).__init__()

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
        self.m_add.clicked.connect(self.confirm)

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


    def confirm(self):
        '''add button'''
        thisFrame = int(self.m_frame.text().replace('x', ''))
        thisId = int(time.time())
        thisLabel = self.m_label.text()
        thisMarker = MarkerButton(thisId, thisFrame, thisLabel)
        self.thisLayout.addWidget(thisMarker)
        self.close()




########## MAIN FUNCTION/CLASS ##########




class Core_TimelineMarker(QtWidgets.QWidget):
    def __init__(self):
        super(Core_TimelineMarker, self).__init__()

        self.data_file = self.getJSONPath()

        self.tx_shot = QtWidgets.QLabel()
        self.bt_add = QtWidgets.QPushButton(u"\u002B")
        self.bt_add.clicked.connect(self.addMarker)
        self.bt_add.setStyle(QtGui.QFont().setBold(True))
        self.bt_remove = QtWidgets.QPushButton(u"\u2212")
        self.bt_remove.clicked.connect(self.removeMarker)
        self.bt_remove.setStyle(QtGui.QFont().setBold(True))
        self.bt_save = QtWidgets.QPushButton('save')
        self.bt_save.setToolTip("Save Current Markers")
        self.bt_save.clicked.connect(self.saveMarkers)
        self.bt_reload = QtWidgets.QPushButton('reload')
        self.bt_reload.setToolTip("Reload Markers from Loaded File")
        self.bt_reload.clicked.connect(self.reloadMarkers)
        self.bt_reloadFile = QtWidgets.QPushButton('reload from file')
        self.bt_reloadFile.clicked.connect(self.loadFromFile)
        self.bt_reloadFile.setToolTip("Load Markers from selected File")

        self.bt_add.setFixedWidth(50)
        self.bt_remove.setFixedWidth(50)
        self.bt_add.setFlat(True)
        self.bt_remove.setFlat(True)
        self.bt_save.setFlat(True)
        self.bt_reload.setFlat(True)
        self.bt_reloadFile.setFlat(True)


        self.layout_editMarkers = QtWidgets.QGridLayout()
        self.layout_editMarkers.setContentsMargins(0,0,0,0)
        self.layout_editMarkers.setSpacing(0)
        self.layout_editMarkers.addWidget(self.tx_shot,0,0)
        self.layout_editMarkers.addWidget(self.bt_add,0,2)
        self.layout_editMarkers.addWidget(self.bt_remove,0,3)

        self.layout_markers = QtWidgets.QHBoxLayout()
        self.layout_markers.setSpacing(0)
        self.group_markers = QtWidgets.QGroupBox()
        self.group_markers.setContentsMargins(0,0,0,0)
        self.group_markers.setLayout(self.layout_markers)

        self.layout_reload = QtWidgets.QGridLayout()
        self.layout_reload.setContentsMargins(0,0,0,0)
        self.layout_reload.setSpacing(0)
        self.layout_reload.addWidget(self.bt_save, 0,0)
        self.layout_reload.addWidget(self.bt_reload, 0,1)
        self.layout_reload.addWidget(self.bt_reloadFile, 0,2)

        self.layout_master = QtWidgets.QHBoxLayout()
        self.layout_master.setContentsMargins(10,0,10,0)
        self.layout_master.setSpacing(0)
        self.layout_master.addLayout(self.layout_editMarkers)
        self.layout_master.addSpacerItem(QtWidgets.QSpacerItem(10,10))
        self.layout_master.addWidget(self.group_markers)
        self.layout_master.addStretch()
        self.layout_master.addLayout(self.layout_reload)

        self.setLayout(self.layout_master)
        self.resize(1000,50)
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


    def setMarkerButtonAttributes(self, marker_obj):
        '''set MarkerButton attributes'''
        '''label, tooltip, left-click set frame, right-click remove'''

        label_button = marker_obj.label if len(marker_obj.label)<=5 else marker_obj.label[:5]+'...'
        marker_obj.setText(label_button)
        marker_obj.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)<br><br><i>Right-Click to Remove</i>" % (marker_obj.frame, marker_obj.label, marker_obj.id) )

        marker_obj.clicked.connect(self.setFrame)
        marker_obj.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        marker_obj.customContextMenuRequested.connect(self.removeMarker_RClicked)


    def addMarker(self):
        '''add MarkerButton widget'''

        try:
            frame = nuke.frame()
        except:
            frame = 1001

        self.p = MarkerAdd(self.layout_markers, frame)
        self.p.exec_()

        newWidget = self.layout_markers.itemAt(self.layout_markers.count()-1).widget()
        self.setMarkerButtonAttributes(newWidget)

        self.saveMarkers()


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
                self.setMarkerButtonAttributes(thisMarker)

                self.layout_markers.addWidget(thisMarker)

            jsonfile_show = os.path.basename(os.path.dirname(self.data_file))
            jsonfile_shot = os.path.basename(self.data_file).split('_TMDataset.json')[0]

            self.tx_shot.setText('%s: <b>%s</b>' % (jsonfile_show, jsonfile_shot))
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
        thisSender = self.sender()
        try:
            nuke.frame(thisSender.frame)
        except:
            pass
        print "%s | %s | %s" % (thisSender.id, thisSender.frame, thisSender.label)


    def event(self, event):
        if event.type() == QtCore.QEvent.Type.Show:

            try:
                set_widget_margins_to_zero(self)
            except:
                pass

        return QtWidgets.QWidget.event(self, event)



try:
    nukescripts.registerWidgetAsPanel('mod_TimelineMarker.Core_TimelineMarker', 'TimelineMarker','uk.co.thefoundry.TimelineMarker')
except:
    try:
        app = QtWidgets.QApplication(sys.argv)
        p = Core_TimelineMarker()
        p.show()
        p.raise_()
        app.exec_()
    except:
        p = Core_TimelineMarker()
        p.show()
        p.raise_()
