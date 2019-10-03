def _version_():
    ver='''

    version 3.2
    - Change Deep node linkStamp from Dot to NoOp
    - Dynamically change knobChanged() effected Class
    
    version 3.1
    - if topnode is a roto node, change tile_color to match
    - add a PyScript button, copy current LinkedStamp and its input
    - If selected node is `Deep`, use `Dot` node

    version 3.0
    - added Button, Show Parent Node in DAG
    - Change name to "LinkedStamp"

    version 2.1
    - added Python_button, connect to a node listed in Label

    version 2.0
    - added Callback, label changes when input changed

    version 0
    - Postage Stamp with hidden inputs
    '''
    return ver




import nuke, nukescripts




########## Supporting Function #########




def stpRename(base_name):

    all_stp = [n.name() for n in nuke.allNodes('PostageStamp') if base_name in n.name()]

    if len(all_stp) > 0:
        stp_max = max(all_stp)
    else:
        stp_max = base_name + "1"

    new_index = int(stp_max.strip(base_name))+1
    new_name = base_name+str(new_index)

    return new_name



def stpColor(rNode):
    '''Find topnode Class and set tile_color'''

    node_top_name = nuke.tcl("full_name [topnode %s]" % rNode.name())
    node_top_class = nuke.toNode(node_top_name).Class()
    node_color = 0

    if node_top_class.startswith('Roto'):
        node_color = 1908830719 # system roto class color
    elif node_top_class.startswith('Deep'):
        node_color = 24831 # system deep class color
    else:
        node_color = 12040191 # pascal cyan

    return node_color




########## Main Function #########




def LinkedStamp():

    rNode = nuke.selectedNode()
    rNode_nam = rNode.name()
    base_name = "LinkStamp"
    rNode.setSelected(False)
    stp = None

    if rNode.Class().startswith('Deep'):
        stp = nuke.createNode('NoOp')
    else:
        stp = nuke.createNode('PostageStamp')

    stp.setInput(0, rNode)
    stp['hide_input'].setValue(1)
    stp['label'].setValue(rNode_nam)
    stp['tile_color'].setValue(stpColor(rNode))
    stp.setName(stpRename(base_name))

    stp['postage_stamp'].setValue(False) if rNode.Class().startswith('Roto') else stp['postage_stamp'].setValue(True)

    # Reset Selections
    stp['selected'].setValue(False)
    rNode['selected'].setValue(True)

    # Add User knobs
    py_cmd_restore= "n=nuke.thisNode()\nn.setInput(0, nuke.toNode(n['label'].value()))"
    py_cmd_orig = "origNode = nuke.thisNode().input(0);\
                    origXpos = origNode.xpos();\
                    origYpos = origNode.ypos();\
                    nuke.zoom(2, [origXpos,origYpos]);\
                    nuke.thisNode()['selected'].setValue(False);\
                    origNode['selected'].setValue(True);\
                    nuke.show(origNode)"

    py_cmd_copy = "origNode = nuke.thisNode().input(0);\
                    filter(lambda n: n.setSelected(False), nuke.selectedNodes());\
                    nuke.thisNode().setSelected(True);\
                    nuke.nodeCopy('%clipboard%');\
                    new_node = nuke.nodePaste('%clipboard%');\
                    new_node.setInput(0, origNode);\
                    new_node.setXpos(nuke.thisNode().xpos()+120)"


    k_tab = nuke.Tab_Knob("LinkedStamp")
    k_text = nuke.Text_Knob('tx_nodename', "Set Input to: ")
    k_setInput = nuke.PyScript_Knob('link', "Set Input", py_cmd_restore)
    k_showParent = nuke.PyScript_Knob('orig', "Show Parent Node", py_cmd_orig)
    k_copy = nuke.PyScript_Knob('copy', "Copy this Node", py_cmd_copy)

    k_setInput.setFlag(nuke.STARTLINE)
    k_showParent.clearFlag(nuke.STARTLINE)
    k_copy.clearFlag(nuke.STARTLINE)

    stp.addKnob(k_tab)
    stp.addKnob(k_text)
    stp.addKnob(k_setInput)
    stp.addKnob(k_showParent)
    stp.addKnob(k_copy)

    k_text.setValue("<b>%s</b>" % (stp['label'].value()))
    k_setInput.setTooltip("Taking the node name from label and connect")
    k_showParent.setTooltip("Show parent node in DAG")
    k_copy.setTooltip("Copy this node with its inputs")

    def inputUpdate():

        n = nuke.thisNode()
        k = nuke.thisKnob()

        try:
            if k.name() == "inputChange":
                n['label'].setValue(n.dependencies()[0].name())
                n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))
                stpColor(nuke.inputs(0))
        except:
            pass

        if k.name() == "label": # Manually Change Label
            n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))


    nuke.addKnobChanged(inputUpdate, nodeClass=stp.Class())
