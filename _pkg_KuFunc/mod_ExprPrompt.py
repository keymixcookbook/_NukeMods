'''

- Selected Expression Node
- Give Presets, which channel to add
- add

'''

import nuke

def ExprPrompt():

    nodes = nuke.selectedNodes('Expression')

    if len(nodes)<=0:
        nuke.message("Please Select Expression nodes")
    else:

        p = nuke.Panel("Expression Value")

        p.addEnumerationPulldown('Set Channel', 'alpha rgb rgba')
        p.addSingleLineInput('expr: ')

        p.addButton('Cancel')
        p.addButton('Set!')

        if p.show():

            sel_channel = p.value('Set Channel')
            input_expr = p.value('expr: ')

            channel_set = []

            if sel_channel == "alpha":
                channel_set = ['expr3']
            elif sel_channel == "rgba":
                channel_set = ['expr0', 'expr1', 'expr2', 'expr3']
            elif sel_channel == "rgb":
                channel_set = ['expr0', 'expr1', 'expr2']

            # Set Expressions

            for n in nodes:
                for ch in channel_set:
                    n[ch].setValue(input_expr)
        else:
            print "Set Expression Cancelled"
