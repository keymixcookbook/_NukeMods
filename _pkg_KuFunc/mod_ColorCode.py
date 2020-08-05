def _version_():
	ver='''

	version 2.1
	- replace html tag for note_font_size with integer number

	version 2.0
	- more Color options (Random)
	- Header Size options

	version 1.0
	- Fixing error when cancel nuke panel
	- Fixing Default value of backdrop label
	- Output -> Transform

	version 0
	- Inherit nukescripts.autobackdrop()
	- Adding Color Scheme selection buttons for groups:
	- Groups include: CG, Plate, Grade, Key, Despill, Output, 2D Elem, Ref, End Comp, Precomp

	'''
	return ver




import nuke, nukescripts, math
from kputl import hsv2rgb, nukeColor




########## Supporting Function ##########




def colorButtons(bd, hex_group, blk):
	'''create ColorCode buttons
	@bd: backdrop node (obj)
	@hex_group: color scheme (dic {'type': [font (hex), tile (hex), button (hex)]})
	@blk: black color (str)
	'''
	## Inherit from:
	## (https://github.com/mb0rt/Nuke-NodeHelpers/blob/master/mbort/backdrop_palette/backdrop.py)

	# Create Knobs
	# Tab
	tab = nuke.Tab_Knob( 'Backdrop+ColorCode' )
	# Label
	label_link = nuke.Link_Knob( 'label_link', 'label' )
	label_link.makeLink( bd.name(), 'label' )
	# Font
	font_link = nuke.Link_Knob( 'note_font_link', 'font' )
	font_link.makeLink( bd.name(), 'note_font' )
	# Font Size
	font_size_link = nuke.Link_Knob( 'note_font_size_link', '' )
	font_size_link.makeLink( bd.name(), 'note_font_size' )
	font_size_link.clearFlag( nuke.STARTLINE )
	# font Color
	font_color_link = nuke.Link_Knob( 'note_font_color_link', 'font color' )
	font_color_link.makeLink( bd.name(), 'note_font_color' )
	font_color_link.clearFlag( nuke.STARTLINE )
	# Divider
	k_div = nuke.Text_Knob('')
	# add Tab
	bd.addKnob( tab )
	# Color Code
	counter = 0
	hex_group_keys = hex_group.keys()
	hex_group_keys.remove('*Random')

	for t in sorted(hex_group_keys):
		name = "bt_%s" % (t)
		label = "<font color='#%s'>%s</font> <b>%s" % (hex_group[t][2], blk, t)
		cmd = "n=nuke.thisNode();\
				n['tile_color'].setValue(int('%sFF',16));\
				n['note_font_color'].setValue(int('%sFF', 16));\
				n['note_font'].setValue('bold')" % (hex_group[t][1], hex_group[t][0])
		cc_knob = nuke.PyScript_Knob(name,label,cmd)
		cc_knob.setTooltip(t)
		# If First Item
		if counter == 0 or counter == 5:
			cc_knob.setFlag(nuke.STARTLINE)
		else:
			cc_knob.clearFlag(nuke.STARTLINE)
		bd.addKnob(cc_knob)

		counter += 1

	# Add Knobs
	bd.addKnob( k_div )
	bd.addKnob( label_link )
	bd.addKnob( font_link )
	bd.addKnob( font_size_link )
	bd.addKnob( font_color_link )




########## Main Function ##########




