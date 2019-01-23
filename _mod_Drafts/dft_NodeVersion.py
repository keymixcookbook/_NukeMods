'''

* Inspired by bi_nodePresets v1.0

- Select a node
- Promot asking for short description
- creating user preset and default adding version 1
    - save userPresetKnobValue in nv_rm_v1 tooltip
    - PresetName : $NODECLASS.$NODENAME.v#
- create a serious of knobs

- Create a user tab "NodeVersion"
- Show Current Node and Current Version used
    - version KnobName convention:
        <nv_rm_v#>      "-"
        <nv_load_v#>    "load v##"
        <nv_tip_v#>     ": ", "Short Description"

- When a load version button is pushed
    1. load user preset
    2. update <cur_ver> knob with this <nv> version

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




def nv_addBasicKnobs(node):

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
	
	

def nv_addKnob(node):

		
	

	
	
def nv_removeKnob():

	n = nuke.thisNode()
	nv_ver = int(nuke.thisKnob().name().split('_v')[1])
	n.removeKnob('nv_rm_v%s' % nv_ver)
	n.removeKnob('nv_load_v%s' % nv_ver)
	n.removeKnob('nv_tip_v%s' % nv_ver)




########## Main Function ##########




def NodeVersion():

    # Global Var
    nv = 1
    node_name = ''
    nodes = nuke.selectedNodes()

    # Predefine Functions
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

        k_add = nuke.PyScript_Knob('bt_add', "<b>+", cmd_add)
        k_add_descr = nuke.Text_Knob('tx_add', " Add to List", " ")

        k_rm = nuke.PyScript_Knob('nv_rm_v1', "<b>&minus;", cmd_remove)
        k_load = nuke.PyScript_Knob('nv_load_v1', "<b>&minus;", cmd_remove)
