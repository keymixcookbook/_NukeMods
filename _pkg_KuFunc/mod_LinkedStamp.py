import nuke

def LinkedStamp():

    '''
    version 3.0
        - added Button, Show Parent Node in DAG
    
    version 2.1
        - added Python_button, connect to a node listed in Label

    version 2.0
        - added Callback, label changes when input changed

    '''

    rNode = nuke.selectedNode()
    rNode_nam = rNode.name()

    rNode['selected'].setValue(False)

    stp = nuke.createNode('PostageStamp')
    stp.setInput(0, rNode)
    stp['hide_input'].setValue(1)
    stp['label'].setValue(rNode_nam)

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


    k_tab = nuke.Tab_Knob("LinkedStamp")
    k_text = nuke.Text_Knob('tx_nodename', "Set Input to: ")
    k_setInput = nuke.PyScript_Knob('link', "Set Input", py_cmd_restore)
    k_showParent = nuke.PyScript_Knob('orig', "Show Parent Node", py_cmd_orig)
    k_showParent.clearFlag(nuke.STARTLINE)

    stp.addKnob(k_tab)
    stp.addKnob(k_text)
    stp.addKnob(k_setInput)
    stp.addKnob(k_showParent)

    k_text.setValue("<b>%s</b>" % (stp['label'].value()))
    k_setInput.setTooltip("Taking the node name from label and connect")
    k_showParent.setTooltip("Show parent node in DAG")

    def inputUpdate():

        n = nuke.thisNode()
        k = nuke.thisKnob()

        try:
            if k.name() == "inputChange":
                n['label'].setValue(n.dependencies()[0].name())
                n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))
        except:
            pass

        if k.name() == "label": # Manually Change Label
            n['tx_nodename'].setValue("<b>%s</b>" % (stp['label'].value()))


    nuke.addKnobChanged(inputUpdate, nodeClass='PostageStamp')
