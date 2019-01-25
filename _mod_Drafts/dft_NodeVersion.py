'''

* Inspired by bi_nodePresets v1.0

- PresetName : <node_class>.<node_name>.v#

- Version Name
    <this_ver>      This Version
    <cur_ver>       Current Version
    <new_ver>       New Version

- Version Knob Name convention:
    <nv_rm_v#>      "-"
    <nv_load_v#>    "load v##"
    <nv_tip_v#>     ": ", "Short Description"

- Used Functions
    - saveUserPreset(node, PresetName)
    - getUserPresetKnobValues (NodeClass, PresetName)
    - deleteUserPreset(NodeClass, PresetName)
    - node.removeKnob(KnobName)

- Abbrations
    - NV/nv: NodeVersion
'''




import nuke,nukescripts,os




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



def nv_BasicKnobs(node):

	# Create Knobs
	k_tab = nuke.Tab_Knob('NodeVersion')

	k_name = nuke.Text_Knob('tx_nodeName', "Node: ", "<b>%s" % node.name())
	k_curVer = nuke.Text_Knob('tx_curVer', "Current: ", "<b>v01")
	k_div = nuke.Text_Knob('div', "", "")

	# Add Knobs
	nuke.addKnob(k_tab)
	nuke.addKnob(k_name)
	nuke.addKnob(k_curVer)
	nuke.addKnob(k_div)



# Button Commands



def nv_cmd_add():

	'''
	command to call when Add button is pressed

	1. find new version
    2. save nuke preset
	2. ask for descrition
	3. create NodeVersion knobs
    4. Change Cur Version knob
	'''

	n = nuke.thisNode()
	new_ver = findNV(n)['new']

    # Preseting
    PresetName = "%s.%s.v%s" % (n.Class(), n.name(), new_ver)
    nuke.saveUserPreset(n, PresetName)

    # Short description
	tip = nuke.ask('Give a Short Version Description', 'add new version, v%s' % new_ver)

	# Knobs
	k_rm = nuke.PyScript_Knob'nv_rm_v%s' % new_ver, '<b>&minus;', "import nuke; import %s as NodeVersion; NodeVersion.nv_cmd_remove()" % __file__)
	k_load = nuke.PyScript_Knob('nv_rm_v%s' % new_ver, 'load v%s' % new_ver, "import nuke; import %s as NodeVersion; NodeVersion.nv_load()" % __file__)
	k_tip = nuke.Text_knob('nv_tip_v%s' % nv_ver, ': %s' % tip)

    #FLAG
    k_load.clearFlag(Nuke.STARTLINE)
    k_tip.clearFlag(Nuke.STARTLINE)

    # Add knobs
    nuke.addKnob(k_rm)
    nuke.addKnob(k_load)
    nuke.addKnob(k_tip)

    # Change current version
    try:
        k_curVer.setValue('v%s' % new_ver)
    except:
        pass

    #Console
    print "%s added NodeVersion: v%s" % (n.name(), str(new_ver).zfill(2))



def nv_cmd_remove():

	'''
	Command to call when Remove button is pressed

    1. find cur version
    2. remove user preset
    3. remove knobs
    *4. if cur version is removed, set cur version to None
	'''

	n = nuke.thisNode()
    k = nuke.thisKnob()
	this_ver = int(k.name().split('_v')[1])

    # Preset
    this_PresetName = '%s.%s.v%s' % (n.Class(), n.name(), this_ver)
    nuke.deleteUserPreset(n.Class(), this_PresetName)

    # Remove Knob
    try:
    	n.removeKnob('nv_rm_v%s' % this_ver)
    	n.removeKnob('nv_load_v%s' % this_ver)
    	n.removeKnob('nv_tip_v%s' % this_ver)

        # Console
        print "%s removed NodeVersion: v%s" % (n.name(), str(this_ver).zfill(2))

    except:
        print "No Such Knobs"


def nv_cmd_load():

    '''
    Command to call when Load button is pressed

    1. find this version
    2. load user preset
    3. update cur version knob
    '''

    


########## Main Function ##########




def NodeVersion():

    # Global Var
    nv = 1
    node_name = ''
    nodes = nuke.selectedNodes()



    # Main Function
    for n in nodes:

        node_class = n.Class()
        node_name = n.name()
        nv_ver = findNV(n)

        preset_name = "%s.%s.%s" % (node_class, node_name, nv_ver['new'])

        # Back End - save preset
        nuke.saveUserPreset(n, preset_name)

        # Front End - Add knobs
        cmd_add = ""
        cmd_remove = "%s.removeKnob()" % __file__
        cmd_load = "nuke.applyUserPreset(%s,%s)" %

	# Knobs
        k_add = nuke.PyScript_Knob('bt_add', "<b>+", cmd_add)
        k_add_descr = nuke.Text_Knob('tx_add', " Add to List", " ")

        k_rm = nuke.PyScript_Knob('nv_rm_v1', "<b>&minus;", cmd_remove)
        k_load = nuke.PyScript_Knob('nv_load_v1', "<b>&minus;", cmd_remove)
