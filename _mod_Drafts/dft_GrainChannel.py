'''

version 0
- create a grain channel shuffle setup for every merge node

'''




import nuke, nukescripts




########## Supporting Functions ##########




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



def grainBuild(nodes_merge):
    '''
    Build Grain nodes set up
    '''

    ch_grain = 'grain'
    console = []
    console_fail = []

    for n in nodes_merge:
        base_node, m_A, m_ASide, m_pos = n
        spacing = (80,74)
        node_color = 1163603199 # Dark Green
        node_connected = base_node.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS)

        # Create Nodes

        try:
            ## Dot node
            node_dot = nuke.nodes.Dot(
                                inputs=[m_A],
                                tile_color=node_color
                                )
            node_dot.setXpos(m_pos[0] + spacing[0] * m_ASide)
            node_dot.setYpos(m_pos[1] + (node_dot.screenHeight()-base_node.screenHeight())/2)
            base_node.setInput(1, node_dot)

            ## Shuffle node
            node_shuffle = nuke.nodes.Shuffle(
                                inputs=[node_dot],
                                tile_color=node_color,
                                )
            node_shuffle.hideControlPanel()
            node_shuffle.setXpos(node_dot.xpos() + (node_dot.screenWidth()-node_shuffle.screenWidth())/2)
            node_shuffle.setYpos(node_dot.ypos() + spacing[1])
            node_shuffle['in'].setValue('alpha')
            node_shuffle['out'].setValue(ch_grain)

            ## Merge node
            node_grainMerge = nuke.nodes.Merge2(
                                inputs=[base_node, node_shuffle],
                                tile_color=node_color,
                                operation='screen',
                                Achannels='alpha',
                                Bchannels=ch_grain,
                                output=ch_grain,
                                xpos=base_node.xpos(),
                                ypos=base_node.ypos() + spacing[1]
                                )
            node_grainMerge.hideControlPanel()

            ### Reconnect base_node output to node_grainMerge
            for n in base_node.dependent():
                for i,idx in enumerate(n.dependencies(),0):
                    if i=base_node:
                        n.setInput(idx, node_grainMerge)
                    else:
                        pass

            console.append(base_node.name())

        except:
            console_fail.append(base_node.name())

    print "Grain Channel set up for\n%s" % console

    if len(console_fail)>0:
        print "Grain Channel fail to set up for\n%s" % console_fail
    else:
        pass

    return None



def grainEnd(nodes_merge):
    '''
    Build Grain nodes at the end to shuffle out
    '''

    pos_merge = {}

    for y in nodes_merge:
        this_node = y[0]
        pos_merge[this_node.ypos()]=this_node.name()

    last_merge = pos_merge[max(pos_merge.keys())]

    end_dot = nuke.nodes.Dot(
                        inputs=[last_merge],
                        tile_color=node_color
                        )
    end_dot.setXpos(end_dot.xpos() + (last_merge.screenWidth() - end_dot.screenWidth())/2)
    end_dot.setYpos(last_merge.ypos() + spacing[1]*2)


    for n in last_merge.dependent():
        for i,idx in enumerate(n.dependencies(),0):
            if i=base_node:
                n.setInput(idx, end_dot)
            else:
                pass

    end_shuffle = nuke.nodes.Shuffle(
                            inputs=[end_dot],
                            tile_color=node_color
                            )
    end_shuffle.setXpos(end_dot.xpos() - spacing[0])
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

        if mode == 'all':

            nodes_merge = collect(cal(nodes))
            grainBuild(nodes_merge)
            grainEnd(nodes_merge)

            print "Grain Channel all Setup"

        elif: mode == 'end':

            grainEnd(nodes_merge)

            print "Grain to Alpha"
