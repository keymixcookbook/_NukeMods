'''

Transfer Knob Values from one script to another with the node of the same name

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
import platform
import os
from Qt import QtWidgets, QtGui, QtCore
import json
from kputl import joinPath
from kplogger import log, col



#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__='0.0 beta'
__OS__=platform.system()
__MODNAME__= "KnobTransfer"
__AUTHOR__="Tianlun Jiang"
__WEBSITE__="jiangovfx.com"
__COPYRIGHT__="copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)
__TITLE__=__MODNAME__ + ' v' + __VERSION__


def _version_():
	ver='''

	version 1.0
    - Transfer Knob Values from one script to another with the node of the same name


	'''
	return ver




# ------------------------------------------------------------------------------
# Global Variable
# ------------------------------------------------------------------------------



# Environment Variable for Show and Shot
ENV_SHOW = os.getenv('KP_SHOW', 'SHOW')
ENV_SHOT = os.getenv('KP_SHOT', 'SHOT')

log.setLevel(10)




#-------------------------------------------------------------------------------
#-Core Class
#-------------------------------------------------------------------------------




class Core_KnobTransfer(QtWidgets.QWidget):
	def __init__(self):
		super(Core_KnobTransfer, self).__init__()

		# Define Widgets
		self.title = QtWidgets.QLabel("<b>%s</b>" % (__TITLE__))
		self.env = QtWidgets.QLabel("%s:<b>%s</b>" % (ENV_SHOW, ENV_SHOT))
		self.btn_append_sel = QtWidgets.QPushButton("Append Selected Node")
		self.btn_append_sel.setToolTip("Append selected node name and knobs value to current shot tab\n(update node if already existed)")
		self.btn_update_sel = QtWidgets.QPushButton("Update Selected Nodes")
		self.btn_update_sel.setToolTip("Update knobs value for selected nodes in the dag to current shot tab")
		self.btn_update_all = QtWidgets.QPushButton("Update All Nodes")
		self.btn_update_all.setToolTip("Update knobs value for all in the current shot tab")
		self.btn_show_current_shot = QtWidgets.QPushButton("Show Current Shot")
		self.btn_save = QtWidgets.QPushButton("Save")
		self.btn_save.setToolTip("Save all shot tabs to file")
		self.btn_reload = QtWidgets.QPushButton("Reload")
		self.btn_reload.setToolTip("Reload all shot tabs from file")
		self.help = QtWidgets.QPushButton(u"\uFF1F")
		self.help.setStyleSheet("font-weight: bold")
		self.help.setMaximumWidth(48)

		## Define TabWidgets
		self.tab_shots = KT_TabWidget()

		## Signals and Slots
		self.btn_show_current_shot.clicked.connect(self.tab_shots.show_current_shot_tab)

		# Define Layouts
		self.layout_master = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout_master)
		self.layout_header = QtWidgets.QHBoxLayout()
		self.layout_nodes = QtWidgets.QHBoxLayout()
		self.layout_widgetfunc = QtWidgets.QHBoxLayout()
		
		# Assign Widgets to Layouts
		self.layout_header.addWidget(self.title)
		self.layout_header.addStretch()
		self.layout_header.addWidget(self.env)
		self.layout_nodes.addWidget(self.btn_append_sel)
		self.layout_nodes.addWidget(self.btn_update_sel)
		self.layout_nodes.addWidget(self.btn_update_all)
		self.layout_nodes.addWidget(self.btn_show_current_shot)
		self.layout_nodes.addWidget(self.help)
		self.layout_widgetfunc.addWidget(self.btn_save)
		self.layout_widgetfunc.addWidget(self.btn_reload)

		self.layout_master.addLayout(self.layout_header)
		self.layout_master.addWidget(divider())
		self.layout_master.addLayout(self.layout_nodes)
		self.layout_master.addWidget(self.tab_shots)
		self.layout_master.addLayout(self.layout_widgetfunc)

		self.setWindowTitle(__TITLE__)
		self.setMaximumWidth(1000)
		self.resize(200,500)
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

	def run(self):
		"""Main Run function"""
		self.show()

	def add_shot_tab(self, shot):
		"""add shot to tab widget
		@shot: (str) shot name
		return: (obj) Widget for newly created tab"""

		_tab = self.tab_shots
		_thisTab = KT_ShotTab(shot, self.tab_shots)
		_tab.addTab(_thisTab, shot)

		log.info("Tab created for shot: %s" % shot)

		return _thisTab




# ------------------------------------------------------------------------------
# KT Widgets
# ------------------------------------------------------------------------------



class KT_TabWidget(QtWidgets.QTabWidget):
	"""KnobTransfer Tab Widget"""
	def __init__(self):
		super(KT_TabWidget, self).__init__()



	def get_shot_names(self):
		"""get names of all tabs
		return: (list of str) list of shot names
		"""
		return [self.tabText(t) for t in range(self.count())]

	def get_shot_tabs(self):
		"""get tab widget of all shots
		return: (dict) {'shotname': tab_obj}
		"""
		return dict( [self.tabText(t), self.widget(t)] for t in range(self.count()) )

	def show_current_shot_tab(self):
		"""make tab of the current shot visiable"""

		for t in range(self.count()):
			if self.tabText(t) == ENV_SHOT:
				self.setCurrentIndex(t)
				break


class KT_ShotTab(QtWidgets.QWidget):
	"""KnobTransfer Widget for Shot per tab
	@shot: (str) shot name for this tab
	@parent: (obj) main tab object
	"""
	def __init__(self, shot, parent=None):
		super(KT_ShotTab, self).__init__()

		self.shot = shot
		self.shotstab = parent
		self.setToolTip(self.shot)

		self.instruction = QtWidgets.QLabel("Click on the buttons to set knob values")
		self.group = QtWidgets.QGroupBox()
		self.group.setFlat(True)

		self.layout_scroll = QtWidgets.QVBoxLayout()
		self.layout_scroll.setContentsMargins(0,0,0,0)
		self.group.setLayout(self.layout_scroll)
		self.layout_master = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout_master)

		self.scroll = QtWidgets.QScrollArea()
		self.scroll.setWidget(self.group)
		self.scroll.setWidgetResizable(True)
		# self.scroll.setFixedHeight(500)
		self.scroll.setStyleSheet("QGroupBox, QScrollArea {border: 0px}")

		for w in range(15):
			self.layout_scroll.addWidget(QtWidgets.QPushButton(str(w)))

		self.layout_master.addWidget(self.instruction)
		self.layout_master.addWidget(self.scroll)

	def get_shot(self):
		"""get the name of the shot"""
		return self.shot

	def get_layout(self):
		"""returns the layout obj that contains the widgets"""
		return self.layout

	def get_nodes(self):
		"""returns a list of PushButton widgets inside the layout
		return: (dict) {'button_names': obj}
		"""

		dict_nodes = {}

		for w in self.layout.count():
			_thisWidget = self.layout.itemAt(_thisWidget)
			if isinstance(_thisWidget, KT_NodeGroupButton):
				dict_nodes[_thisWidget.text()] = _thisWidget
				

class KT_NodeGroupButton(QtWidgets.QPushButton):
	"""KnobTransfer Widget for node
	@group_name: (str) name of the node group
	@dict_nodes: (dict) {'node_name': "knobvalues"}
	"""
	def __init__(self, group_name, dict_nodes):
		super(KT_NodeGroupButton, self).__init__()

		self.group_name = group_name
		self.dict_nodes = dict_nodes

		self.setText(self.group_name)

	def transfer_knobvalues(self):
		"""Transfer knob values to the node of the same name in the script"""

		pass


class divider(QtWidgets.QFrame):
	def __init__(self):
		super(divider, self).__init__()
		self.setFrameShape(QtWidgets.QFrame.HLine)
		self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.setMaximumHeight(9)


# ------------------------------------------------------------------------------
# Instancing
# ------------------------------------------------------------------------------




KnobTransfer = Core_KnobTransfer()

if log.level <= 10:

	KnobTransfer.add_shot_tab('ism0030')
	KnobTransfer.add_shot_tab('ism0010')
	KnobTransfer.add_shot_tab('ism0020')


	log.debug(KnobTransfer.tab_shots.get_shot_names())

else:
	nukescripts.panels.registerWidgetAsPanel('mod_KnobTransfer.Core_KnobTransfer', 'KnobTransfer', 'jiangvfx.com.KnobTransfer')

