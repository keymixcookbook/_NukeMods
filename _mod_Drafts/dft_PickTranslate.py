import nuke, nukescripts


class Core_PickTranslate(nukescripts.PythonPanel):
    def __init__(self):
        super(Core_PickTranslate, self).__init__('PickTranslate')

        self.k_pick = nuke.Color_Knob('pick', "pick translate")
        self.k_node = nuke.Enumeration_Knob('geo', "pick geo node", [])

        self.addKnob(self.k_pick)
        self.addKnob(self.k_node)

    
    def run(self):
        filter_class = ['Card2', 'Axis2', 'TransformGeo']
        nodes = [n.name() for n in nuke.allNodes() if n.Class() in filter_class]
        self.k_node.setValues(nodes)        
        self.show()


    def knobChanged(self, knob):
        if knob == self.k_pick:
            nuke.toNode(self.k_node.value())['translate'].setValue(knob.value())

PickTranslate = Core_PickTranslate()
PickTranslate.run()