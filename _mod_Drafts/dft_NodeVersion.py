'''

* Inspired by bi_nodePresets v1.0

- preset_name : <node_class>.<node_name>.v#

- Version Name
    <this_ver>      This Version
    <cur_ver>       Current Version
    <new_ver>       New Version

- Version Knob Name convention:
    <nv_rm_v#>      "-"
    <nv_load_v#>    "load v##"
    <nv_tip_v#>     ": ", "Short Description"

- Used Functions
    - saveUserPreset(node, preset_name)
    - getUserPresetKnobValues (NodeClass, preset_name)
    - deleteUserPreset(NodeClass, preset_name)
    - node.removeKnob(KnobName)
    - applyUserPreset(nodeName, preset_name)

- Abbrations
    - NV/nv: NodeVersion
'''




import nuke,nukescripts




########## Supporting Function ##########




def findNV(node):

	'''
	Find NV version
	return Highest Current Version as Int
	'''

	nv_knobs = [k for k in node.knobs() if k.startswith("nv_load")]
	nv_vers = [int(v.split('_v')[1]) for v in nv_knobs]
	try:
	    cur_ver = max(nv_ver)
	except:
	    cur_ver = 0 # No Version
	new_ver = cur_ver+1

	return {'cur': cur_ver, 'new': new_ver}



def BasicKnobs(n):

    # Create Knobs
    k_tab = nuke.Tab_Knob('NodeVersion')

    # k_name = nuke.Text_Knob('tx_nodeName', "Node: <b>%s" % node.name(), " ")
    # k_curVer = nuke.Text_Knob('tx_curVer', "Current: <b>v01", " ")

    k_preset = nuke.Text_Knob('tx_preset', "Version: ", "<b>%s.v%s" % (n.name(), '01'))
    k_div = nuke.Text_Knob('div', " ", "")

    # Add Knobs
    n.addKnob(k_tab)
    n.addKnob(k_preset)
    n.addKnob(k_div)



# Button Commands



def cmd_add(n):

    '''
    command to call when Add button is pressed

    1. find new version
    2. save nuke preset
    2. ask for descrition
    3. create NodeVersion knobs
    4. Change Cur Version knob
    '''

    # n = nuke.thisNode()
    new_ver = findNV(n)['new']

    # Preseting
    preset_name = "%s.%s.v%s" % (n.Class(), n.name(), new_ver)
    nuke.saveUserPreset(n, preset_name)
    print preset_name

    # Short description
    tip = nuke.getInput('Give a Short Version Description', '%s' % preset_name)

    # Knobs
    k_rm = nuke.PyScript_Knob('nv_rm_v%s' % new_ver, '<b>&minus;', "import nuke;import dft_NodeVersion as nv;nv.cmd_remove(nuke.thisNode(), nuke.thisKnob())")
    k_load = nuke.PyScript_Knob('nv_load_v%s' % new_ver, '<b>load v%s' % new_ver, "import nuke;import dft_NodeVersion as nv;nv.cmd_load(nuke.thisNode(), nuke.thisKnob())")
    k_tip = nuke.Text_Knob('nv_tip_v%s' % new_ver, ': %s' % tip, "\s")

    #FLAG
    k_load.clearFlag(nuke.STARTLINE)
    k_tip.clearFlag(nuke.STARTLINE)

    # Add knobs
    n.addKnob(k_rm)
    n.addKnob(k_load)
    n.addKnob(k_tip)

    # Change current version
    try:
        n.knob('tx_preset').setValue('<b>%s.v%s' % (n.name(), new_ver.zfill(2)))
    except:
        pass

    #Console
    print "%s added NodeVersion: v%s" % (n.name(), str(new_ver).zfill(2))



def cmd_remove(n,k):

    '''
    Command to call when Remove button is pressed

    1. find cur version
    2. remove user preset
    3. remove knobs
    *4. if cur version is removed, set cur version to None
    '''

    # n = nuke.thisNode()
    # k = nuke.thisKnob()
    this_ver = int(k.name().split('_v')[1])

    # Preset
    this_preset_name = '%s.%s.v%s' % (n.Class(), n.name(), this_ver)
    nuke.deleteUserPreset(n.Class(), this_preset_name)
    print this_preset_name

    # Remove Knob
    try:
    	n.removeKnob('nv_rm_v%s' % this_ver)
    	n.removeKnob('nv_load_v%s' % this_ver)
    	n.removeKnob('nv_tip_v%s' % this_ver)

        # Console
        print "%s removed NodeVersion: v%s" % (n.name(), str(this_ver).zfill(2))

    except:
        print "No Such Knobs"



def cmd_load(n,k):

    '''
    Command to call when Load button is pressed

    1. find this version
    2. load user preset
    3. update cur version knob
    '''

    # n = nuke.thisNode()
    # k = nuke.thisKnob()
    this_ver = int(k.name().split('_v')[1])
    print this_ver

    # Preset
    this_preset_name = '%s.%s.v%s' % (n.Class(), n.name(), this_ver)
    nuke.applyUserPreset(n.name(), this_preset_name)

    # Update Current Version
    try:
        n.knob('tx_preset').setValue('<b>%s.v%s' % (n.name(), this_ver.zfill(2)))
    except:
        print "Fail to load preset: %s" % this_preset_name



########## Main Function ##########




def NodeVersion():

    nv = 1
    node_name = ''
    nodes = nuke.selectedNodes()

    if len(nodes)<=0:
        nuke.message("Please select a node")
    else:
        for n in nodes:

            node_class = n.Class()
            node_name = n.name()
            nv_ver = findNV(n)

            # Add Static Nodes
            BasicKnobs(n)

            # Add Add Button
            k_add = nuke.PyScript_Knob('bt_add', "<b>+", "import nuke;import dft_NodeVersion as nv;nv.cmd_add(nuke.thisNode())")
            k_add_tip = nuke.Text_Knob('tx_add', " Add to list", " ")

            k_add_tip.clearFlag(nuke.STARTLINE)

            n.addKnob(k_add)
            n.addKnob(k_add_tip)

            # Excecute
            cmd_add(n)
