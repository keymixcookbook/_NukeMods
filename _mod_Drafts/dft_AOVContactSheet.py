'''

- Filtering chanel layers with keywords

'''

import platform


__VERSION__='0.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__COPYRIGHT__="copyright %s" % __AUTHOR__

__TITLE__=__file__.split('_')[1].split('.')[0]


def _version_():
	ver='''

	version 0.0
    - if a node is selected, prompt for keyword create a contactsheet group node

	'''
	return ver




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts
import re



def AOVContactSheet():
    '''main function'''
    if not nuke.selectedNode():
        nuke.message("Select a node")
    else:
        node_xpos = nuke.selectedNode().xpos()+nuke.selectedNode().screenWidth()
        node = create_group()
        node.setXpos(node_xpos)
        node.setInput(0, nuke.selectedNode())
    

def button_filter():
    '''filter with keywords with button pressed'''
    node = nuke.thisNode()
    filtering(node)




#------------------------------------------------------------------------------
#-Supporting Function
#------------------------------------------------------------------------------




def filtering(node):
    '''main filtering function'''

    layers_all = nuke.layers(node.dependencies(nuke.INPUTS)[0])
    layers_filtered = filter_core(layers_all, node['keywords'].value())
    build_remove(layers_filtered, node)


def filter_core(layers_all, search_str):
    '''filter layers with user input string
    @layers_all: (list of str) list of all layers
    @search_str: (str) string to filter layers
    return: (dict of str, int: [str,...]) filtered dict of layers'''

    _layers_keep = [s for s in layers_all if re.search(search_str, s)]
    _layers_remove = list(set(layers_all)-set(_layers_keep))

    counter = 0
    dict_remove={}
    _thisList = list()
    for idx, l in enumerate(_layers_remove, 1):

        _thisList.append(l)
        if idx % 4 == 0:
            dict_remove[counter]=_thisList
            _thisList=[]
            counter += 1
    del _thisList
    
    return dict_remove
    

def build_remove(dict_remove, node):
    '''rebuild Remove node everytime it's called
    @dict_remove: (dict of str, int: [str,...]) filtered dict of layers
    @node: (obj) node object to build
    '''

    CH = ['channels', 'channels2', 'channels3', 'channels4']

    with node:
        for r in nuke.allNodes('Remove'):
            nuke.delete(r)

        nukescripts.clear_selection_recursive()
        nuke.toNode('Input').setSelected(True)
        
        for k in dict_remove:
            node_remove = nuke.createNode('Remove', 'operation remove', inpanel=False)
            thisGroup = dict_remove[k]
            node_remove['label'].setValue(', '.join(thisGroup))
            for idx, l in enumerate(thisGroup):
                node_remove[CH[idx]].setValue(l)


def create_group():
    '''create a group node with proper nodes
    return: (obj) group node object'''

    user_keyword = nuke.getInput("keyword to filter", "*")

    if user_keyword:
        node = nuke.nodes.Group()
        node.setName('AOVContactSheet')

        k_tab = nuke.Tab_Knob('tb_user', 'ku_AOVContactsheet')
        k_key = nuke.String_Knob('keywords', "keywords", user_keyword)
        k_filter = nuke.PyScript_Knob('bt_filter', "Filter", 'mod_AOVContactSheet.button_filter()')

        node.addKnob(k_tab)
        node.addKnob(k_key)
        node.addKnob(k_filter)
        node['label'].setValue('filtering: <b>[value keywords]</b>')

        with node:
            node_input = nuke.createNode('Input', 'name Input', inpanel=False)
            node_crop = nuke.createNode('Crop', inpanel=False)
            node_contact = nuke.createNode('LayerContactSheet', inpanel=False)
            node_output = nuke.createNode('Output', 'name Output', inpanel=False)

            node_crop['box'].setExpression('input.bbox.x', 0)
            node_crop['box'].setExpression('input.bbox.y', 1)
            node_crop['box'].setExpression('input.bbox.r', 2)
            node_crop['box'].setExpression('input.bbox.t', 3)
            node_contact['showLayerNames'].setValue(True)
            node_crop['reformat'].setValue(True)

        return node


