'''

version 3.0
- Fit to selection
- Select which `Backdrop` node to resize

version 2.0 (with mod_ColorCode)
- add color palatte, with html special characters and pyScript buttom

version 1.0
- Select Backdrop
- Enter Width and Height
- Select if From center or Side

'''


import nuke, nukescripts




########## Supporting Functions ##########




def bdFind(nodes):
	'''
	Finds the largest Backdrop node
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
	'''
	Filter out Backdrop node and calculate new size
	'''

	filter_bd.remove(node_bd)

	new_x = min([n.xpos() for n in filter_bd])
	new_y = min([n.ypos() for n in filter_bd])
	new_w = max([n.xpos() + n.screenWidth() for n in filter_bd]) - new_x
	new_h = max([n.ypos() + n.screenHeight() for n in filter_bd]) - new_y

	print new_x, new_y, new_w, new_h

	# Margin
	left, top, right, bottom = (-80, -148, 80, 74)
	new_x += left
	new_y += top
	new_w += (right - left)
	new_h += (bottom - top)

	print "Fit"
	print new_x, new_y, new_w, new_h
	return [new_x, new_y, new_w, new_h]



def bdSizeScale(node_bd, input_w, input_h, center):
	'''
	Resize with manual input values
	'''

	if center == False:
		cur_w = node_bd['bdwidth'].value()
		cur_h = node_bd['bdheight'].value()

		new_x = node_bd.xpos()
		new_y = node_bd.ypos()
		new_w = cur_w + float(input_w)*80
		new_h = cur_h + float(input_h)*74

	elif center == True:

		cur_x = node_bd.xpos()
		cur_y = node_bd.ypos()
		new_x = cur_x - float(input_w)*80/2
		new_y = cur_y - float(input_h)*74/2

	print "Scale"
	return [new_x, new_y, new_w, new_h]



def resize(node, new_size):
	'''
	Resize the `Backdrop`
	'''
	knobs = ['xpos', 'ypos', 'bdwidth', 'bdheight']
	for k in knobs:
		node[k].setValue(new_size[knobs.index(k)])




########## Main Function ##########




def BackdropResize():

	nodes = nuke.selectedNodes()

	if len(nodes)<=0:
		nuke.message("Select some nodes goddamnit")
		print "Abort"
	else:

		# Prompt
		p=nuke.Panel("Resize Backdrop")
		p.addBooleanCheckBox('Fit to Selection', True)
		p.addExpressionInput('Width by Node',0) # average node width: 80
		p.addExpressionInput('Height by Node',0) #average node height: 74
		p.addBooleanCheckBox('From Center', False)
		p.addButton('Cancel')
		p.addButton('Resize!')

		if p.show():

			input_w = p.value('Width')
			input_h = p.value('Height')
			input_c = p.value('From Center')
			f = p.value('Fit to Selection')

		# Find Biggest Backdrop node to resize
		node_bd = bdFind(nodes)

		# Fit to Selection
		if f == True:

			new_size = bdSizeFit(nodes, node_bd)

			resize(node_bd, new_size)
			print "%s Resized to Fit Selection" % node_bd.name()

		# Manual Scaling
		elif f == False:
			new_size = bdSizeScale(node_bd, input_w, input_h, input_c)

			resize(node_bd, new_size)
			print "%s Resized with input values" % node_bd.name()
