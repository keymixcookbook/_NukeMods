try:
    import nuke, nukescripts
except:
    pass
import json, sys, os
from Qt import QtWidgets, QtGui, QtCore



def getTooltip(version, commments, notes):
    '''set tooltips'''
    return "<b>v%03d</b><br><br>%s<br>------<br>NOTES: <b>%s</b>" % (version,commments,notes)



def int2str(int):
    '''convert integer to string'''
    return "v%03d" % int



def setCell(obj_table, d, r, c, i):
    '''
    set cell value
    obj_table: QTableWidget, d: data, r: row, c: column value, i: column index
    '''

    thisData, thisCell = None, None
    if c=='SHOT':
        thisData = d[c]
        thisCell = QtWidgets.QTableWidgetItem(thisData)
        thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
        obj_table.setItem(r, i, thisCell)
    elif c=='TASK':
        thisData = d[c]
        thisCell = QtWidgets.QTableWidgetItem(thisData)
        thisCell.setToolTip(getTooltip(d['VERSION'],d['COMMENTS'],d['NOTES']))
        obj_table.setItem(r, i, thisCell)
    elif c=='VERSION':
        thisData = int2str(d[c])
        thisCell = QtWidgets.QTableWidgetItem(thisData)
        thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
        obj_table.setItem(r, i, thisCell)
    elif c=='STATUS':
        thisData = d[c]
        thisCell = StatusBox()
        thisCell.addItems(obj_table.ls_status)
        thisCell.setCurrentIndex(thisCell.findText(thisData))
        obj_table.setCellWidget(r, i, thisCell)
    elif c=='COMMENTS':
        thisData = d[c]
        thisCell = QtWidgets.QTableWidgetItem(thisData)
        thisCell.setToolTip(thisData)
        obj_table.setItem(r, i, thisCell)
    elif c=='NOTES':
        thisData = d[c]
        thisCell = QtWidgets.QTableWidgetItem(thisData)
        thisCell.setToolTip(thisData)
        obj_table.setItem(r, i, thisCell)


def setTable(obj_table, data, ls_header):
    '''
    populating table with data
    obj_table: QTableWidget, data: JSON data, ls_header: header columns
    '''

    print "%s entries" % len(data)

    for r, d in enumerate(data):
        #r: row number, d: data for this row - 'SHOT', 'TASK', 'VERSION', 'COMMENTS', 'NOTES'
        # self.setRowHeight(r,24)
        for i, c in enumerate(ls_header):
            # i: column index, c: column title
            # SHOT: String | TASK: String with completer | VERSION: Integer | COMMENTS: String | NOTES: String
            setCell(obj_table,d,r,c,i)



class StatusBox(QtWidgets.QComboBox):
    '''
    source: https://stackoverflow.com/questions/3241830/qt-how-to-disable-mouse-scrolling-of-qcombobox
    '''
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(StatusBox, self).__init__(*args, **kwargs)

        #['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']
        self.colorCode = {
            'FARM':     (195 ,  75,  100),
            'RENDERED': (125 ,  75,  100),
            'VIEWED':   (248 ,  50,  50),
            'DAILIED':  (248 ,  75,  100),
            'NOTED':    (53  ,  75,  100),
            'SENT':     (30  ,  100, 100),
            'FINAL':    (80  ,  100, 100)
            }

        self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.currentIndexChanged.connect(self.setColorCode)


    def setColorCode(self):
        thisColor = self.colorCode[self.currentText()]
        self.setStyleSheet('''
            QComboBox {background: hsv(%s,%s,%s); color: white;}
            QComboBox QAbstractItemView {background: hsv(0,0,25); selection-background-color: hsv(0,0,50); color: hsv(0,0,75)}
            ''' % thisColor)


    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            QtGui.QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            try:
                self.scrollWidget.wheelEvent(*args, **kwargs)
            except:
                pass



class VersionBox(QtWidgets.QSpinBox):
    def __init__(self):
        super(VersionBox, self).__init__()
        self.valueChanged.connect(self.zeroPadding)
        self.setFixedWidth(60)
        self.setRange(0,999)
    def zeroPadding(self):
        input_len = len(str(self.value()))
        if input_len <= 3:
            self.setPrefix('v%s' % ('0'*(3-input_len)))
        else:
            self.setPrefix('v')



