'''

- Show the type of channels selected
- ie. only "id", "spec", "multi", "multiSpecs", or "data"

- Renderman Light: multi[0-9], diffMulti[0-9], specMulti[0-9]. id[0-10], diffCol, diffDir, diffInd, specDir, specInd, emission, subserface
- Renderman Data: depth2, norm, position2, refPosition2, uv2, vel, shadow

- Have Options to view: single layer OR group of layers with a given type[multiLights, diffMulti, specMulti, diff, spec, shading, data]
- Only keep selected layer/layer groups
- Output with LayerContactSheet

'''

import nuke, nukescripts
import re





def AOVContactSheet():
    '''main function'''

    if not nuke.selectedNode():
        try:
            node = nuke.thisNode()
        except:
            nuke.message("Select a node")
    else:
        node = nuke.selectedNode()

    if node is not nuke.thisNode():
        node = create_group()
        node.setInput(0, nuke.selectedNode())
    
    layers_all = nuke.layers(node.dependencies(nuke.INPUTS)[0])

    layers_filtered = filter_layers(layers_all, node['keywords'].value())
    build_remove(layers_filtered, node)


def filter_layers(layers_all, search_str):
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
        k_filter = nuke.PyScript_Knob('bt_filter', "Filter", 'mod_AOVContactSheet.AOVContactSheet()')

        node.addKnob(k_tab)
        node.addKnob(k_key)
        node.addKnob(k_filter)
        node['label'].setValue('filtering: [value keywords]')

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


