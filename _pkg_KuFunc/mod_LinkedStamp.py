def _version_():
    ver='''

    version 3.3
    - added shortcut to reconnect
    
    version 3.2
    - Change Deep node linkStamp from Dot to NoOp
    - Dynamically change knobChanged() effected Class
    - remove node name from autolabel
    - change note_font when disconnected

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

    all_stp = [n.name() for n in nuke.allNodes() if base_name in n.name()]

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




def LinkedStamp(mode='set'):
    '''Main function
    mode='set': creating link (default)
    mode='reconnect': reconnect
    ''' 

    rNode = nuke.selectedNode()
    
    if mode == 'set':
        rNode_nam = rNode.name()
        base_name = "LinkStamp"
        stp = None

        if rNode.Class().startswith('Deep'):
            stp = nuke.nodes.NoOp()
        else:
            stp = nuke.nodes.PostageStamp()

        stp.setInput(0, rNode)
        stp['hide_input'].setValue(1)
        stp['postage_stamp'].setValue(True)
        #stp['label'].setValue(rNode_nam)
        stp['tile_color'].setValue(stpColor(rNode))
        stp.setName(stpRename(base_name))
        stp.setXpos(rNode.xpos()+75,rNode.ypos()+25)

        #stp['postage_stamp'].setValue(False) if rNode.Class().startswith('Roto') else stp['postage_stamp'].setValue(True)

        # Add User knobs
        py_cmd_restore= "n=nuke.thisNode()\nn.setInput(0, nuke.toNode(n['connect'].value()))"
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
        k_text = nuke.String_Knob('tx_nodename', "Set Input to: ")
        k_enable = nuke.Boolean_Knob('ck_enable', "Enable")
        k_setInput = nuke.PyScript_Knob('link', "Set Input", py_cmd_restore)
        k_showParent = nuke.PyScript_Knob('orig', "Show Parent Node", py_cmd_orig)
        k_copy = nuke.PyScript_Knob('copy', "Copy this Node", py_cmd_copy)
        k_connect = nuke.String_Knob('connect','toConnect',rNode_nam)

        k_setInput.setFlag(nuke.STARTLINE)
        k_text.setEnabled(False)
        k_enable.clearFlag(nuke.STARTLINE)
        k_showParent.clearFlag(nuke.STARTLINE)
        k_copy.clearFlag(nuke.STARTLINE)
        k_connect.setFlag(nuke.INVISIBLE)

        stp.addKnob(k_tab)
        stp.addKnob(k_text)
        stp.addKnob(k_enable)
        stp.addKnob(k_setInput)
        stp.addKnob(k_showParent)
        stp.addKnob(k_copy)
        stp.addKnob(k_connect)


        k_text.setValue(stp['connect'].value())
        k_setInput.setTooltip("Taking the node name from label and connect")
        k_showParent.setTooltip("Show parent node in DAG")
        k_copy.setTooltip("Copy this node with its inputs")

        stp['knobChanged'].setValue('k=nuke.thisKnob()\nif k.name()=="ck_enable":\n\tnuke.thisNode()["tx_nodename"].setEnabled(k.value())')
        stp['autolabel'].setValue("('Disconnected from\\n' if len(nuke.thisNode().dependencies())<=0 else 'Linked to\\n')+nuke.thisNode()['tx_nodename'].value()")
    elif mode=='reconnect':
        rNodes = nuke.selectedNodes()
        for n in rNodes:
            if n['LinkedStamp'].value():
                n.setInput(0, nuke.toNode(n['connect'].value()))


def inputUpdate():

    n = nuke.thisNode()
    k = nuke.thisKnob()
    if n.Class() in ['PostageStamp', 'NoOp']:
        if k.name() == "inputChange":
            if len(n.dependencies())<=0:
                n['note_font'].setValue('bold')
                n['note_font_color'].setValue(3623878911) # Dark Red
                n['hide_input'].setValue(False)
                print '%s disconnected' % n.name()
            elif len(n.dependencies())>0:
                n['connect'].setValue(n.dependencies()[0].name())
                n['tx_nodename'].setValue(n['connect'].value())
                n['note_font'].setValue('')
                n['note_font_color'].setValue(0)
                n['hide_input'].setValue(True)
                print '%s connected' % n.name()
        elif k.name() == 'tx_nodename':
            n['connect'].setValue(k.value())


nuke.addKnobChanged(inputUpdate, nodeClass='PostageStamp')
nuke.addKnobChanged(inputUpdate, nodeClass='NoOp')
