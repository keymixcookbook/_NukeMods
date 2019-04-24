import nuke

elements = []

def getElements(layer):
    for element in layer:
        if isinstance(element, nuke.rotopaint.Layer):
            getElements(element)
        elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
            elements.append(element)
        return elements

def autolife():
    n = nuke.selectedNode()

    node_curve = n['curves']
    nlayer = node_curve.rootLayer

    global elements
    # Clear global elements array so that only the current Roto/Rotopaint node's elements are 'autolifed'
    elements = []
    getElements(nlayer)

    selNode = None
    try:
        selNode = nuke.selectedNode()
        selXpos = selNode.xpos()
        selYpos = selNode.ypos()
    except ValueError: # no node selected
        pass

    for element in selNode['curves'].getSelected():
        # Get keyframes for the 0-indexed control point
        if isinstance(element, nuke.rotopaint.Stroke):
            keys = element[0].getControlPointKeyTimes()
        elif isinstance(element, nuke.rotopaint.Shape):
            keys = element[0].center.getControlPointKeyTimes()

        firstKey = keys[0]
        lastKey = keys[-1]

        attrs = element.getAttributes()
        attrs.set('ltn', firstKey) # frame range 'from' value
        attrs.set('ltm', lastKey) # frame range 'to' value
        attrs.set('ltt', 4) # set 'lifetime type' of element to 'frame range' - index 4 in combobox

        node_curve.changed()
