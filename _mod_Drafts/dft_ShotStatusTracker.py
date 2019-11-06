#import nuke, nukescripts
import json, sys
from Qt import QtWidgets, QtGui, QtCore




class StatusBox(QtWidgets.QComboBox):
    '''
    source: https://stackoverflow.com/questions/3241830/qt-how-to-disable-mouse-scrolling-of-qcombobox
    '''
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(StatusBox, self).__init__(*args, **kwargs)
        self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            QtGui.QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            try:
                self.scrollWidget.wheelEvent(*args, **kwargs)
            except:
                pass



class Main_ShotStatusTracker(QtWidgets.QDialog):
    def __init__(self):
        super(Main_ShotStatusTracker,self).__init__()

        self.bt_reload = QtWidgets.QPushButton('Reload')
        self.bt_reload.clicked.connect(self.onReload)
        self.bt_save = QtWidgets.QPushButton('Save')
        self.bt_save.clicked.connect(self.onSave)
        self.core = Core_ShotStatusTracker()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout_button = QtWidgets.QHBoxLayout()
        self.layout_button.setAlignment(QtCore.Qt.AlignLeft)
        self.layout_button.addWidget(self.bt_reload)
        self.layout_button.addWidget(self.bt_save)

        self.layout.addWidget(self.core)
        self.layout.addLayout(self.layout_button)
        self.resize(800,500)
        self.setLayout(self.layout)


    def getCellValue(self, core_obj, idx_r, idx_c, column):
        '''gets the value for current cell, if cell type differ from cell to cell'''

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

        out_path = '/Users/Tianlun/Desktop/_NukeTestScript/doc/ShotStatusTracker_Datasets_onSave.json'
        core = self.core
        allRow = core.rowCount()
        allColumn = core.columnCount()
        column = core.ls_header

        ls_out = []

        for r in range(allRow): # row
            idx_r = r
            dic_row = {} # resets column value for every row
            for idx_c, c in enumerate(column): # column
                dic_row[c] = self.getCellValue(core, idx_r, idx_c, c)
            ls_out.append(dic_row)
        print ls_out
        with open(out_path, 'w') as f:
            f.write(json.dumps(ls_out,indent=2))

        print "data save to json"


    def onReload(self):
        '''when reload button is pressed'''
        print "data load from json"


    def run(self):
        '''run panel instance'''
        self.show()
        self.activateWindow()
        self.raise_()


class Core_ShotStatusTracker(QtWidgets.QTableWidget):
    def __init__(self):
        super(Core_ShotStatusTracker, self).__init__()

        self.data = self.getData()
        self.ls_header = ['SHOT', 'TASK', 'VERSION','STATUS','COMMENTS', 'NOTES']
        self.ls_status = ['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']
        self.task_completer = QtWidgets.QCompleter(['comp', 'mastercomp', 'precomp-'])
        self.resize(800,500)
        self.setShowGrid(False)
        self.setSortingEnabled(False)
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.ls_header))
        self.setHorizontalHeaderLabels(self.ls_header)
        # for i, h in enumerate(self.ls_header):
        #     self.setHorizontalHeaderItem(i,QtWidgets.QTableWidgetItem(h))
        self.horizontalHeader().setStretchLastSection(True)

        self.setColumnWidth(0,125)
        self.setColumnWidth(1,150)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,100)
        self.setColumnWidth(4,150)

        self.setDefault()

    def setDefault(self):
        '''set default value when instancing'''

        self.setTable(self.getData())


    def setTable(self, data):
        '''populating table with data'''

        def int2str(int):
            '''convert integer to string'''
            return "v%03d" % int

        for r, c in enumerate(data):
            #r: row number, c: data for this row - 'SHOT', 'TASK', 'VERSION', 'COMMENTS', 'NOTES'
            # self.setRowHeight(r,24)
            for i, d in enumerate(self.ls_header):
                # i: column index, d: column title
                # SHOT: String | TASK: String with completer | VERSION: Integer | COMMENTS: String | NOTES: String
                thisData, thisCell = None, None
                if d=='SHOT':
                    thisData = c[d]
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.setItem(r, i, thisCell)
                elif d=='TASK':
                    thisData = c[d]
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    self.setItem(r, i, thisCell)
                elif d=='VERSION':
                    thisData = int2str(c[d])
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.setItem(r, i, thisCell)
                elif d=='STATUS':
                    thisData = c[d]
                    thisCell = StatusBox()
                    # thisCell.setStyleSheet("QComboBox::down-arrow {border: 1px; image: none}")
                    # thisCell.insertSeparator(0)
                    thisCell.addItems(self.ls_status)
                    thisCell.setCurrentIndex(thisCell.findText(thisData))
                    self.setCellWidget(r, i, thisCell)
                elif d=='COMMENTS':
                    thisData = c[d]
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    thisCell.setToolTip(thisData)
                    self.setItem(r, i, thisCell)
                elif d=='NOTES':
                    thisData = c[d]
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    thisCell.setToolTip(thisData)
                    self.setItem(r, i, thisCell)
        self.setAlternatingRowColors(True)




    def getData(self):
        '''get data from json file'''
        file_path = '/Users/Tianlun/Desktop/_NukeTestScript/doc/ShotStatusTracker_Datasets.json'
        with open(file_path, 'r') as f:
            data = json.load(f)

        return data



# Show the panel


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ShotStatusTracker = Main_ShotStatusTracker()
    ShotStatusTracker.run()
    app.exec_()
else:
    ShotStatusTracker = Main_ShotStatusTracker()
    ShotStatusTracker.run()