class DataAdd(QtWidgets.QDialog):
    def __init__(self, core, thisRow, ls_shots):
        '''
        core: QTableWidget
        thisRow: index for the new row
        '''
        super(DataAdd, self).__init__()

        self.core = core
        self.thisRow = thisRow
        self.ls_shots = ls_shots

        self.st_shot = QtWidgets.QComboBox()
        # self.st_shot.setPlaceholderText('Shot (ie. str050_1010)')
        # self.st_shot.setCompleter(QtWidgets.QCompleter(ls_shots))
        self.st_shot.addItems(self.ls_shots)
        self.st_shot.setEditable(True)
        self.st_task = QtWidgets.QLineEdit()
        self.st_task.setPlaceholderText('Task (ie. mastercomp)')
        self.st_task.setCompleter(QtWidgets.QCompleter(['comp', 'mastercomp','precomp-']))
        self.no_version = VersionBox()
        self.no_version.setValue(1)
        self.bx_status = QtWidgets.QComboBox()
        self.bx_status.addItems(self.core.ls_status)
        self.st_comments = QtWidgets.QLineEdit()
        self.bt_add = QtWidgets.QPushButton('ADD')
        self.bt_add.clicked.connect(self.onClicked)

        self.layout_master = QtWidgets.QVBoxLayout()
        self.layout_version = QtWidgets.QHBoxLayout()
        self.layout_version.addWidget(self.st_shot)
        self.layout_version.addWidget(self.st_task)
        self.layout_version.addWidget(self.no_version)
        self.layout_version.addWidget(self.bx_status)
        self.layout_master.addLayout(self.layout_version)
        self.layout_master.addWidget(self.st_comments)
        self.layout_master.addWidget(self.bt_add)
        self.setLayout(self.layout_master)
        self.setWindowTitle("Add a version: entry %s" % self.thisRow)


    def onClicked(self):
        '''collect data from GUI and assign to variables'''

        entry = {}

        thisShot, thisTask, thisVersion, thisStatus, thisComments = None, None, None, None, None

        thisShot = self.st_shot.currentText()
        thisTask = self.st_task.text()
        thisVersion = int(self.no_version.text().replace('v',''))
        thisStatus = self.bx_status.currentText()
        thisComments = self.st_comments.text()
        entry['SHOT']=thisShot
        entry['TASK']=thisTask
        entry['VERSION']=thisVersion
        entry['STATUS']=thisStatus
        entry['COMMENTS']=thisComments
        entry['NOTES']=""

        for i,c in enumerate(self.core.ls_header):
            setCell(self.core, entry, self.thisRow, c, i)

        print "added\n---SHOT: %s\n---TASK: %s\n---VERSION: %s\n---STATUS: %s\n---COMMENTS: %s" % (thisShot, thisTask, thisVersion, thisStatus, thisComments)

        self.close()


class Main_ShotStatusTracker(QtWidgets.QDialog):
    def __init__(self):
        super(Main_ShotStatusTracker,self).__init__()

        self.core = Core_ShotStatusTracker()

        self.bt_reload = QtWidgets.QPushButton('Reload')
        self.bt_reload.clicked.connect(self.onReload)
        self.bt_save = QtWidgets.QPushButton('Save')
        self.bt_save.clicked.connect(self.onSave)
        self.bt_add = QtWidgets.QPushButton('Add')
        self.bt_add.clicked.connect(self.onAdd)
        self.bt_remove = QtWidgets.QPushButton('Remove')
        self.bt_remove.clicked.connect(self.onRemove)
        self.tx_show = QtWidgets.QLabel('<i>NO SHOW SET</i>')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10,0,10,0)
        self.layout.setSpacing(0)
        self.layout_button = QtWidgets.QHBoxLayout()
        self.layout_button.setAlignment(QtCore.Qt.AlignLeft)
        self.layout_button.addWidget(self.bt_add)
        self.layout_button.addWidget(self.bt_remove)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.tx_show)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.bt_reload)
        self.layout_button.addWidget(self.bt_save)

        self.layout.addWidget(self.core)
        self.layout.addLayout(self.layout_button)
        self.resize(800,500)
        self.setLayout(self.layout)
        self.setWindowTitle("Shot Status Tracker - beta")

        self.core.cellChanged.connect(self.onUpdateCells)

        try:
            self.tx_show.setText('<b>%s</b>' % os.path.basename(self.core.json_file_path).split('_')[0])
        except:
            print "No Show Set"



    def closeEvent(self, event):
        '''save on close'''
        self.onSave()
        print 'save and closed'



    def getCellValue(self, core_obj, idx_r, idx_c, column):
        '''
        gets the value for current cell, if cell type differ from cell to cell
        core_obj: QTableWidget
        idx_r: row index
        idx_c: column index
        column: Header name (use to get cellTypes)
        '''

        cellTypes={'SHOT': 'item', 'TASK': 'item', 'VERSION': 'integer', 'STATUS': 'combo', 'COMMENTS': 'item', 'NOTES': 'item'}

        val_cell = None

        if cellTypes[column] == 'item':
            val_cell = core_obj.item(idx_r,idx_c).text()
        elif cellTypes[column] == 'integer':
            val_cell = int(core_obj.item(idx_r,idx_c).text().replace('v',''))
        elif cellTypes[column] == 'combo':
            val_cell = core_obj.cellWidget(idx_r,idx_c).currentText()
        return val_cell


    def onSave(self):
        '''when save button is pressed'''

        core = self.core
        out_path = core.json_file_path
        allRow = core.rowCount()
        allColumn = core.columnCount()
        column = core.ls_header

        ls_out = []

        try:
            for r in range(allRow): # row
                idx_r = r
                dic_row = {} # resets column value for every row
                for idx_c, c in enumerate(column): # column
                    dic_row[c] = self.getCellValue(core, idx_r, idx_c, c)
                ls_out.append(dic_row)

                with open(out_path, 'w') as f:
                    f.write(json.dumps(ls_out,indent=2))
        except:
            pass


        # print "data save to json: %s entries" % len(ls_out)


    def onReload(self):
        '''when reload button is pressed'''
        core = self.core
        data = core.getData(core.json_file_path)
        core.setRowCount(len(data))
        setTable(core, data, core.ls_header)
        self.tx_show.setText('<b>%s</b>' % os.path.basename(core.json_file_path).split('_')[0])




    def onAdd(self):
        '''add data entry'''
        core = self.core
        core.setRowCount(core.rowCount()+1)
        thisRow = core.rowCount()-1
        ls_shots_all = [self.getCellValue(core, r, 0, 'SHOT') for r in range(core.rowCount()-1)]
        ls_shots = list(dict.fromkeys(ls_shots_all))
        self.d = DataAdd(core, thisRow, ls_shots)
        self.d.exec_()


    def onRemove(self):
        '''remove data of the last row'''
        core = self.core
        core.setRowCount(core.rowCount()-1)


    def onUpdateCells(self):
        '''update cells when changed'''
        core = self.core
        cur_r = core.currentRow()
        cur_c = core.currentColumn()

        if core.ls_header[cur_c] == 'COMMENTS' or core.ls_header[cur_c] == 'NOTES':
            thisItem = core.item(cur_r,cur_c)
            thisItem.setToolTip(thisItem.text())

            try:
                row_verion = self.getCellValue(core, cur_r, core.ls_header.index('VERSION'), 'VERSION')
                row_comments = self.getCellValue(core, cur_r, core.ls_header.index('COMMENTS'), 'COMMENTS')
                row_notes = self.getCellValue(core, cur_r, core.ls_header.index('NOTES'), 'NOTES')
                thisTask = core.item(cur_r, 1)
                thisTask.setToolTip(getTooltip(row_verion,row_comments,row_notes)) # version, commments, notes
            except:
                pass
        self.onSave()


    def run(self):
        '''run panel instance'''
        self.show()
        self.activateWindow()
        self.raise_()


