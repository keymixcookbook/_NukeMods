# BackDrop Contents
# By Nathan Rusch
# Updated April 11, 2010

import nuke

def bdContents():
	'''
	Returns all the nodes contained in all selected Backdrop nodes.
	'''
	if not nuke.selectedNodes("BackdropNode"):
		return
	bdNodes = nuke.selectedNodes("BackdropNode")
	bdRanges = []
	for bd in bdNodes:
		left = bd.xpos()
		top = bd.ypos()
		right = left + bd['bdwidth'].value()
		bottom = top + bd['bdheight'].value()
		bdRanges.append((left, right, top, bottom))
	inNodes = []
	for node in nuke.allNodes():
		if node.Class() == "Viewer":
			continue
		for r in bdRanges:
			if node.xpos() > r[0] and node.xpos() + node.screenWidth() < r[1] and node.ypos() > r[2] and node.ypos() + node.screenHeight() < r[3]:
				inNodes.append(node)
				break
	return inNodes