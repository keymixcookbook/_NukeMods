'''

- Finds all or selected Nodes with hidden inputs
- unhide inputs, save node names
- take saved node names and hide them back

'''


import nuke, nukescripts





def switch(node):
    for n in node['tx_store'].value().split(';'):
        this_node = nuke.toNode(n)
        if this_node['hidden_input'].value() == True:
            this_node['hidden_input'].setValue(False)
        else:
            this_node['hidden_input'].setValue(True)



def upd(node):
    all_hidden = [n.name() for n in nuke.allNodes() if n['hidden_input'].value() == True]

    node['tx_store'].setValue(','.join(all_hidden))




def RestoreHiddenInputs():

    all_hidden = [n.name() for n in nuke.allNodes() if n['hidden_input'].value() == True]

    node_hidden = nuke.nodes.NoOp(
                            hidden_input=True,
                            note_font_size = 48,
                            note_font = 'bold',
                            note_font_color = 4294967295,
                            tile_color = 4278190335
                            )

    nuke.nodes.BackdropNode(
                            tile_color = 4278190335,
                            xpos = int(node_hidden.xpos()-80),
                            ypos = int(node_hidden.ypos()-60),
                            bdwidth = int(node_hidden.screenWidth()+160),
                            bdheight = int(node_hidden.screenHeight()+120)
                            )

    cmd_s="import mod_RestoreHiddenInputs as rhi\nrhi.switch(nuke.thisNode())"
    cmd_u="import mod_RestoreHiddenInputs as rhi\nrhi.upd(nuke.thisNode())"

    k_tab = nuke.Tab_Knob('tb_user','RestoreHiddenInputs')
    k_switch = nuke.PyScript_Knob('bt_switch', 'Hide/Show', cmd_s)
    k_upd = nuke.PyScript_Knob('bt_upd', 'Update Nodes', cmd_u)
    k_store = nuke.String_Knob('tx_store', 'Nodes:', ','.join(all_hidden))

    k_upd.clearFlag(nuke.STARTLINE)

    node_hidden.addKnob(k_tab)
    node_hidden.addKnob(k_switch)
    node_hidden.addKnob(k_upd)
    node_hidden.addKnob(k_store)

    switch(node_hidden)
