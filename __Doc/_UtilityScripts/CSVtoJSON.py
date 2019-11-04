try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtWidgets

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets

import sys, os, csv, json


class Core_CSVtoJSON(QtWidgets.QFileDialog):
    def __init__(self):
        super(Core_CSVtoJSON, self).__init__()

        self.setWindowTitle("Select a CSV file")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def convert(self, sel_f):
        '''convert selected CSV to JSON'''

        f_name = sel_f.replace('.csv','.json')

        with open( sel_f, 'r' ) as c:
            reader = csv.DictReader(c)
            out = json.dumps( [ row for row in reader ], indent=4, sort_keys=True)
        with open(f_name, 'w') as j:
            j.write(out)
            print f_name

    def run(self):

        sel_f = self.getOpenFileName(self, "Select a CSV file",os.curdir,"CSV files (*.csv)")[0]
        if sel_f:
            self.convert(sel_f)
            print "File converted:"
        else:
            print "User Cancelled"
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    CSVtoJSON = Core_CSVtoJSON()
    CSVtoJSON.run()
    sys.exit(app.exec_())
