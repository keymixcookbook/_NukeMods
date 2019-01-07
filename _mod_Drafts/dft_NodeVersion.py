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
- incert the node

'''
