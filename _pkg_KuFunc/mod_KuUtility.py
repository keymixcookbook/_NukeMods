'''

mod_KuFunc.py for _NukeStudio & _NukeFreelance
to used in both a VFX Studio and Freelance enviroment

originally KuFunc.py

Contain sets of 'Light Weight' Functions, shouldn't be longer than 50 lines

'''


import nuke, os, nukescripts, sys



########## GLOBAL KU FUNCTIONS ##########




def ku_knobCh (node, knob, val):
	node[knob].setValue(val)

def ku_knobVal (node, knob):
	return node[knob].value()

def settingCh(knob, val):
	nuke.root()[knob].setValue(val)
	print "{knob} set to {value}".format(knob=knob, value=val)

def nukeColor(r,g,b,a):
	return int('%02x%02x%02x%02x' % (r * 255, g * 255, b * 255, a * 255), 16)

def knobFlagClear(knob):
	if knob.getFlag(nuke.STARTLINE) == True:
		knob.clearFlag(nuke.STARTLINE)
	else:
		return knob




########## NODE GRAPH FUNCTIONS ##########




def mask():
	for n in nuke.selectedNodes():
		if n != 0:
			mk = n.optionalInput()
			n.setInput(mk, nuke.selectedNodes()[0])


def reloadRead():

	#Define Functions
	def reload(node,node_list):
		node['reload'].execute()
		node_list.append("%s Reloaded" % (node.name()))

	#Define Variables

	read_sel = nuke.selectedNodes('Read')
	reload_list = []

	#Reloading

	if len(read_sel)>0: #if there are Read node Selectred
		for s in read_sel:
			if s.Class() == "Read":
				reload(s,reload_list)

	elif len(nuke.allNodes('Read'))>0: #if there are Read Node Enabled
		for e in nodes_read:
			if e['disable'] == False:
				reload(e,reload_list)

	else:
		nuke.message("No Read Nodes to Reload")

	print '\n, '"="*25, '\n'
	print "\n".join(reload_list)
	print '\n, '"="*25, '\n'


def showFileDir():

	nodes = nuke.allNodes('Read')

	print "========== FILES ==========", "\n\n"

	for n in nodes:
		print '------  ', n.name() , " -> ",n['file'].value(), "\n", "__________"

	print "\n\n", "========== END FILES =========="


def resetNodeCol():
	aNode = []

	for n in nuke.allNodes():
		if n.Class() == "Grade" or n.Class() == "Merge2" or n.Class() == "Keymix":
			n['tile_color'].setValue(0)
			aNode.append(n.name())

	nuke.message('Reseted Color For: ' + '\n' + str(', '.join(aNode)))


def groupConnect():
	sel = nuke.selectedNodes()

	for n in nuke.selectedNodes():
		if n != 0:
			n.setInput(0, sel[0])  # Connecting the A pipe


def selectiveCache():
	lst = []

	# Storing Shit in an Array
	for n in nuke.allNodes('DiskCache'):
		lst.append(n.name())

	# Panels
	p = nuke.Panel('Tree 2 Cache')
	p.addEnumerationPulldown('Node', ' '.join(lst))
	p.addEnumerationPulldown('Channels', 'rgb rgba alpha')
	p.show()

	# Select Nodes by Name
	for n in nuke.allNodes('DiskCache'):
		if n.name() == p.value('Node'):
			n['channels'].setValue(p.value('Channels'))
			n['Precache'].execute()


def filterSelection():

	nodes = nuke.selectedNodes()

	if len(nodes)>0:

		node_class = list(set([n.Class() for n in nodes]))

		p = nuke.Panel('Filter Selection')
		p.addEnumerationPulldown('Class', ' '.join(node_class))

		class_sel = p.value('Class')

		if p.show():
			class_sel = p.value('Class')

			for n in nodes:
				if n.Class() != class_sel:
					n['selected'].setValue(False)
	else:
		nuke.message('Please Select a node')


def alignNodes():

	nodes = nuke.selectedNodes()

	p = nuke.Panel("Align")
	p.addEnumerationPulldown('IN','X-Vertical Y-Horizontal')

	if len( nodes ) < 2:
		return

	if p.show():
		direction = p.value("IN")

		positions = [ float( n[ direction[0].lower()+'pos' ].value() ) for n in nodes]
		avrg = sum( positions ) / len( positions )

		for n in nodes:
			if direction == 'X-Vertical':
				for n in nodes:
					n.setXpos( int(avrg) )
			else:
				for n in nodes:
					n.setYpos( int(avrg) )


def selectChildNodes():
	sel = nuke.selectedNode()
	childNodes = []

	for n in nuke.selectedNode().dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS):
		n['selected'].setValue(True)
		childNodes.append(n.name())

	sel['selected'].setValue(False)

	print sel.name(), " is connected by ", "\n", ', '.join(childNodes)


def selConnected():

	for n in nuke.selectedNodes():
		n_frist = n.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS)[0]
		n_second = n_first.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS)[0]

		n_first['selected'].setValue(True)
		n_sec['selected'].setValue(True)

		n['selected'].setValue(False)


def quickChannel():
	node = nuke.selectedNode()
	ch_node = nuke.layers(node)
	ch = ['all']
	ch.extend(ch_node)

	if 'channels' in node.knobs().keys():

		p = nuke.Panel(node.name() + ".Channels")
		p.addEnumerationPulldown('Channel', ' '.join(ch))
		p.show()

		ch_sel = p.value('Channel')

		if ch_sel:
			node['channels'].setValue(ch_sel)

		print "\n", node.name(), " --> ", ch_sel

	else:
		nuke.message("No Channel to Change")