class Core_ShotStatusTracker(QtWidgets.QTableWidget):
    def __init__(self):
        super(Core_ShotStatusTracker, self).__init__()

        self.json_file_path = self.getJSONPath()

        self.data = self.getData(self.json_file_path)
        self.ls_header = ['SHOT', 'TASK', 'VERSION','STATUS','COMMENTS', 'NOTES']
        self.ls_status = ['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']
        self.resize(800,500)
        self.setShowGrid(False)
        self.setSortingEnabled(False)
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.ls_header))
        self.setHorizontalHeaderLabels(self.ls_header)
        # for i, h in enumerate(self.ls_header):
        #     self.setHorizontalHeaderItem(i,QtWidgets.QTableWidgetItem(h))
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)

        self.setColumnWidth(0,125)
        self.setColumnWidth(1,150)
        self.setColumnWidth(2,70)
        self.setColumnWidth(3,100)
        self.setColumnWidth(4,150)
        self.setColumnWidth(5,150)

        self.setDefault()


    def setDefault(self):
        '''set default value when instancing'''
        setTable(self, self.getData(self.json_file_path), self.ls_header)


    def getData(self, json_file_path):
        '''get data from json file'''
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        except:
            data = []
            print "No SSTDataset file"

        return data


    def getJSONPath(self):
        '''
        reutrn file path for the json file
        Naming convension:
        <HOME Dir>/.nuke/ShotStatusTracker/<SHOW>_SSTDataset.json
        /Users/Tianlun/.nuke/TimelineMarker/PHX_SSTDataset.json
        '''
        # Get pipline enviroment variables
        data_SHOW = os.getenv('PL_SHOW') if os.getenv('PL_SHOW') else 'KUHQ'

        data_folder = os.path.join(os.getenv('HOME'), '.nuke','ShotStatusTracker')
        data_filename = "%s_SSTDataset.json" % data_SHOW
        data_file = os.path.join(data_folder, data_SHOW, data_filename)

        if not os.path.isdir(os.path.dirname(data_file)):
            os.makedirs(os.path.dirname(data_file))

        return data_file

try:
    nukescripts.registerWidgetAsPanel('mod_ShotStatusTracker.Main_ShotStatusTracker', 'Shot Status Tracker','uk.co.thefoundry.ShotStatusTracker')
except:
    try:
        app = QtWidgets.QApplication(sys.argv)
        #['bb10dark', 'bb10bright', 'cleanlooks', 'cde', 'motif', 'plastique', 'Windows', 'Fusion']
        # app.setStyle('Plastique')
        ShotStatusTracker = Main_ShotStatusTracker()
        ShotStatusTracker.run()
        app.exec_()
    except:
        ShotStatusTracker = Main_ShotStatusTracker()
        ShotStatusTracker.run()