def ColorCode():
	'''main function'''
	# Symbols and Color
	blk = '&#9608;'
	hex_group = {
				'CG': ['CCC0C0', '5C3737', '7D5F5F'],
				'Key/Roto': ['C2CCC0', '3E5C37', '657d5f'],
				'Precomp': ['CAC0CC', '55375C', '775f7d'],
				'EndComp': ['CCCCCC', '5C5C5C', '7D7D7D'],
				'LensFX': ['C2C0CC', '3E375C', '655f7d'],
				'Transform': ['CCC7C0', '5C4625', '7D6B51'],
				'Despill': ['C0CCC5', '2E5C40', '587d66'],
				'Grade': ['C0CCCC', '2E5C5C', '587d7d'],
				'Elem2D': ['CACCC0', '535C2E', '757d58'],
				'Plate': ['BFC5CC', '2E405C', '58667d'],
				'*Random': []
				}

	# Main Function
	sel_class = []
	exclude_class = ['Dot', 'Merge2']
	for c in nuke.selectedNodes():
		if c.Class() not in exclude_class:
			sel_class.append(c.Class())

	try:
		most_class = max(set(sel_class), key=sel_class.count)
	except:
		most_class = 'NewBackdrop'

	bd = ku_autoBackdrop()

	if bd:

		p = nuke.Panel('ColorCode It')

		p.addEnumerationPulldown('Type: ', ' '.join(sorted(hex_group.keys())))
		p.addSingleLineInput('Label: ', most_class)
		p.addEnumerationPulldown('Font Size: ', 'h3 h2 h1')
		p.addBooleanCheckBox('center',False)

		if p.show():
			bd_type = p.value('Type: ')
			bd_label = p.value('Label: ')
			bd_font = p.value('Font Size: ')
			bd_center = p.value('center')
			dir_font = {'h1': 200, 'h2': 96, 'h1': 48}

			colorButtons(bd, hex_group, blk)

			# Execute a button on default
			if bd_type == '*Random':
				import random, math

				rand_h = random.randrange(0,360,10)
				rand_r, rand_g, rand_b = hsv2rgb(rand_h,.25,.36)

				bd.knob('tile_color').setValue(nukeColor(rand_r,rand_g,rand_b))
				bd.knob('note_font_size').setValue(dir_font[bd_font])
				bd.knob('note_font_color').setValue(nukeColor(int(rand_r*2),int(rand_g*2),int(rand_b*2)))
				setLabel = "<center>%s" % bd_label if bd_center == True else bd_label
				bd.knob('label').setValue(setLabel)
			else:
				bd.knob('bt_%s' % bd_type).execute()
				setLabel = "<center>%s" % bd_label if bd_center == True else bd_label
				bd.knob('label').setValue(setLabel)
			nuke.show(bd)

		else:
			nuke.delete(bd)
			print "Operation Cancelled"





########## Copy of nukescripts.autobackdrop() ##########




# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import nuke, random

def nodeIsInside (node, backdropNode):
  """Returns true if node geometry is inside backdropNode otherwise returns false"""
  topLeftNode = [node.xpos(), node.ypos()]
  topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
  bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
  bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(), backdropNode.ypos() + backdropNode.screenHeight()]

  topLeft = ( topLeftNode[0] >= topLeftBackDrop[0] ) and ( topLeftNode[1] >= topLeftBackDrop[1] )
  bottomRight = ( bottomRightNode[0] <= bottomRightBackdrop[0] ) and ( bottomRightNode[1] <= bottomRightBackdrop[1] )

  return topLeft and bottomRight

def ku_autoBackdrop():
  '''
  Automatically puts a backdrop behind the selected nodes.

  The backdrop will be just big enough to fit all the select nodes in, with room
  at the top for some text in a large font.
  '''
  selNodes = nuke.selectedNodes()
  if not selNodes:
	return nuke.nodes.BackdropNode()

  # Calculate bounds for the backdrop node.
  bdX = min([node.xpos() for node in selNodes])
  bdY = min([node.ypos() for node in selNodes])
  bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
  bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

  zOrder = 0
  selectedBackdropNodes = nuke.selectedNodes( "BackdropNode" )
  #if there are backdropNodes selected put the new one immediately behind the farthest one
  if len( selectedBackdropNodes ) :
	zOrder = min( [node.knob( "z_order" ).value() for node in selectedBackdropNodes] ) - 1
  else :
	#otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
	nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
	for nonBackdrop in selNodes:
	  for backdrop in nonSelectedBackdropNodes:
		if nodeIsInside( nonBackdrop, backdrop ):
		  zOrder = max( zOrder, backdrop.knob( "z_order" ).value() + 1 )

  # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
  left, top, right, bottom = (-80, -148, 80, 74)
  bdX += left
  bdY += top
  bdW += (right - left)
  bdH += (bottom - top)

  n = nuke.nodes.BackdropNode(xpos = bdX,
							  bdwidth = bdW,
							  ypos = bdY,
							  bdheight = bdH,
							  # tile_color = int((random.random()*(16 - 10))) + 10,
							  note_font_size=96,
							  z_order = zOrder,
							  tile_color = 808464639, # 19% gray, nuke DAG default color
							  )

  # revert to previous selection
  n['selected'].setValue(False)
  for node in selNodes:
	node['selected'].setValue(True)

  return n
