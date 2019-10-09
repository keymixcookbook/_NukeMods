import nuke.rotopaint as rp
import _curvelib as cl

def link_roto(tracker_node, node_roto=False):
	'''
    source: https://gist.github.com/jedypod/759871a41a35482704af

	Utility function: Creates a layer in node_roto linked to tracker_node
	if node_roto is False, creates a roto node next to tracker node to link to
	'''
	grid_x = int(nuke.toNode('preferences').knob('GridWidth').value())
	grid_y = int(nuke.toNode('preferences').knob('GridHeight').value())

	tracker_name = tracker_node.name()
	tracker_node.setSelected(False)

	# If Roto node not selected, create one.
	if not node_roto:
		node_roto = nuke.nodes.Roto()
		node_roto.setXYpos(tracker_node.xpos()-grid_x*0, tracker_node.ypos()+grid_y*2)
		node_roto.setSelected(True)

	# Create linked layer in Roto Node, mm - MatchMove
	curves_knob = node_roto["curves"]
	mm_layer = rp.Layer(curves_knob)
	mm_layer.name = "mm_"+tracker_name

    # Translate object
	trans_curve_x = cl.AnimCurve()
	trans_curve_y = cl.AnimCurve()

	trans_curve_x.expressionString = "parent.{0}.translate.x".format(tracker_name)
	trans_curve_y.expressionString = "parent.{0}.translate.y".format(tracker_name)
	trans_curve_x.useExpression = True
	trans_curve_y.useExpression = True

    # Rotate object
	rot_curve = cl.AnimCurve()
	rot_curve.expressionString = "parent.{0}.rotate".format(tracker_name)
	rot_curve.useExpression = True

    # Scale object
	scale_curve = cl.AnimCurve()
	scale_curve.expressionString = "parent.{0}.scale".format(tracker_name)
	scale_curve.useExpression = True

    # Center object
	center_curve_x = cl.AnimCurve()
	center_curve_y = cl.AnimCurve()
	center_curve_x.expressionString = "parent.{0}.center.x".format(tracker_name)
	center_curve_y.expressionString = "parent.{0}.center.y".format(tracker_name)
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
curves_knob.rootLayer.append(mm_layer)