def _version_():
	ver='''

	version 0.0
    - sets a dot node as markers for all deepRecolor node
	- creates DeepMerge node to connect with DeepMarker

	'''
	return ver


import nuke, nukescripts




########## Supporting Functions ##########




def setMarkers():
    '''create dot node for selected DeepRecolor node'''
    color = 24831
    nodes = nuke.allNodes('DeepRecolor') if len(nuke.selectedNodes('DeepCollector'))<=0 else nuke.selectedNodes('DeepRecolor')
    print '\n'
    for n in nodes:
        thisDeep = findTopNode(n)
        thisPos = [n.xpos()+n.screenWidth()*2, n.ypos()+n.screenHeight()*2]
        node_marker = nuke.nodes.Dot(tile_color=color)
        k_tab = nuke.Tab_Knob('tb_deepMarker', 'DeepCollect_Marker')
        k_text = nuke.Text_Knob('tx_deepRead', '<b>DeepRead: </b>', thisDeep)
        node_marker.addKnob(k_tab)
        node_marker.addKnob(k_text)
        node_marker.setName('DeepMarker1')
        node_marker.setXYpos(*thisPos)
        node_marker.setInput(0, n)

        print "set DeepMarker: %s -> %s" % (n.name(), node_marker.name())



def getMarker():
    '''finds all the deep markers in the script
	return: markers (list of obj)
	'''

    markers = [n for n in nuke.allNodes('Dot') if 'tb_deepMarker' in n.knobs()]
    for m in markers:
        print "DeepMarker collected: %s - %s" % (m.name(),m['tx_deepRead'].value())
    return markers



def findTopNode(n):
    '''Returns a name of the top node
	return: topnode_name (str)
	'''
    topnode_name = nuke.tcl("full_name [topnode %s]" % n.name())
    return topnode_name



########## Main Functions ##########




def DeepCollect(mode='collect'):
    '''collects or sets markers
    mode='collect': collects deep from markers
    mode='markers': sets markers
    '''

    if mode=='collect':
        markers = getMarker()
        node_collector = nuke.nodes.DeepMerge(note_font='bold', hide_input=True)
        k_tab = nuke.Tab_Knob('tb_user', 'DeepCollector')
        k_text = nuke.Text_Knob('tx_collector', 'Deeps Collected:', '\n'.join(['-'+n['tx_deepRead'].value() for n in markers]))
        k_text.setTooltip('<b>Deeps Collected:</b>\n'+'\n'.join(['-'+n['tx_deepRead'].value()[:-8] for n in markers]))
        k_markers = nuke.String_Knob('tx_markers', 'DeepMarkers Collected', ','.join([m.name() for m in markers]))
        node_collector.addKnob(k_tab)
        node_collector.addKnob(k_text)
        node_collector.addKnob(k_markers)
        node_collector.setName('DeepCollector1')
        node_collector['autolabel'].setValue("nuke.thisNode().name()+'\\ninputs: '+str(nuke.thisNode().inputs())")
        node_collector.setXYpos(*nuke.center())

        for i, m in enumerate(markers):
            node_collector.setInput(i, m)

        print "Deep collected for %s" % node_collector.name()
    elif mode=='markers':
        setMarkers()
