'''

Functions to call for VIEWER_INPUT

'''


import platform


__VERSION__='1'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__COPYRIGHT__="copyright %s" % __AUTHOR__

__TITLE__=__file__.split('_')[1].split('.')[0]


def _version_():
	ver='''

	version 1.0
    - adds preset buttons

	'''
	return ver




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts
PRESET_STR = 'IPSet' 




#-------------------------------------------------------------------------------
#-FUNCTIONS
#-------------------------------------------------------------------------------




def add_cdl():
    '''adds cdl group to IP node'''
    node_cdl = nuke.root().selectedNode()
    print node_cdl.name()
    if node_cdl != nuke.thisNode():
        node_ip = nuke.thisNode()
        #node_ip = nuke.toNode('VIEWER_INPUT')
        with nuke.root():
            nuke.nodeCopy('%clipboard%')
            nukescripts.clear_selection_recursive()
        
        k_cdl = nuke.Boolean_Knob('cdl', "AVID GRADE CDL")
        k_cdl.setFlag(nuke.STARTLINE)
        node_ip.addKnob(k_cdl)
        
        with node_ip:
            group_input = nuke.toNode('Input')
            group_input.setSelected(True)
            node_cdl = nuke.nodePaste('%clipboard%')
            node_cdl['disable'].setExpression('!parent.cdl')


def add_preset():
    '''create preset buttons adds data to tooltip'''
    node = nuke.thisNode()
    node_viewer = nuke.activeViewer().node()

    # Get knob values
    dict_knobs = {}

    dict_knobs['lut'] = node_viewer['viewerProcess'].value()
    dict_knobs['cdl'] = node['cdl'].value() if 'cdl' in node.knobs() else None
    ls_knobs = ['exposure', 'y','saturation', 'd_exp', 'd_y', 'd_sat']
    for k in ls_knobs:
        dict_knobs[k] = node[k].value()
            
    # Build knob for this preset
    this_preset_idx = preset_idx()
    preset_latest = PRESET_STR+str(this_preset_idx)
    cmd="mod_IP.apply_preset()"
    k_preset = nuke.PyScript_Knob(preset_latest, preset_latest.replace(PRESET_STR, PRESET_STR+': '), cmd)
    k_preset.setTooltip(str(dict_knobs))
    if this_preset_idx > 1:
        k_preset.clearFlag(nuke.STARTLINE)

    if this_preset_idx == 1:
        node.addKnob(nuke.Text_Knob('',''))

    node.addKnob(k_preset)


def apply_preset():
    '''apply presets
    @idx: (int), index for preset to apply
    '''

    node = nuke.thisNode()
    thisPreset = eval(nuke.thisKnob().tooltip())

    for k,v in thisPreset.iteritems():
        if k == 'lut':
            nuke.activeViewer().node()['viewerProcess'].setValue(v)
        elif k == 'cdl' and v != None:
            node[k].setValue(v)
        else:
            node[k].setValue(v)
    

def preset_idx():
    '''finds latest preset button index
    return: int
    '''

    node = nuke.thisNode()
    try:
        idx_latest = int(max([k.split(PRESET_STR)[1] for k in node.knobs() if k.startswith(PRESET_STR)]))+1
    except:
        idx_latest = 1

    return int(idx_latest)
