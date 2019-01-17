'''

version 1.0
- Select Backdrop
- Enter Width and Height
- Select if From center or Side

version 2.0 (WIP)
- add color palatte, with html special characters and pyScript buttom

'''


import nuke, nukescripts


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
