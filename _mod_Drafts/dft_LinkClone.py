import nuke,nukescripts, python

'''
- Select a Node
- Copy the Node and expression link knobs

- Two or More Nodes selected
- Expression link knobs to the last selected Node

'''

exclude_knobs = ['xpos', 'ypos', 'autolabel', 'selected', 'onCreate', 'label']

sel_node = nuke.selectedNodes()

if len(sel_node) == 1:

	sel = nuke.selectedNode()

	node_create = "nuke.nodes.%s()" % (sel.Class())
	clone_node = eval(node_create)

	clone_node.setXpos(sel.xpos()+80)
	clone_node.setYpos(sel.ypos()+74)

	for k in sel.knobs():
		if k in exclude_knobs:
			pass
		else:
			clone_node.knob(k).setExpression("%s.%s" % (sel.name(),k))

	clone_node['label'].setValue("linked: %s" % (sel.name()))