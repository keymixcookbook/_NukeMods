import nuke, nukescripts
import json, sys
try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtWidgets

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets




class Core_ShotStatusTracker(QtWidgets.QTableWidget):
    def __init__(self):
        super(Core_ShotStatusTracker, self).__init__()

        self.data = self.getData()
        self.ls_header = ['SHOT', 'TASK', 'VERSION','STATUS','COMMENTS', 'NOTES']
        self.ls_status = ['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']
        self.task_completer = QtWidgets.QCompleter(['comp', 'mastercomp', 'precomp-'])
        self.resize(800,500)
        # self.setShowGrid(False)
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

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setDefault()

    def setDefault(self):
        '''set default value when instancing'''

        self.setTable(self.getData())


    def setTable(self, data):
        '''populating table with data'''

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
                    thisData = c[d]
                    thisCell = QtWidgets.QTableWidgetItem(thisData)
                    thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.setItem(r, i, thisCell)
                elif d=='STATUS':
                    thisData = c[d]
                    thisCell = QtWidgets.QComboBox()
                    thisCell.setStyleSheet("QComboBox::down-arrow {border: 1px; image: none}")
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

    def run(self):
        '''run panel instance'''
        self.show()
        self.activateWindow()
        self.raise_()


# Show the panel


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ShotStatusTracker = Core_ShotStatusTracker()
    ShotStatusTracker.run()
    app.exec_()
else:
    ShotStatusTracker.run()
