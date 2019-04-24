
'''
- Select a Node
- Copy the Node and expression link knobs

- Two or More Nodes selected
- Expression link knobs to the last selected Node

'''




import nuke,nukescripts




########## Supporting Function ##########




def link(sel, clone_nodes, exclude_knobs):

	for c in clone_nodes:
		for k in sel.knobs():
			if k in exclude_knobs:
				pass
			else:
				c.knob(k).setExpression("%s.%s" % (sel.name(),k))




########## Main Function ##########




def LinkClone():
	exclude_knobs = ['xpos', 'ypos', 'autolabel', 'selected', 'onCreate', 'label']

	sel_node = nuke.selectedNodes()

	if len(sel_node) == 1:

		sel = nuke.selectedNode()

		node_create = "nuke.nodes.%s()" % (sel.Class())
		clone_node = eval(node_create)

		clone_node.setXpos(sel.xpos()+80)
		clone_node.setYpos(sel.ypos()+74)

		link(sel, [clone_node], exclude_knobs)

		clone_node['label'].setValue("linked: %s" % (sel.name()))

	elif len(sel_node) > 1:
		sel = sel_node[0]
		clone_node = sel_node[1:]

		link(sel, clone_node, exclude_knobs)

		for c in clone_node:
			c['label'].setValue("linked: %s" % (sel.name()))
