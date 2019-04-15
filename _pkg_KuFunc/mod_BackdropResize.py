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
	all_bd = nuke.selectedNodes('BackdropNode')
	nodes_class = [c.Class() for c in nodes]

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



def bdSize(nodes):
	'''
	Filter out Backdrop node and calculate new size
	'''

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

	return [new_x, new_y, new_w, new_h]



def resize(node, new_size):
	'''
	Resize the Backdropnode
	'''
	knobs = ['xpos', 'ypos', 'bdwidth', 'bdheight']
	for k in knobs:
		node[k].setValue(new_size[knobs.index(k)])




########## Main Function ##########




def BackdropResize():

	nodes = nuke.selectedNodes()

	if len(nodes)<=0:
		nuke.message("Select some nodes goddamnit")
		print "Operation Cancelled"
	else:

		node_bd = bdFind(nodes)
		new_size = bdSize(nodes)

		resize(node_bg, new_size)
		print "%s Resized" % node_bd.name()




########## Old Function ###########




'''
def BackdropResize():

	node_backdrop = nuke.selectedNodes('BackdropNode')

	if len(node_backdrop)>0:

		p=nuke.Panel("Resize Backdrop")
		p.addExpressionInput('Width by Node',1) # average node width: 80
		p.addExpressionInput('Height by Node',1) #average node height: 74
		p.addBooleanCheckBox('From Center', True)
		p.addButton('Cancel')
		p.addButton('Resize!')

		if p.show():

			w = p.value('Width')
			h = p.value('Height')
			c = p.value('From Center')

			def bdsizing(n):
				cur_w = n['bdwidth'].value()
				cur_h = n['bdheight'].value()

				new_w = cur_w + float(w)*80
				new_h = cur_h + float(h)*74

				return [new_w, new_h]

			if c == False:
				for n in node_backdrop:
					n['bdwidth'].setValue(bdsizing(n)[0])
					n['bdheight'].setValue(bdsizing(n)[1])
			else:
				for n in node_backdrop:

					cur_c_x = n.xpos()
					cur_c_y = n.ypos()

					# Setting New Size
					n['bdwidth'].setValue(bdsizing(n)[0])
					n['bdheight'].setValue(bdsizing(n)[1])

					# Find new Position Point
					new_c_x = cur_c_x-float(w)*80/2
					new_c_y = cur_c_y-float(h)*74/2

					# Setting new Position Point
					n['xpos'].setValue(new_c_x)
					n['ypos'].setValue(new_c_y)
	else:
		nuke.message("Please Select a Backdrop Node")
'''
