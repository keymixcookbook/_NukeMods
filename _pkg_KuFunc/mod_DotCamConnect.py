'''

Dot node to connect a camera

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import platform
import os
from Qt import QtWidgets, QtGui, QtCore
import nuke, nukescripts
import logging





#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '2.1'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "DotCamConnect v%s" % __VERSION__



def _version_():
	ver='''
	
	version 2.1
	- directly connect if only one camera in the script
	- Redorder codes

	version 2.0
	- add button to open input node property panel

	version 1.0
	- Find A Camera nodes in nuke
	- List names of the ndoes in a menu
	- Select the node and Connect!
	- Hide the input, set the color to red and put the Camera Node name to Dot node's label

	'''
	return ver




# ------------------------------------------------------------------------------
#-GLOBAL VARIABLE
# ------------------------------------------------------------------------------




CLASS_CAM = 'Camera2'
COL_RED = int('%02x%02x%02x%02x' % (1*255,0*255,0*255,0*255),16)
COL_WHITE = int('%02x%02x%02x%02x' % (1*255,1*255,1*255,1*255),16)





# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------




log = logging.getLogger('kplogger')




#-------------------------------------------------------------------------------
#-Main Functions
#-------------------------------------------------------------------------------




def DotCamConnect():

	# Find All the Camera nodes
	node_ls_cam = [n.name() for n in nuke.allNodes(CLASS_CAM)]
	node_ls_cam.sort()
	sel_node_dot = nuke.selectedNodes('Dot')
	sel_cam_node = get_camera(node_ls_cam)

	if sel_cam_node:

		# If a Dot node is selected
		if sel_node_dot != [] and node_ls_cam != []:
			for d in sel_node_dot:
				set_node_dot(d, sel_cam_node)
			return True 

		# if nothing is selected
		if nuke.selectedNodes() == []:
			node_create_dot = nuke.createNode('Dot', inpanel=False)
			set_node_dot(node_create_dot, sel_cam_node)
			return True
		



# ------------------------------------------------------------------------------
# Supporting Function
# ------------------------------------------------------------------------------




def set_node_dot(d, node_sel_cam):
	"""Set Connect Function OR setting Dot Node Function"""

	d['label'].setValue("\n%s" % (node_sel_cam))
	d['note_font'].setValue('bold')
	d['note_font_size'].setValue(24)
	d['note_font_color'].setValue(COL_WHITE)
	d['tile_color'].setValue(COL_RED)
	d['hide_input'].setValue(True)
	d.setInput(0, nuke.toNode(node_sel_cam))

	# Add Show Panel Knob
	cmd_ppanel = "n=nuke.thisNode()\ntry:\n\tn.input(0).showControlPanel(forceFloat=n.knob('isFloat').value())\nexcept:\n\tpass"
	cmd_orig = "origNode = nuke.thisNode().input(0);\
					origXpos = origNode.xpos();\
					origYpos = origNode.ypos();\
					nuke.zoom(2, [origXpos,origYpos]);\
					nuke.thisNode()['selected'].setValue(False);\
					origNode['selected'].setValue(True);\
					nuke.show(origNode)"
	t_tab = nuke.Tab_Knob('t_user', "DotCamConnect")
	k_showPanel = nuke.PyScript_Knob('ppanel', "Show Input Property Panel", cmd_ppanel)
	k_float = nuke.Boolean_Knob('isFloat', "Floating Panel", True)
	k_showCam = nuke.PyScript_Knob('orig', "Show Camera Node", cmd_orig)

	k_float.clearFlag(nuke.STARTLINE)
	k_float.setFlag(nuke.STARTLINE)

	d.addKnob(t_tab)
	d.addKnob(k_showPanel)
	d.addKnob(k_float)
	d.addKnob(k_showCam)

	print("%s -> %s" % (d.name(), node_sel_cam))


def get_camera(node_ls_cam):
	"""Prompt UI for camera selection
	@node_ls_cam: (list of camera node)
	return: (node) selected camera node, None if cancel or no camera in DAG
	"""
	
	node_sel_cam = None

	if len(node_ls_cam) > 1:

		p = nuke.Panel('Select A Camera Node to Connect')
		p.addEnumerationPulldown('Cam to Connect', ' '.join(node_ls_cam))
		p.addButton('Cancel')
		p.addButton('Connect!')

		if p.show():
			node_sel_cam = p.value('Cam to Connect')
		else:
			node_sel_cam = None

	elif len(node_ls_cam) == 1:
		node_sel_cam = node_ls_cam[0]	

	return node_sel_cam