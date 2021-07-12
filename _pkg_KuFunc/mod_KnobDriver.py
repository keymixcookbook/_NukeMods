'''

Setting Driver and Driven Knobs

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
from Qt import QtWidgets, QtGui, QtCore
import platform
import os
import re




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '1.0'
__OS__			= platform.system()
__AUTHOR__		= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "KnobDriver v%s" % __VERSION__


def _version_():
	ver='''

	version 1.0
    - beta version
	- Create driver controls and stores driven knobs in Tooltip in '-nodename.knob' format
	- Driver controls includes:
		- SLIDER (Double_Knob)
		- RGBA (AColor_Knob)
		- XY (XY_Knob)
		- XYZ (XYZ_Knob)
		- INT (Int_Knob)
	- Only matching knob types will be linked
	- Button to refresh or sync Driven List in each Driver Knob

	'''
	return ver




#-------------------------------------------------------------------------------
#-Global Variables
#-------------------------------------------------------------------------------




STR_PLUS = '<b style="color: lightgreen">+</b> {}'
STR_SETDRIVEN = '<b>-&lt;-'
STR_LISTDRIVEN = '<b>&#8801;'
STR_SYNC = '<p>&#8634;'
STR_CMD_SETUP = "import mod_KnobDriver\nreload(mod_KnobDriver)\nmod_KnobDriver.{}" 
DIR_TYPES = {
	'SLIDER': 'Double_Knob',
	'RGBA': 'AColor_Knob',
	'XY': 'XY_Knob',
	'XYZ': 'XYZ_Knob',
	'INT': 'Int_Knob',
	'BOOL': 'Boolean_Knob'
}

RE_D = re.compile('\d+')
CLASS_EQ = {
	'Double_Knob': ['Double_Knob', 'Array_Knob', 'AColor_Knob', 'WH_Knob', 'Scale_Knob'],
	'AColor_Knob': ['AColor_Knob'],
	'XY_Knob': ['XY_Knob'],
	'XYZ_Knob': ['XYZ_Knob'],
	'Int_Knob': ['Int_Knob'],
	'Boolean_Knob': ['Boolean_Knob']
}




#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




def get_master_driver():
	"""Get Master Driver Node, create one if not in DAG
	return: (obj) Master Driver Node
	"""

	node = nuke.toNode('MASTER_DRIVER')

	if not node:
		node = nuke.nodes.NoOp(name='MASTER_DRIVER')
		# Tab
		k_id = nuke.Tab_Knob('tb_id', 'MASTER_DRIVER')
		node.addKnob(k_id)
		# Driver Buttons
		build_driver_types('SLIDER', node, newline=True)
		build_driver_types('RGBA', node)
		build_driver_types('XY', node)
		build_driver_types('XYZ', node)
		build_driver_types('INT', node)
		build_driver_types('BOOL', node)
		k_sync = nuke.PyScript_Knob('sync', STR_SYNC)
		k_sync.clearFlag(nuke.STARTLINE)
		k_sync.setCommand(STR_CMD_SETUP.format('sync_list_driven()'))
		node.addKnob(k_sync)
		# Divider
		node.addKnob(nuke.Text_Knob('',''))
	
	node['note_font'].setValue('bold')
	node['note_font_size'].setValue(24)
	node['tile_color'].setValue(2047999)
	node['hide_input'].setValue(True)

	node.showControlPanel(forceFloat=True)
	return node




#-------------------------------------------------------------------------------
#-Button Functions
#-------------------------------------------------------------------------------




def add_driver(knobtype):
	"""Add a set driver knobs
	@knobtype: (str) Nuke Knob Type
	"""
	try:	
		dr_no = int(max([find_digit(k.name()) for k in nuke.thisNode().knobs() if k.name().startswith('dr')]) + 1)
	except:
		dr_no = 0

	label = nuke.getInput('Label this Driver')	
	if label: 
		k_this_name = 'dr%02d_%s' % (dr_no, label)
		k_this = eval("nuke.{}('')".format(knobtype))
		k_this.setName(k_this_name)
		k_this.setLabel(label)
		k_this.setFlag(nuke.STARTLINE)

		k_set_driven = nuke.PyScript_Knob('dr%02ddriven' % dr_no, STR_SETDRIVEN)
		k_set_driven.setCommand(STR_CMD_SETUP.format("set_driven('%s')" % k_this_name))
		k_set_driven.setTooltip(k_this_name)
		k_set_driven.clearFlag(nuke.STARTLINE)
		k_list_driven = nuke.PyScript_Knob('dr%02dlist' % dr_no, STR_LISTDRIVEN)
		k_list_driven.clearFlag(nuke.STARTLINE)
		k_list_driven.setCommand(STR_CMD_SETUP.format("show_list_driven('%s')" % k_this_name))
		k_list_driven.setTooltip(k_this_name)

		n = nuke.thisNode()
		n.addKnob(k_this)
		n.addKnob(k_set_driven)
		n.addKnob(k_list_driven)


def set_driven(driver_name):
	"""set the driven node.knob with selected nodes
	@driver_name: (str) Name of the driver knob to set expression with
	"""

	node_driver = nuke.thisNode()
	knob_driver = nuke.thisKnob().tooltip()
	driver_type = node_driver.knob(knob_driver).Class()

	with nuke.root():
		nodes_driven = nuke.selectedNodes()
		if node_driver in nodes_driven:
			nodes_driven.remove(node_driver)
	
	if nodes_driven == []:
		nuke.message("Select A Node in DAG")
	else:
		for n in nodes_driven:
			ls_knobs = [k for k in n.knobs() if n.knob(k).Class() in CLASS_EQ[driver_type]]
			ls_knobs = filter_knobs(ls_knobs)
			print(ls_knobs)
			panel = nuke.Panel(n.name())
			panel.addEnumerationPulldown('knob to drive: ', ' '.join(ls_knobs))
			if panel.show():
				k_sel = panel.value('knob to drive: ')
				if k_sel:
					n.knob(k_sel).setValue(node_driver[knob_driver].value())
					str_expr = '%s.%s' % (node_driver.name(), knob_driver)
					n.knob(k_sel).setExpression(str_expr)
					print('%s > %s' % (k_sel, str_expr))

					append_driven_knob(node_driver.knob(knob_driver), n.name(), k_sel)


def show_list_driven(driver_name):
	"""show the list of driven node.knob
	@driver_name: (str) Name of the driver knob to set expression with
	"""

	ls_driven = nuke.thisNode().knob(driver_name).tooltip().split('\n')
	for d in ls_driven:
		print(d.split('.'))


def sync_list_driven():
	"""sync driven list of each driver knob"""

	print("sync driven list of each driver knob")	




#-------------------------------------------------------------------------------
#-Supportin Functions
#-------------------------------------------------------------------------------



def append_driven_knob(knob_driver, node_driven, knob_driven):
	"""append node_driven.knob_driven to knob_driver's tooltip
	@knob_driver: (knob) driver knob object
	@node_driven: (str) name of the node being driven
	@knob_driven: (str) name of the knob being driven
	"""
	new_entry = '%s.%s' % (node_driven, knob_driven)
	ls = knob_driver.tooltip().split('\n')
	ls.append(new_entry)
	ls = sorted(list(dict.fromkeys(ls)))
	try: ls.remove('')
	except: pass
	knob_driver.setTooltip('\n'.join(ls))
	



def build_driver_types(driver, node, newline=False):
	"""Build Driver buttons
	@driver: (str) driver type of this node
	@node: (node) the node to add knob
	@newline=False: (bool) if the node create on a newline
	"""

	k_this = nuke.PyScript_Knob('driver_%s' % driver, STR_PLUS.format(driver))
	k_this.setCommand(STR_CMD_SETUP.format("add_driver('%s')" % DIR_TYPES[driver]))
	k_this.setTooltip(DIR_TYPES[driver])
	if not newline: k_this.clearFlag(nuke.STARTLINE)
	else: k_this.setFlag(nuke.STARTLINE)
	node.addKnob(k_this)


def find_digit(knobname):
	"""return interger from knob name
	@knobname: (str) Driven Knob Name with digit
	return: (int) Integer from Knob name
	"""

	return int(RE_D.search(k.name()).group())


def filter_knobs(ls_knobs):
	"""filter out unwanted layers
	@ls_knobs: (list of knob names)
	return: ls_knobs
	"""
	f = ['xpos', 'indicators', 'lifetimeEnd', 'ypos', 'postage_stamp_frame', 'lifetimeStart', 'note_font_size', 'note_font', 'note_font_color', 'enable']
	return [l for l in ls_knobs if l not in f]
		


# def get_driven_knob(driver):
# 	"""nuke panel to get knob to drive with driver
# 	@driver: (knob) Driver Knob
# 	return: (knob) knob driven
# 	"""