def _version_():
    ver='''

    version 0
    - Selected Expression Node
    - Give Presets, which channel to add
    - add

    '''
    return ver



import nuke




def findNode():
    '''Node if selected, else create'''

    nodes = None
    if len(nuke.selectedNodes('Expression'))>0:
        nodes = selectedNodes('Expression')
    else:
        nodes = nuke.createdNode('Expression')

    return nodes



def setFields(node, ch, expr):
    '''set the expr field with given node'''

    fields = {
            'alpha': ['expr3'],
            'rgb': ['expr0', 'expr1', 'expr2'],
            'rgba': ['expr0', 'expr1', 'expr2', 'expr3']
            }

    for k in fields[f]:
        node[k].setValue(expr)


def ExprPrompt():
    '''main function'''

    nodes = findNode()

    p = nuke.Panel("Expression Value")

    p.addSingleLineInput('expr: ')
    p.addEnumerationPulldown('Set Channel', 'alpha rgb rgba')

    p.addButton('Cancel')
    p.addButton('Set!')

    if p.show():

        ch = p.value('Set Channel')
        expr = p.value('expr: ')

        if isinstance(nodes, list):
            for n in nodes:
                setFields(n, ch, expr)
        else:
            setFields(nodes, ch, expr)

    else:
        print "Set Expression Cancelled"
