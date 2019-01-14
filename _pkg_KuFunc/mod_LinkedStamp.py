def linkedStamp():

    '''
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

    py_cmd = "n=nuke.thisNode()\nn.setInput(0, nuke.toNode(n['label'].value()))"


    k_tab = nuke.Tab_Knob("LinkedStamp")
    k_setInput = nuke.PyScript_Knob('link', "Set Input", py_cmd)
    k_text = nuke.Text_Knob('tx_nodename', "Set Input to: ")

    stp.addKnob(k_tab)
    stp.addKnob(k_text)
    stp.addKnob(k_setInput)

    k_setInput.setTooltip("Taking the node name from label and connect")
    k_text.setValue("<b>%s</b>" % (stp['label'].value()))
    
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