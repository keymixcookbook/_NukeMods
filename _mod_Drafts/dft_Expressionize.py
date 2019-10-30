import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import re


class Core_Expressionize(QtGui.QWidget):
    def __init__(self):
        super(Core_Expressionize, self).__init__()
        # set
        self.ls_layers = ['rgb', 'rgba', 'alpha']
        # define widgets
        self.mu_layers = QtGui.QComboBox('Layers')
        self.st_expr = QtGui.QLineEdit()
        self.ck_ch_r = QtGui.QCheckbox('r')
        self.ck_ch_g = QtGui.QCheckbox('g')
        self.ck_ch_b = QtGui.QCheckbox('b')
        self.ck_ch_a = QtGui.QCheckbox('alpha')
        self.ck_ch_f = QtGui.QCheckbox('all')
        self.ck_clamp = QtGui.QCheckbox('clamp')
        self.ck_invert = QtGui.QCheckbox('invert')

        self.ls_ch_layer = [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_ch_a]
        self.ls_wrapper = [self.ck_clamp, self.ck_invert]
        # define layouts
        self.layout_master = QtGui.QVBoxLayout()
        self.layout_channels = QtGui.QHBoxLayout()
        self.layout_wrappers = QtGui.QHboxLayout()
        # add widgets
        self.layout_master.addWidgets(self.mu_layers)
        self.layout_master.addWidgets(self.st_expr)
        for c in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b,self.ck_ch_a, self.ck_ch_f]:
            self.layout_channels.addWidgets(c)
        for w in [self.ck_clamp, self.ck_invert]:
            self.layout_wrappers.addWidgets(w)
        # set layouts
        self.layout_master.addLayout(self.layout_channels)
        self.layout_master.addLayout(self.layout_wrappers)
        self.setLayout(self.layout_master)
        self.resize(400,240)
        self.setWindowTitle("Expressionize")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)

        self.setDefault()


    def setDefault(self):
        '''set default value when instansing'''
        self.mu_layers.addItem(self.ls_layers)
        for k in [self.ck_ch_r, self.ck_ch_g, self.ck_ch_b, self.ck_ch_f, self.ck_clamp, self.ck_invert]:
            k.setChecked(False)
        self.ck_ch_a.setChecked(True)


    def getLayers(self):
        '''get layers from root'''
        self.mu_layers.clear()
        sel = nuke.selectedNode()
        self.ls_layers = nuke.layers(sel) if sel else nuke.layers()
        self.mu_layers.addItem(self.ls_layers)

        return self.mu_layers # ['rgba', 'Id06']


    def getSelected(self):
        '''get values for the checkboxs and comboboxs'''
        sel_layer = self.mu_layers.currentText() # 'Id06'
        for idx,c in enumerate(self.ls_ch_layer):
            if c.isChecked():
                sel_channel.append('expr%s' % idx) # ['expr1', 'expr2']
        for w in self.ls_wrapper:
            if w.isChecked():
                sel_wrapper.append(w.text()) # ['clamp', 'invert']

        return sel_layer, sel_channel, sel_wrapper


    def setExpr(self, node, sel_layer, sel_channel, sel_wrapper):
        '''get string from expression line edit'''
        knob_to_ch = {'expr0':'red', 'expr1': 'green', 'expr2': 'blue', 'expr3': 'alpha'}

        expr_input = self.st_expr.text()
        expr_mid = expr_input
        expr_mid = '1-(%s)' % expr_mid if 'invert' in sel_wrapper else expr_mid
        expr_mid = 'clamp(%s)' % expr_mid if 'clamp' in sel_wrapper else expr_mid
        expr_output = expr_mid

        key_layer = '_lyr'
        key_channel = '_ch'

        for k in sel_channel:
            thisExpr = re.sub(key_layer,sel_layer, expr_output)
            thisExpr = re.sub(key_channel, knob_to_ch[k], expr_output)
            node[k].setValue(thisExpr)





# set instanse
Expressionize = Core_Expressionize()