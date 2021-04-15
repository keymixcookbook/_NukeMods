'''

Merge a branch into the main pipe

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import platform
import os
from Qt import QtWidgets, QtGui, QtCore
import nuke, nukescripts




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '2.0'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "Branching v%s" % __VERSION__



def _version_():
    ver='''

    version 2.0
    - Only need to select branches and trunk_top, will detect trunk_bottom base on xpos

    verion 1.1
    - fix bottom node not connecting
    - fix `Dot` node alignment
    - fix bottom node connect with wrong pipe

    version 1.0
    - Merge or detach a branch with multiple nodes on the B pipe

    '''
    return ver



#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




def Branching():
    '''main function'''

    nodes = nuke.selectedNodes()
    if len(nodes)<=0:
        nuke.message("Select branches to merge")
    else:
        trunks, branches = nodeSplit(nodes)

        ends = bonds(branches)
        move(branches, trunks)
        attach(trunks,ends)

    return None




#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------




def nodeSplit(nodes):
    '''Filter selection to parts
    @nodes: selected nodes (list of obj)
    return: [trunks, branches] (list of lists)
    '''

    def centerPoint(node):
        return int((node.xpos()+node.screenWidth())/2)

    trunk_top = nodes[0]
    trunk_bottom = None
    trunk_top_cx = centerPoint(trunk_top)
    threshold = 10

    for n in trunk_top.dependent():
        if centerPoint(n)>(centerPoint(trunk_top)-10) and centerPoint(n)<(centerPoint(trunk_top)+10):
            trunk_bottom = n
        else:
            pass

    trunks = (trunk_top, trunk_bottom)

    branches = nodes[1:]

    return [trunks, branches]


def move(branches, trunks):
    '''Move Branches nodes to trunks
    @branches: nodes to merge (list of obj)
    @trunks: nodes to merge with (list of obj)
    return: None
    '''

    trunk_x = (trunks[0].xpos()+trunks[1].xpos())/2
    trunk_cX = trunk_x+int(trunks[0].screenWidth()/2)

    for b in branches:
        b_cX = b.xpos()+int(b.screenWidth()/2)
        cX_dif = b_cX-trunk_cX
        b.setXpos(int(b.xpos()-cX_dif))

    return None


def bonds(branches):
    '''Find the top and bottom of the branches
    @branches: nodes about to be merged (list of obj)
    return: [branch_top, branch_bottom] (list of obj)
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
    '''Attach branches to trunks
    @trunks: nodes to merge with (list of obj)
    @ends: nodes about to be merged (list of obj)
    return: None
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