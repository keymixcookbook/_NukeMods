import nuke,nukescripts, os

### Find the Top Node of a given root node

def findTopNode(n=nuke.selectedNode()):

    '''
    Returns a string of the top node
    '''

    topnode_name = nuke.tcl("full_name [topnode %s]" % n.name())
    topnode_file = nuke.filename(nuke.toNode(topnode_name))

    return topnode_name



def DeepCollector():

    def get_topnode(node):
        # Get topnode of node
        return nuke.toNode(nuke.tcl("full_name [topnode {0}]".format(node.name())))

    def get_layername(filepath):
        show = os.getenv('AF_PROJECT_NAME')
        if show not in filepath:
            layername = os.path.basename(filepath).split('.')[0]
            return layername
        show_path = filepath.split('show/{0}/'.format(show))[1]
        tokens = show_path.split('/')
        layername = tokens[8]
        return layername

    def get_topnode(node):
    # Get topnode of node
        return nuke.toNode(nuke.tcl("full_name [topnode {0}]".format(node.name())))

    def get_layername(filepath):
        show = os.getenv('AF_PROJECT_NAME')
        if show not in filepath:
            layername = os.path.basename(filepath).split('.')[0]
            return layername
        show_path = filepath.split('show/{0}/'.format(show))[1]
        tokens = show_path.split('/')
        layername = tokens[8]
        return layername
    
    '''
    - Find Dot Bookmark - dot_bookmark
    - Find Top Node - topnode
    - Find File base name without extensions - topnode_layername

    {topnode_layername: [dot_bookmark, topnode, counter]}

    - create a group
    - create the tabs and checkboxes with topnode_layername
    - inside the group, create Input, Switch and DeepMerge per tab
        - link value of the Switch to "parent.topnode_layername"
        - create output link to DeeoMerge
    - outside the group, setInput to dot_bookmark, with corresponding input number

    Filename: LRB_2130_main_light_bty_fx_roverdust_b_backleftwheel_v053.deep.%05d.exr
    '''

    dot_bookmark = [n for n in nuke.allNodes('Dot') if "toCollector" in n['label'].value()]

    counter = 0
    deep_dict = {}


    ## Collecting nodes
    for t in dot_bookmark:
        topnode = get_topnode(t)
        topnode_layername = get_layername(nuke.filename(topnode))

        counter += 1

        deep_dict[topnode_layername] = [t, topnode, counter]

    ## Create Group and add input
    g = nuke.nodes.Group(name="DeepCollector", tile_color=25344)
 
    g.begin()

    for n in range(len(deep_dict)):
        node_input = nuke.nodes.Input(label="[value number]")
        node_switch = nuke.nodes.Switch(xpos=node_input, which=1)
        node_switch.setInput(1,node_input)
 
    sw = 0
    deepMerge = nuke.nodes.DeepMerge()
    for s in nuke.allNodes('Switch'):
        deepMerge.setInput(sw, s)
        sw += 1
 
    nuke.nodes.Output().setInput(0,deepMerge)
 
    g.end()

    ## Set Group input to dot_mark
    ip = 0
    for k, v in deep_dict.iteritems():
        print "Layer %s" % (k)
        g.setInput(ip, v[0]) #Counter, dot_Bookmark
        ip += 1