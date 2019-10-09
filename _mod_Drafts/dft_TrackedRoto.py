def _version_():
	ver='''

	version 0.0
    - Expression link Roto with Trackers


	'''
	return ver


import nuke, nukescripts
import nuke.rotopaint as rp
import _curvelib as cl




########## Supporting Functions ##########




def findElements():
    '''Find Roto node, Transform node and Curve'''
    '''
    a. Selected Roto, promot Transform, option for Curve
    b. Selected Transform, prompt Roto, Curve layer set to rootLayer
    c. Selected Roto and Transform, prompt for Curve
    '''


    node_roto, node_trans, roto_curve = None, None, None
    class_roto = ['Roto', 'Rotopaint']
    class_transform = ['Transform', 'Tracker4']


    # a. Selected Roto, promot Transform, option for Curve
    if len(sel)==1 and sel[0].Class() in class_roto:
        node_roto = sel[0]
        k = node_roto['curves']
        all_transform = [n.name() for n in nuke.allNodes('Transform')]
        all_curves = [c.name for c in k.rootLayer if isinstance(c, nuke.rotopaint.Shape)]
        p = nuke.Panel("Select Transform node and Shape")
        p.addEnumerationPulldown('MatchMove', ' '.join(all_transform))
        p.addEnumerationPulldown('Shape', ' '.join(all_curves.insert(0,'all')))
        if p.show():
            node_trans = nuke.toNode(p.value('MatchMove')
            sel_shape = p.value('Shape')
            roto_curve = k.getElement(sel_shape) if sel_shape != 'all' else k.rootLayer

    # b. Selected Transform, prompt Roto, Curve layer set to rootLayer
    elif len(sel)==1 and sel[0].Class() in class_transform:
        node_trans = sel[0]
        all_roto = [n.name() for n in nuke.allNodes() if n.Class() in class_roto]
        p = nuke.Panel("Select Roto node")
        p.addEnumerationPulldown('Roto', ' '.join(all_roto.insert(0, 'new')))
        if p.show():
            sel_roto = p.value('Roto')
            node_roto =  nuke.toNode(sel_roto) if sel_roto != 'new' else nuke.createNode('Roto')
            roto_curve = node_roto['curves'].rootLayer

    # c. Selected Roto and Transform, prompt for Curve
    elif len(sel)==2 and [c.Class() for c in sel] in class_roto.extend(class_transform):

        node_roto = [r for r in sel if c.Class() in class_roto][0]
        node_trans = [t for r in sel if t.Class() in class_transform][0]
        if node_roto and node_trans:
            k = node_roto['curves']
            all_curves = [c.name for c in k.rootLayer if isinstance(c, nuke.rotopaint.Shape)]
            p = nuke.Panel("Select Shape")
            p.addEnumerationPulldown('Shape', ' '.join(all_curves.insert(0,'all')))
            if p.show():
                roto_curve = k.getElement(sel_shape) if sel_shape != 'all' else k.rootLayer





    return {r: node_roto, t: node_trans, c: roto_curve}




def linkRoto(node_roto, node_trans, roto_curve):
	'''
    source: https://gist.github.com/jedypod/759871a41a35482704af

	Utility function: Creates a layer in node_roto linked to node_trans
	if node_roto is False, creates a roto node next to tracker node to link to
	'''
	grid_x = int(nuke.toNode('preferences').knob('GridWidth').value())
	grid_y = int(nuke.toNode('preferences').knob('GridHeight').value())

	name_trans = node_trans.name()
	node_trans.setSelected(False)

	# If Roto node not selected, create one.
	if not node_roto:
		node_roto = nuke.nodes.Roto()
		node_roto.setXYpos(node_trans.xpos()-grid_x*0, node_trans.ypos()+grid_y*2)
		node_roto.setSelected(True)

	# Create linked layer in Roto Node, mm - MatchMove
	curves_knob = node_roto["curves"]
	mm_layer = rp.Layer(curves_knob)
	mm_layer.name = "mm_"+name_trans

    # Translate object
	trans_curve_x = cl.AnimCurve()
	trans_curve_y = cl.AnimCurve()

	trans_curve_x.expressionString = "parent.{0}.translate.x".format(name_trans)
	trans_curve_y.expressionString = "parent.{0}.translate.y".format(name_trans)
	trans_curve_x.useExpression = True
	trans_curve_y.useExpression = True

    # Rotate object
	rot_curve = cl.AnimCurve()
	rot_curve.expressionString = "parent.{0}.rotate".format(name_trans)
	rot_curve.useExpression = True

    # Scale object
	scale_curve = cl.AnimCurve()
	scale_curve.expressionString = "parent.{0}.scale".format(name_trans)
	scale_curve.useExpression = True

    # Center object
	center_curve_x = cl.AnimCurve()
	center_curve_y = cl.AnimCurve()
	center_curve_x.expressionString = "parent.{0}.center.x".format(name_trans)
	center_curve_y.expressionString = "parent.{0}.center.y".format(name_trans)
	center_curve_x.useExpression = True
	center_curve_y.useExpression = True

	# Define variable for accessing the getTransform()
	transform_attr = mm_layer.getTransform()
	# Set the Animation Curve for the Translation attribute to the value of the previously defined curve, for both x and y
	transform_attr.setTranslationAnimCurve(0, trans_curve_x)
	transform_attr.setTranslationAnimCurve(1, trans_curve_y)
	# Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
	# http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
	transform_attr.setRotationAnimCurve(2, rot_curve)
	transform_attr.setScaleAnimCurve(0, scale_curve)
	transform_attr.setScaleAnimCurve(1, scale_curve)
	transform_attr.setPivotPointAnimCurve(0, center_curve_x)
	transform_attr.setPivotPointAnimCurve(1, center_curve_y)




########## Main Functions ##########




def TrackedRoto():
    '''Roto with expression linked transform'''

    sel = nuke.selectedNodes()

    if len(sel)<=0:
        nuke.message("Please select a Roto node or Transform node")
    else:
        elem = findElements(sel)
        linkRoto(elem['r'],elem['t'],elem['c'])