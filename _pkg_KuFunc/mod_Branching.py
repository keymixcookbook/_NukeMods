'''

version 0
- Merge or detach a branch with multiple nodes on the B pipe

'''


import nuke, nukescripts




########## Supporting Functions ##########




def nodeSplit(nodes):

    '''
    Filter selection to parts
    '''

    trunks = (nodes[1], nodes[0])
    branches = nodes[2:]

    return [trunks, branches]



def move(branches, trunks):
    '''
    Move Branches nodes to trunks
    '''

    trunk_x = (trunks[0].xpos()+trunks[1].xpos())/2

    for b in branches:
        b.setXpos(int(trunk_x))

    return None



def bonds(branches):
    '''
    Find the top and bottom of the branches
    '''

    print branches

    dic_top = {}
    dic_bottom = {}
    branch_bottom = None

    # Finding Top Branch node
    for n in branches:
        if n.input(0) == None:
            dic_top[n.ypos()]=n

    branch_top = dic_top[min(dic_top.keys())]

    # Find Bottom Branch node
    for n in branches:
        if len(n.dependent())<=0:
            branch_bottom = n

    ends = [branch_top, branch_bottom]

    return ends



def attach(trunks, ends):
    '''
    Attach branches to trunks
    '''

    trunk_top, trunk_bottom = trunks
    branch_top, branch_bottom = ends

    trunk_bottom_input = None
    for idx, i in enumerate(trunk_bottom.dependencies(),0):
        if i == trunk_top:
            trunk_bottom_input = idx

    branch_top.setInput(0, trunk_top)
    trunk_bottom.setInput(idx, branch_bottom)


    return None




########## Main Functions ##########




def Branching():

    nodes = nuke.selectedNodes()

    if len(nodes)<=0:
        nuke.message("Select branches to merge")
    else:

        trunks, branches = nodeSplit(nodes)

        ends = bonds(branches)
        move(branches, trunks)
        attach(trunks,ends)

    return None
