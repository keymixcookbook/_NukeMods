

def DeepBookmark():
	for n in nuke.selectedNodes('DeepRecolor'):
		n.setSelected(False)
		d = nuke.nodes.Dot(tile_color=25344)
		d.setInput(0,n)
		d.setXpos(n.xpos()+n.screenWidth()/2-d.screenWidth()/2)
		d.setYpos(n.ypos()+100)


def DeepCollecting():
	'''
	Collects All the Deep in the comp
	Deep data need to go through a DeepRecolor Node
	'''
	deeps = [n for n in nuke.allNodes('Dot') if "toCollector" in n['label'].value()]

	deep_collector = nuke.selectedNode()

	counter = len(deeps)

	print "\n\n", "="*25, "Collecting Deeps", "="*25

	for n in range(counter):
	    counter -= 1 
	    deep_collector.setInput(n, deeps[n])
	    print "%s -> %s" % (deeps[n].name(),deep_collector.name())

	deep_collector['label'].setValue("DeepCollector")
	deep_collector['hide_input'].setValue(True)


def DeepCollector():
	'''
	- Find Dot Bookmark - dot_bookmark
	- Find Top Node - topnode
	- Find File base name without extensions - topnode_filename

	{topnode_filename: [dot_bookmark, topnode, counter]}

	- create a group
	- create the tabs and checkboxes with topnode_filename
	- inside the group, create Input, Switch and DeepMerge per tab
		- link value of the Switch to "parent.topnode_filename"
		- create output link to DeeoMerge
	- outside the group, setInput to dot_bookmark, with corresponding input number
	'''