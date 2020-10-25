'''

Functions to call for VIEWER_INPUT

'''


import platform


__VERSION__='1.0'
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




def build_IP():
    '''build IP node'''
    if 'VIEWER_INPUT' in [n.name() for n in nuke.allNodes()]:
        nuke.message('IP already exist')
    else:

        str_autolabel = "\n('exp: %s\\n' % nuke.thisNode()['exp'].value())+('gamma: %s\\n' % nuke.thisNode()['y'].value())+('sat: %s\\n' % nuke.thisNode()['sat'].value())"
        colour_bg = 2135237631
        colour_text = 4289560575

        # Declare Node
        node_IP = nuke.nodes.Group(
            note_font_color = colour_text,
            note_font_size = 48,
            note_font = 'bold',
            tile_color = colour_bg,
            hide_input = True
        )
        node_IP.setName('VIEWER_INPUT')

        # Declare knobs
        k_tab = nuke.Tab_Knob('tb_user', 'ku_IP')
        k_cdl_add = nuke.PyScript_Knob('cdl_add', 'add cdl', 'mod_IP.add_cdl()')
        k_exp = nuke.Double_Knob('exp', 'exposure')
        k_exp_d = nuke.Boolean_Knob('d_exp', 'disable', True)
        k_y = nuke.Double_Knob('y', 'gamma')
        k_y_d = nuke.Boolean_Knob('d_y', 'disable', True)
        k_sat = nuke.Double_Knob('sat', 'saturation')
        k_sat_d = nuke.Boolean_Knob('d_sat', 'disable', True)
        k_cdl = nuke.Boolean_Knob('cdl', 'SHOW CDL GRADE')
        k_div_preset = nuke.Text_Knob('tx_preset', 'preset')
        k_preset_add = nuke.PyScript_Knob('preset_add', '<b>&#43;</b>', 'mod_IP.add_preset()')
        k_preset_remove = nuke.PyScript_Knob('preset_remove', '<b>&#8722;</b>', 'mod_IP.remove_preset()')

        k_exp.setValue(0)
        k_y.setValue(1)
        k_sat.setValue(1)

        for k in [k_exp_d, k_y_d, k_sat_d, k_preset_remove]:
            k.clearFlag(nuke.STARTLINE)
        k_cdl.setFlag(nuke.STARTLINE)

        ## Add Knobs
        for k in [k_tab, k_cdl_add, k_exp, k_exp_d, k_y, k_y_d, k_sat, k_sat_d, k_cdl, k_div_preset, k_preset_add, k_preset_remove]:
            node_IP.addKnob(k)

        # Add nodes inside IP Group
        with node_IP:
            nuke.createNode('Input', "name Input", inpanel=False)
            nuke.createNode('EXPTool', "name _EXPOSURE_ channels rgb", inpanel=False)
            nuke.createNode('Gamma', "name _GAMMA_ channels rgb", inpanel=False)
            nuke.createNode('Saturation', "name _SATURATION_ channels rgb", inpanel=False)
            nuke.createNode('Output', "name Output", inpanel=False)

            nuke.toNode('_EXPOSURE_')['red'].setExpression('parent.exp')
            nuke.toNode('_EXPOSURE_')['green'].setExpression('parent.exp')
            nuke.toNode('_EXPOSURE_')['blue'].setExpression('parent.exp')
            nuke.toNode('_GAMMA_')['value'].setExpression('parent.y')
            nuke.toNode('_SATURATION_')['saturation'].setExpression('parent.saturation')

        node_IP['autolabel'].setValue(str_autolabel)

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
        
        # k_cdl = nuke.Boolean_Knob('cdl', "AVID GRADE CDL")
        # k_cdl.setFlag(nuke.STARTLINE)
        # node_ip.addKnob(k_cdl)
        
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
    ls_knobs = ['exp', 'y','saturation', 'd_exp', 'd_y', 'd_sat']
    for k in ls_knobs:
        dict_knobs[k] = node[k].value()
            
    # Build knob for this preset
    this_preset_idx = preset_idx()
    preset_latest = PRESET_STR+str(this_preset_idx)

    ## Label input
    this_preset_label = nuke.getInput('Preset Label (keep it short)', 
                                    preset_latest.replace(PRESET_STR, PRESET_STR+': '))

    if this_preset_label:
        cmd="mod_IP.apply_preset()"
        k_preset = nuke.PyScript_Knob(preset_latest, this_preset_label, cmd)
        k_preset.setTooltip(str(dict_knobs))
        if this_preset_idx > 1:
            k_preset.clearFlag(nuke.STARTLINE)

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


def remove_preset():
    '''remove preset button'''

    node = nuke.thisNode()

    knob_presets = [str(k +' | ' + node.knob(k).label()) for k in node.knobs() if k.startswith(PRESET_STR)]

    p = nukescripts.PythonPanel('Remove A Preset')
    pk_knoblist = nuke.Enumeration_Knob('knoblist', "Delete Preset: ", knob_presets)
    p.addKnob(pk_knoblist)

    if p.showModalDialog():
        knob_delete = node.knob(pk_knoblist.value().split(' | ')[0])
        node.removeKnob(knob_delete)