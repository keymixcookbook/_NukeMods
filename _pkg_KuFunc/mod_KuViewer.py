
'''

Set of functions associated with the Viewer node

'''


# ------------------------------------------------------------------------------
# -Module Import
# ------------------------------------------------------------------------------


import nuke
import nukescripts
import platform
import os
import logging




#-------------------------------------------------------------------------------
#-Logging
#-------------------------------------------------------------------------------




LOG = logging.getLogger("kplogger")




# ------------------------------------------------------------------------------
# -Header
# ------------------------------------------------------------------------------




__VERSION__ = '1.0'
__OS__ = platform.system()
__AUTHOR__ = "Tianlun Jiang"
__WEBSITE__ = "jiangovfx.com"
__COPYRIGHT__ = "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__ = "KuViewer v%s" % __VERSION__


def _version_():
	ver = '''

	version 1.0
	- Set node name to viewer input number
	- viewer menu with set and restore
	- nuke prefs for JSON and nuke pref

	'''
	return ver




# -------------------------------------------------------------------------------
# -GLOBAL VARIABLE
# -------------------------------------------------------------------------------




# Preference Default Values
PREF = ["Viewer Label", "StickyNote Node"]
PREF_NAME = 'mu_viewerinputs'
PREF_DEFAULT = PREF[0]
PREF_NODE = nuke.toNode('preferences')




# -------------------------------------------------------------------------------
# -Main Function
# -------------------------------------------------------------------------------


def KuViewer(mode='restore'):
	'''set and restore viewer input pipes with options
	mode='restore': restore set inputs
	mode='set': record exsisting inputs
	'''

	nuke_pref_check()

	node_viewer = nuke.activeViewer().node()
	node_viewer.setName('KuViewer')
	data_knob = None

	if PREF_NODE[PREF_NAME].value() == "Viewer Label":
		data_knob = node_viewer.knob('label')
		LOG.debug("Pref: Viewer Label")
	elif PREF_NODE[PREF_NAME].value() == "StickyNote Node":
		sticky_node = nuke.toNode("KuViewerInputs")
		if not sticky_node:
			sticky_node = nuke.createNode("StickyNote", "name KuViewerInputs")
		data_knob = sticky_node.knob('label')
		LOG.debug("Pref: StickyNote")
	else:
		nuke.warning("Preferences 'viewerinputs' value note valide")
		LOG.warning("No data_knob found")

	if data_knob: 
		if mode == 'set':
			num_inputs = node_viewer.inputs()
			data = ''
			for i in range(num_inputs):
				node_thisInput = node_viewer.input(i).name() if node_viewer.input(i) else None
				data += "%s:%s\n" % (i+1, node_thisInput)
			data_knob.setValue(data)
			LOG.debug("Set Viewer Inputs")

		if mode == 'restore':
			data = data_knob.value()
			ls_restore = [i.split(':') for i in data.split('\n')[:-1]]

			for n in ls_restore:
				node_viewer.setInput(int(n[0])-1, nuke.toNode(n[1]))
				LOG.info("%s:%s" % (n[0], n[1]))




# -------------------------------------------------------------------------------
# -Nuke Preferences
# -------------------------------------------------------------------------------




def nuke_pref_check():
	"""Adds and update nuke pref"""
	ls_menu = [
		['tb_kuviewer', 'KuViewer', None],
		[PREF_NAME, "KuViewer Inputs", PREF]
	]

	for k in ls_menu:
		k_name, k_label, k_value = k
		if not PREF_NODE.knob(k_name):
			if k_name.startswith('tb_'):
				k_toadd = nuke.Tab_Knob(k_name, k_label)
				PREF_NODE.addKnob(k_toadd)
			if k_name.startswith('mu_'):
				k_toadd = nuke.Enumeration_Knob(k_name, k_label, k_value)
				PREF_NODE.addKnob(k_toadd)




#-------------------------------------------------------------------------------
#-Debug
#-------------------------------------------------------------------------------




def debug():
	"""Simulate menu call"""
	LOG.propagate = False
	LOG.setLevel(logging.DEBUG)
	KuViewer(mode='restore')