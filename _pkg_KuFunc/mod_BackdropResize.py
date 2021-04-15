'''

Resize Backdrops

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

__TITLE__		= "BackdropResize v%s" % __VERSION__


def _version_():
	ver='''

	version 2.0
	- Fit to selection
	- Select which `Backdrop` node to resize

	version 1.0
	- Select Backdrop
	- Enter Width and Height
	- Select if From center or Side

	'''
	return ver




#-------------------------------------------------------------------------------
#-Main Functions
#-------------------------------------------------------------------------------




def BackdropResize():
	'''main function'''

	nodes = nuke.selectedNodes()

	if len(nodes) <= 0:
		nuke.message("Select some nodes goddamnit")
		print "Abort"
	elif len([b for b in nodes if b.Class() == 'BackdropNode']) <= 0:
		nuke.message("Gotta include a Backdrop Node, man")
		print "Abort"
	else:

		# Prompt
		p=nuke.Panel("Resize %s" % bdFind(nodes).name())
		p.addEnumerationPulldown('Mode', '"Fit to Selection" "Manual Scaling"')
		# p.addBooleanCheckBox('Fit to Selection', True)
		p.addButton('Cancel')
		p.addButton('Resize!')

		p.setWidth(len(p.title())*12)

		if p.show():

			mode_sel = p.value('Mode')

			# Find Biggest Backdrop node to resize
			node_bd = bdFind(nodes)

			# Fit to Selection
			if mode_sel == "Fit to Selection":

				new_size = bdSizeFit(nodes, node_bd)

				resize(node_bd, new_size)
				print "%s Resized to Fit Selection" % node_bd.name()

			# Manual Scaling
			elif mode_sel == "Manual Scaling":

				# Second Prompt
				psub = nuke.Panel("Resize %s" % bdFind(nodes).name())
				psub.addExpressionInput('Width',1) # average node width: 80
				psub.addExpressionInput('Height',1) #average node height: 74
				psub.addBooleanCheckBox('From Center', True)
				psub.addButton('Cancel')
				psub.addButton('Resize!')

				psub.setWidth(len(p.title())*12)

				if psub.show():

					input_w = psub.value('Width')
					input_h = psub.value('Height')
					input_c = psub.value('From Center')

					new_size = bdSizeScale(node_bd, input_w, input_h, input_c)

					resize(node_bd, new_size)
					print "%s Resized with input values" % node_bd.name()
		else:
			print "Operation Cancelled"
			
			
			

#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------




def bdFind(nodes):
	'''Finds the largest Backdrop node
	@nodes: nodes selected (list of objs)
	return: obj
	'''

	all_bd = [n for n in nodes if n.Class() == 'BackdropNode']

	if len(all_bd)<=0:
		nuke.message("Please include a Backdrop Node")
	else:

		all_bdSize = {}
		for b in all_bd:
			name = b.name()
			area = b['bdwidth'].value()*b['bdheight'].value()
			all_bdSize[area] = name

		node_bd = nuke.toNode(all_bdSize[max(all_bdSize.keys())])

		return node_bd


def bdSizeFit(nodes, node_bd):
	'''Filter out Backdrop node and calculate new size
	@nodes: selecteds nodes (list of objs)
	@node_bd: backdrop nodes (objs)
	return: [new_x, new_y, new_w, new_h] (list of ints)
	'''

	nodes.remove(node_bd)

	new_x = min([n.xpos() for n in nodes])
	new_y = min([n.ypos() for n in nodes])
	new_w = max([n.xpos() + n.screenWidth() for n in nodes]) - new_x
	new_h = max([n.ypos() + n.screenHeight() for n in nodes]) - new_y


	# Margin
	left, top, right, bottom = (-80, -148, 80, 74)
	new_x += left
	new_y += top
	new_w += (right - left)
	new_h += (bottom - top)

	print "Fit"
	return [new_x, new_y, new_w, new_h]


def bdSizeScale(node_bd, input_w, input_h, center):
	'''Resize with manual input values
	@node_bd: backdrop node (obj)
	@input_w: input width (int)
	@input_h: input height (int)
	@center: if scale from center (bool)
	return: [new_x, new_y, new_w, new_h] (list of ints)
	'''
	cur_x = node_bd.xpos()
	cur_y = node_bd.ypos()
	cur_w = node_bd['bdwidth'].value()
	cur_h = node_bd['bdheight'].value()

	if center == False:

		new_x = cur_x
		new_y = cur_y
		new_w = cur_w + float(input_w)*80
		new_h = cur_h + float(input_h)*74

	elif center == True:

		new_x = cur_x - float(input_w)*80/2
		new_y = cur_y - float(input_h)*74/2
		new_w = cur_w + float(input_w)*80
		new_h = cur_h + float(input_h)*74


	print "Scale"
	return [new_x, new_y, new_w, new_h]


def resize(node, new_size):
	'''Resize the Backdrop
	@node: backdrop node to resize (obj)
	@new_size: size value (list of int)
	'''
	knobs = ['xpos', 'ypos', 'bdwidth', 'bdheight']
	for k in knobs:
		node[k].setValue(new_size[knobs.index(k)])
