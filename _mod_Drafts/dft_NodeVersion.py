'''

- Find out env variabe: USER, HOME, SHOW, SCENE, SHOTNAME or SHOT
- Create directory: $HOME/.nuke/kuNodeVersion/SHOW/SCENE/SHOT

# Save Node Version
- name version: $NODENAME_nv$VERSION.nk
- save selected node to the corrisponding dir

# Load Node Version
- select a node for loading version
- find its corrisponding saved node base on NODENAME
- prompt with NODENAME as title and nv$VERSION as menu item
- combine selected menu item with NODENAME: NODENAME + nk$VERSION + .nk
- insert the node

'''

import nuke,nukescripts,os
from mod_StudioENV import *

def NodeVersion():

    StudioENV(studio="MPC")

    # NodeVersion Directory
    dir_nv = os.path.join(os.getenv('HOME'), ".nuke", "kuNodeVersion", SHOW, SCENE, SHOT)

    if os.path.exists(dir_nv):
        pass
    else:
        os.makedirs(dir_nv)

    # Global Variables & Functions
    node = nuke.selectedNode()
    nodename = node.name()

    def findVersion(dir_nv, new=True):

        list_ver = os.listdir(dir_nv)

        if len(list_ver)<=0:
            ver = '%03d' % 1
        else:
            all_ver = [int(os.path.splitext(v)[0].split('_nv')[1]) for v in os.listdir(dir_nv)]
            if new == True:
                ver = '%03d' % (max(all_versions) + 1)
            elif new == False:
                ver = '%03d' % max(all_versions)

        return ver

    # Save Node Version
    if node:
        nuke.nodeCopy(os.path.join(dir_nv, "%s_nv%s.nk" % (nodename,findVersion(dir_nv))))
    else:
        nuke.message('Gotta select a node')

    # Load Node Version
    if node:
        all_ver = [os.path.splitext(v)[0].split('_nv')[1] for v in os.listdir(dir_nv)]

        p = nuke.Panel('Load Node Version')
        p.addEnumerationPulldown('%s_v' % nodename, ' '.join(all_ver))

        if p.show():
            sel_ver = p.value('%s_v' % nodename)
            sel_filename = "%s_nv%s.nk" % (nodename, sel_ver)

            nuke.nodePaste(os.path.join(dir_nv, sel_filename))

    else:
        nuke.message('Gotta select a node')