def holdAtFrame():
	node = nuke.selectedNode()
	node_label = node['label'].value()

	nukescripts.node_copypaste()  # Duplicating the Node
	print "\n\n", node.name()

	node_held = nuke.selectedNode()  # Return the duplicated node

	for name, k in node_held.knobs().items():
		try:
			if k.isAnimated():
				k.clearAnimated()
				print 'Deleting Animation on %s' % name
		except:
			print 'no animation to delete'

		node_held['tile_color'].setValue(2147418367)  # Light Green Color

		if node_label != "":  # for MPC Naming convnsion
			node_held['label'].setValue(node_label + "\n" + "x" + str(nuke.frame()))
		else:
			node_held['label'].setValue("x" + str(nuke.frame()))


def stackIBK():
	'''build IBK stack with one IBK master node selected'''

	if not nuke.selectedNodes('IBKColourV3'):
		nuke.message('Select a IBKColour node')
	else:
		node_master = nuke.selectedNode()
		ls_stack = [6,24,96,192]

		for idx, s in enumerate(ls_stack,0):
			node_slave = nuke.createNode('IBKColourV3', inpanel=False)

			node_slave.setYpos(node_slave.ypos()+18) if idx == 0 else idx

			knobs = ['screen_type','Size','off','mult']
			for k in knobs:
				print k
				node_slave[k].setValue(node_master[k].value())
			node_slave.knob('multi').setValue(int(s))


def setSize(increment = 0.5):
	'''Set knob values with multiplical increments'''

	knobs = ['size', 'Size', 'value', 'which', 'saturation']
	for n in nuke.selectedNodes():
		for k in n.knobs():
			k_size = None
			if k in knobs:
				k_size = k
				k_val = n[k_size].value()
				n[k_size].setValue(k_val*(1+increment))
				print "%s %s set to %s" % (n.name(), k_size, k_val*increment)
			else:
				pass



def disable():
	'''customized disable function, with changing tile_color'''
	'''replace hotkey D'''

	nodes = nuke.selectedNodes()

	col_red = 780084223
	col_green = 2133009407
	col_white = 4294967295
	col_yellow = 3891223551

	if len(nodes)<0:
		nuke.message("Select a node or two, man")
	else:
		for n in nodes:
			try:
				k_disable = n['disable']
			except:
				k_disable = None

			if k_disable:
				if k_disable.value() == False:
					k_disable.setValue(True)
					if n.Class() == 'Switch':
						n['tile_color'].setValue(col_red)
						n['note_font_color'].setValue(col_white)
				else:
					k_disable.setValue(False)
					if n.Class() == 'Switch':
						n['tile_color'].setValue(col_yellow)
						n['note_font_color'].setValue(col_white)



def swapColorspace():
	'''swap in and out OCIOcolorspace node'''
	nodes = nuke.selectedNodes('OCIOColorSpace')

	if nodes:
		for n in nodes:
			old_in = n['in_colorspace'].value()
			old_out = n['out_colorspace'].value()

			n['in_colorspace'].setValue(old_out)
			n['out_colorspace'].setValue(old_in)
	else:
		nuke.message('Select OCIOColorSpace node')


def showIPPanel(panelfloat=True):
	'''Show viewer input control panel'''

	try:
		node_ip = nuke.activeViewer().node()['input_process_node'].value()
		nuke.toNode(node_ip).showControlPanel(forceFloat=panelfloat)
		print "VIEWER_INPUT Shown"
	except:
		if nuke.ask('No Viewer_Input found, load one?'):
			import os
			nuke.loadToolset(os.path.join(os.getEnv('HOME'), '.nuke/ToolSets/Utility/ku_IP.nk'))
		else:
			nuke.message("Oh well then")


def copyMasterNodeStyle():
	'''Copy Master node style to children that are expression linked'''

	n = nuke.selectedNode()

	for d in nuke.dependentNodes(nodes=[n]):
		d['tile_color'].setValue(n['tile_color'].value())
		d['note_font_color'].setValue(n['note_font_color'].value())


def add_gizmo_copyright(n):
    '''add gizmo copyright'''

    c_str = """
    
    <p style="color: gray"><b>%s</b> &#169; 2020 Tianlun Jiang - jiangovfx.com

    """ % n.name()
    k_div = nuke.Text_Knob('div','','')
    k_copyright = nuke.Text_Knob('copyright', ' ',c_str)

    n.addKnob(k_div)
    n.addKnob(k_copyright)


def set_viewer(mode='restore'):
    '''set and restore viewer input pipes
    mode='restore': restore set inputs
    mode='set': record exsisting inputs
    '''

    node_viewer = nuke.activeViewer().node()

    if mode == 'set':
        label = ''
        num_inputs = node_viewer.inputs()
        
        for i in range( num_inputs ):
            node_thisInput = node_viewer.input(i).name() if node_viewer.input(i) else None
            label += "%s:%s\n" % (i+1, node_thisInput)
        node_viewer['label'].setValue(label)
        print( label )

    if mode == 'restore':
        label = node_viewer['label'].value()
        ls_restore = [i.split(':') for i in label.split('\n')[:-1]]

        for n in ls_restore:
            node_viewer.setInput(int(n[0])-1, nuke.toNode(n[1]))
            print("%s:%s" % (n[0], n[1]))
            

