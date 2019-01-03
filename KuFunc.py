'''

KuFunc.py for _NukeStudio & _NukeFreelance
to used in both a VFX Studio and Freelance enviroment

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

def tc2Frames(tc, fps, hh_l):

	tc_int = [int(t) for t in tc.split(':')]

	hh, mm, ss, ff = tc_int

	#Drop Frame Err Difference
	xErr = 0.0 #per Second

	if fps < 30 and fps > 29:
		xErr = 30/fps
	elif fps < 24 and fps > 23:
		xErr = 24/fps
	else:
		xErr = 0

	#Convert
	x = ((hh-hh_l)*3600 + mm*60 + ss)*xErr*fps + ff

	x=int(x)
	return x


def imgSeqDir(path, upDir = -1):

	"""

	:param path: Full path ie. /Volume/../EXPORT/TCC_002_020_v011/TCC_002_020_v011.%04d.dpx
	:param upDir: up directory
	:return: a string of new directaries
	"""

	return os.path.dirname(os.path.dirname(path))
	# return '/'.join(os.path.dirname(path).split('/')[:upDir])




########## NODE GRAPH FUNCTIONS ##########




def mask():
    for n in nuke.selectedNodes():
        if n != 0:
            mk = n.optionalInput()
            n.setInput(mk, nuke.selectedNodes()[0])


def labelChange():
    prevLabel = nuke.selectedNode()['label'].getValue()

    newLabel = nuke.getInput('Change Node Label', prevLabel)

    # Change Values

    for n in nuke.selectedNodes():
        n['name'].getValue()
        n['label'].setValue(newLabel)


def linkedStamp():

    rNode = nuke.selectedNode()
    rNode_nam = rNode.name()

    rNode['selected'].setValue(False)

    stp = nuke.createNode('PostageStamp')
    stp.setInput(0, rNode)
    stp['hide_input'].setValue(1)
    stp['label'].setValue(rNode_nam)

    # Reset Selections
    stp['selected'].setValue(False)
    rNode['selected'].setValue(True)

    # Add User knobs

    py_cmd = "n=nuke.thisNode()\nn.setInput(0, nuke.toNode(n['label'].value()))"


    k_tab = nuke.Tab_Knob("LinkedStamp")
    k_setInput = nuke.PyScript_Knob('link', "Restore Input", py_cmd)
    k_text = nuke.Text_Knob('tx_nodename', "Set Input to: ")

    stp.addKnob(k_tab)
    stp.addKnob(k_text)
    stp.addKnob(k_setInput)

    k_setInput.setTooltip("Taking the node name from label and connect")
    k_text.setValue("<b>%s</b>" % (stp['label'].value()))
    
    def inputUpdate():

        n = nuke.thisNode()
        k = nuke.thisKnob()

        try:
            if k.name() == "inputChange":
                n['label'].setValue(n.dependencies()[0].name())
                n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))
        except:
            pass

        if k.name() == "label": # Manually Change Label
            n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))


    nuke.addKnobChanged(inputUpdate, nodeClass='PostageStamp')


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


def selectChildNodes():
    sel = nuke.selectedNode()
    childNodes = []

    for n in nuke.selectedNode().dependent():
        n['selected'].setValue(True)
        childNodes.append(n.name())

    sel['selected'].setValue(False)

    print sel.name(), " is connected by ", "\n", ', '.join(childNodes)


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
        
        import collections
        node_class = collections.Counter([n.Class() for n in nodes]).keys()

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

def selConnected():

    for n in nuke.selectedNodes():
        n_frist = n.dependent()[0]
        n_second = n_first.dependent()[0]

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


def mergeOp():

	op = ['over', 'under', 'multiply', 'divide', 'plus', 'minus', 'from', 'stencil', 'mask']

	if nuke.selectedNodes('Merge2'):

		p = nuke.Panel('Operation')
		p.addEnumerationPulldown('operation', ' '.join(op))

		if p.show():
			op_sel = p.value('operation')
			for n in nuke.selectedNodes('Merge2'):
				ku_knobCh(n,'operation',op_sel)
	else:
		nuke.message("Please select a Merge node")


def kuDrop():

	if nuke.selectedNodes():

		sel = nuke.selectedNodes()

		#Get Inputs
		p = nuke.getInput('Label Backdrop')

		ls_xpos = [n['xpos'].value() for n in sel]
		ls_ypos = [n['ypos'].value() for n in sel]

		dim_w = [min(ls_xpos), max(ls_xpos)]
		dim_h = [min(ls_ypos), max(ls_ypos)]

		margin_x = 80*1.5
		margin_y = 84*2

		bd = nuke.nodes.BackdropNode(note_font_size=96, note_font='bold', label=p, tile_color=1870626559)

		ku_knobCh(bd, 'xpos', dim_w[0] - margin_x / 2)
		ku_knobCh(bd, 'ypos', dim_h[0] - margin_y - 40)
		ku_knobCh(bd, 'bdwidth', dim_w[1] - dim_w[0] + margin_x + 80)
		ku_knobCh(bd, 'bdheight', max(dim_h[1] - dim_h[0]+84, 84) + margin_y)

	else:
		nuke.message("Plese selecte Nodes")


