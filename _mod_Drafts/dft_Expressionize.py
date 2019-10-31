import nuke, nukescripts
try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtWidgets

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets
import re


class Core_Expressionize(QtWidgets.QWidget):
    def __init__(self):
        super(Core_Expressionize, self).__init__()
        # set
        self.ls_layers = ['rgb', 'rgba', 'alpha']
        # define widgets
        self.title = QtWidgets.QLabel("<b>Expressionize</b>")
        self.mu_layers = QtWidgets.QComboBox()
        self.st_expr = QtWidgets.QLineEdit()
        self.st_expr.returnPressed.connect(self.onPressed)
        self.st_expr.setCompleter(QtWidgets.QCompleter(['_lyr', '_lyr._ch', 'rgba']))
        self.ck_ch_r = QtWidgets.QCheckBox('r')
        self.ck_ch_g = QtWidgets.QCheckBox('g')
        self.ck_ch_b = QtWidgets.QCheckBox('b')
        self.ck_ch_a = QtWidgets.QCheckBox('alpha')
        self.bt_ch_all = QtWidgets.QPushButton('all')
        self.bt_ch_all.clicked.connect(self.setAllChannel)
        self.ck_clamp = QtWidgets.QCheckBox('clamp')
        self.ck_invert = QtWidgets.QCheckBox('invert')

        self.ls_ch_layer = [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_ch_a]
        self.ls_wrapper = [self.ck_clamp, self.ck_invert]
        # define layouts
        self.layout_master = QtWidgets.QVBoxLayout()
        self.layout_channels = QtWidgets.QHBoxLayout()
        self.layout_wrappers = QtWidgets.QHBoxLayout()
        # add widgets
        self.layout_master.addWidget(self.title)
        self.layout_master.addWidget(self.mu_layers)
        self.layout_master.addWidget(self.st_expr)
        for c in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b,self.ck_ch_a, self.bt_ch_all]:
            self.layout_channels.addWidget(c)
        for w in [self.ck_clamp, self.ck_invert]:
            self.layout_wrappers.addWidget(w)
        # set layouts
        self.layout_master.addLayout(self.layout_channels)
        self.layout_master.addLayout(self.layout_wrappers)
        self.setLayout(self.layout_master)
        #self.resize(400,240)
        self.setWindowTitle("Expressionize")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

        self.setDefault()


    def setDefault(self):
        '''set default value when instansing'''
        self.mu_layers.addItems(self.ls_layers)
        for k in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_clamp, self.ck_invert]:
            k.setChecked(False)
        self.ck_ch_a.setChecked(True)


    def setLayers(self,node_expr,node_sel):
        '''get layers from root'''
        self.mu_layers.clear()
        self.ls_layers = nuke.layers() if node_sel == None else nuke.layers(node_sel)
        self.mu_layers.addItems(self.ls_layers)

        return self.mu_layers # ['rgba', 'Id06']


    def getSelected(self):
        '''get values for the checkboxs and comboboxs'''
        sel_layer = self.mu_layers.currentText() # 'Id06'

        sel_channel, sel_wrapper = [],[]

        for idx,c in enumerate(self.ls_ch_layer):
            if c.isChecked():
                sel_channel.append('expr%s' % idx) # ['expr1', 'expr2']
        for w in self.ls_wrapper:
            if w.isChecked():
                sel_wrapper.append(w.text()) # ['clamp', 'invert']

        return [sel_layer, sel_channel, sel_wrapper]


    def setExpr(self, node, sel):
        '''get string from expression line edit'''

        sel_layer, sel_channel, sel_wrapper = sel

        knob_to_ch = {'expr0':'red', 'expr1': 'green', 'expr2': 'blue', 'expr3': 'alpha'}

        expr_in = self.st_expr.text()
        expr_mid = expr_in
        expr_mid = '1-(%s)' % expr_mid if 'invert' in sel_wrapper else expr_mid
        expr_mid = 'clamp(%s)' % expr_mid if 'clamp' in sel_wrapper else expr_mid
        expr_out = expr_mid

        key_layer = '_lyr'
        key_channel = '_ch'

        for k in sel_channel:
            expr_out = expr_out.replace(key_layer,sel_layer)
            expr_out = expr_out.replace(key_channel,knob_to_ch[k])
            node[k].setValue(expr_out)


    def onPressed(self):
        '''when enter-key is pressed on expression line edit'''
        self.setExpr(self.node, self.getSelected())
        self.close()


    def setAllChannel(self):
        for k in self.ls_ch_layer:
            k.setChecked(True)

    def getNode(self):
        '''find out the node_sel and node_expr'''

        sel = nuke.selectedNodes()
        node_sel, node_expr = None, None

        if len(sel)<=0:
            node_sel = nuke.toNode('root')
            node_expr = nuke.createNode('Expression')
        elif len(sel) == 1:
            if sel[0].Class() != 'Expression':
                node_sel = sel[0]
                node_expr = nuke.createNode('Expression')
            elif sel[0].Class() == 'Expression':
                node_expr = sel[0]
                node_sel = None

        print node_expr.name(), node_sel.name()
        return [node_expr, node_sel]

    def run(self):
        '''run the instance'''

        self.setDefault()
        self.setLayers(self.getNode()[0],self.getNode()[1])
        self.show()
        self.move(QtWidgets.QCursor.pos())







# set instanse
Expressionize = Core_Expressionize()