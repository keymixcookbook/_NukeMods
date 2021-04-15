def _version_():
	ver='''

	version 0
	- create a grain channel shuffle setup for every merge node

	'''
	return ver





import nuke, nukescripts




########## Supporting Functions ##########




def defaultValue():

	node_color = 1163603199 # Dark Green
	spacing = (80,74)
	ch_grain = 'grain'

	return node_color, spacing, ch_grain

def collect(nodes):
	'''
	Collect `Merge` nodes data
	'''

	nodes_merge = []

	for n in nodes:
		m_A = n.dependencies(nuke.INPUTS)[1]
		nodes_merge.append([n, m_A])


	return nodes_merge



def cal(nodes_merge):
	'''
	Calculate A pipe side and `Merge` nodes position
	'''

	for n in nodes_merge:
		this_merge = n[0]
		m_A = n[1]

		condition = this_merge.xpos() - m_A.xpos()
		m_ASide = -1 if condition > 0 else 1 # -1: left; 1: right

		m_pos = (this_merge.xpos(), this_merge.ypos())

		n.extend([m_ASide, m_pos])


	return nodes_merge



def nodeInsert(node_parent, node_toInsert):

	for n in node_parent.dependent():

		for idx,i in enumerate(n.dependencies(),0):
			if i==node_parent:
				n.setInput(idx, node_toInsert)
			else:
				pass



def grainBuild(nodes_merge):
	'''
	Build Grain nodes set up
	'''

	node_color, spacing, ch_grain = defaultValue()
	nuke.Layer(ch_grain, ["%s.red", "%s.green", "%s.blue", "%s.alpha"])
	console = []
	grain_merge = []

	for n in nodes_merge:
		base_node, m_A, m_ASide, m_pos = n
		spacing = (80,74)
		node_color = 1163603199 # Dark Green
		node_connected = base_node.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS)

		# Create Nodes


		## Dot node
		node_dot = nuke.nodes.Dot(
							inputs=[m_A],
							tile_color=node_color
							)
		node_dot_diff = (node_dot.screenHeight() - base_node.screenHeight())/2
		if m_ASide<0:
			node_dot.setXpos(m_pos[0] + spacing[0] * m_ASide)
		else:
			node_dot.setXpos(m_pos[0] + base_node.screenWidth() + spacing[0] * m_ASide)

		node_dot.setYpos(m_pos[1] - node_dot_diff)
		base_node.setInput(1, node_dot)


		## Shuffle node
		node_shuffle = nuke.nodes.Shuffle(
							inputs=[node_dot],
							tile_color=node_color,
							label = '[value out]'
							)
		node_shuffle.hideControlPanel()
		node_shuffle_diff = (node_dot.screenWidth() - node_shuffle.screenWidth())/2
		node_shuffle.setXpos(node_dot.xpos() + node_shuffle_diff)
		node_shuffle.setYpos(node_dot.ypos() + spacing[1])
		node_shuffle['in'].setValue('alpha')
		node_shuffle['out'].setValue(ch_grain)


		## Merge node
		node_grainMerge = nuke.nodes.Merge2(
							inputs=[base_node, node_shuffle],
							tile_color=node_color,
							operation='screen',
							Achannels='alpha',
							Bchannels='grain',
							output=ch_grain
							)
		node_grainMerge.hideControlPanel()
		node_grainMerge.setXpos(base_node.xpos())
		node_grainMerge.setYpos(node_shuffle.ypos())

		nodeInsert(base_node, node_grainMerge)

		console.append(base_node.name())
		grain_merge.append(node_grainMerge)


	print "Grain Channel set up for\n%s" % console

	# if len(console_fail)>0:
	#     print "Grain Channel fail to set up for\n%s" % console_fail
	# else:
	#     pass

	return grain_merge



def grainEnd(nodes_merge):
	'''
	Build Grain nodes at the end to shuffle out
	'''

	pos_merge = {}
	node_color, spacing, ch_grain = defaultValue()

	for y in nodes_merge:
		pos_merge[y.ypos()]=y.name()

	last_merge = nuke.toNode(pos_merge[max(pos_merge.keys())])

	end_dot = nuke.nodes.Dot(
						inputs=[last_merge],
						tile_color=node_color
						)
	end_dot_diff = int(end_dot.screenWidth()/2 - last_merge.screenWidth()/2)
	end_dot.setXpos(last_merge.xpos() - end_dot_diff)
	end_dot.setYpos(last_merge.ypos() + spacing[1]*2)

	nodeInsert(last_merge, end_dot)

	end_shuffle = nuke.nodes.Shuffle(
							inputs=[end_dot],
							tile_color=node_color,
							label='[value in]>[value out]'
							)
	end_shuffle.setXpos(end_dot.xpos() - spacing[0]*2)
	end_shuffle.setYpos(end_dot.ypos() + spacing[1])
	end_shuffle['in'].setValue(ch_grain)
	end_shuffle['out'].setValue('rgba')

	return None




########## Main Functions ##########




def GrainChannel(mode='all'):

	nodes = nuke.selectedNodes('Merge2')

	if len(nodes)<=0:
		nuke.message('Select a Merge node gaddamnit')
	else:
		nodes_merge = cal(collect(nodes))

		if mode == 'all':

			grain_merge = grainBuild(nodes_merge)
			grainEnd(grain_merge)

			print "Grain Channel all Setup"

		elif mode == 'end':

			grainEnd(nodes)

			print "Grain to Alpha"
