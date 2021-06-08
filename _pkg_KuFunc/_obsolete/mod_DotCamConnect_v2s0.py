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





#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '2.0'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "DotCamConnect v%s" % __VERSION__



def _version_():
	ver='''

	version 2.0
	- add button to open input node property panel

	version 1.0
	- Find A Camera nodes in nuke
	- List names of the ndoes in a menu
	- Select the node and Connect!
	- Hide the input, set the color to red and put the Camera Node name to Dot node's label

	'''
	return ver




#-------------------------------------------------------------------------------
#-Main Functions
#-------------------------------------------------------------------------------




def DotCamConnect():

	color_red = int('%02x%02x%02x%02x' % (1*255,0*255,0*255,0*255),16)
	color_white = int('%02x%02x%02x%02x' % (1*255,1*255,1*255,1*255),16)

	# Find All the Camera nodes
	node_ls_cam = [n.name() for n in nuke.allNodes('Camera2')]
	node_ls_cam.sort()

	# Set Connect Function OR setting Dot Node Function
	def setDotNode(d, node_sel_cam):

		d['label'].setValue("\n%s" % (node_sel_cam))
		d['note_font'].setValue('bold')
		d['note_font_size'].setValue(24)
		d['note_font_color'].setValue(color_white)
		d['tile_color'].setValue(color_red)
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

		print "%s -> %s" % (d.name(), node_sel_cam)

	# If there is a camera selected
	if len(nuke.selectedNodes('Camera2'))>0:

		for c in nuke.selectedNodes('Camera2'):

			nuke.selectedNode()['selected'].setValue(False)
			node_create_dot = nuke.createNode('Dot', inpanel=False)

			node_create_dot['xpos'].setValue(c['xpos'].value()+100)
			node_create_dot['ypos'].setValue(c['ypos'].value()+100)

			setDotNode(node_create_dot, c.name())

	# If there isn't a camera selected
	else:

		if len(node_ls_cam) > 1:
			'''prompt to select which camera to connect'''

			p = nuke.Panel('Select A Camera Node to Connect')
			p.addEnumerationPulldown('Cam to Connect', ' '.join(node_ls_cam))
			p.addButton('Cancel')
			p.addButton('Connect!')

			if p.show():

				node_sel_cam = p.value('Cam to Connect')

				# Detect if it's a selection or just create a Dot
				if len(nuke.selectedNodes('Dot'))>0:
					node_ls_dot = nuke.selectedNodes('Dot')

					for d in node_ls_dot:
						setDotNode(d,node_sel_cam)

				else:
					node_create_dot = nuke.createNode('Dot', inpanel=False)

					setDotNode(node_create_dot, node_sel_cam)
		
		elif len(node_ls_cam) == 1:
			'''connect the only camera in the script'''

			node_create_dot = nuke.createNode('Dot', inpanel=False)
			setDotNode(node_create_dot, node_ls_cam[0])

