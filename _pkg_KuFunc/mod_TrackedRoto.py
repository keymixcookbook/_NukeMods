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




def findElements(sel):
	'''Find Roto node, Transform node and Curve'''
	'''
	a. Selected Roto, promot Transform, option for Curve
	b. Selected Transform, prompt Roto, Curve layer set to rootLayer
	c. Selected Roto and Transform, prompt for Curve
	'''

	sel = nuke.selectedNodes()
	node_roto, node_trans, roto_curve, op_cancel = None, None, None, False
	type_roto = ['Roto', 'Rotopaint']
	type_transform = ['Transform', 'Tracker4']
	type_all = type_roto+type_transform
	type_sel = [c.Class() for c in sel]


	if len(sel)==1:

		# a. Selected Roto, promot Transform, option for Curve
		if sel[0].Class() in type_roto:
			print "Selected Roto"
			node_roto = sel[0]
			k = node_roto['curves']
			all_transform = [n.name() for n in nuke.allNodes('Transform')]
			all_curves = [c.name for c in k.rootLayer if isinstance(c, nuke.rotopaint.Shape)]
			all_curves.insert(0,'all')
			p = nuke.Panel("Select Transform node and Shape")
			p.addEnumerationPulldown('MatchMove', ' '.join(all_transform))
			p.addEnumerationPulldown('Shape', ' '.join(all_curves))
			if p.show():
				node_trans = nuke.toNode(p.value('MatchMove'))
				sel_shape = p.value('Shape')
				roto_curve = k.toElement(sel_shape) if sel_shape != 'all' else k.rootLayer
			else:
				op_cancel = True

		# b. Selected Transform, prompt Roto, Curve layer set to rootLayer
		# b. Rename transform node
		elif sel[0].Class() in type_transform:

			# # Create Roto node from Transform
			# print "Selected Transform"
			# node_trans = sel[0]
			# all_roto = [n.name() for n in nuke.allNodes() if n.Class() in type_roto]
			# all_roto.insert(0, 'new')
			# p = nuke.Panel("Select Roto node")
			# p.addEnumerationPulldown('Roto', ' '.join(all_roto))
			# if p.show():
			# 	sel_roto = p.value('Roto')
			# 	node_roto =  nuke.toNode(sel_roto) if sel_roto != 'new' else nuke.nodes.Roto(output='alpha', cliptype='no clip')
			# 	roto_curve = node_roto['curves'].rootLayer
			# else:
			# 	op_cancel = True

			# Rename Transform Node
			ls_transform_type = ['MatchMove', 'Stabalize']
			node_transform = sel[0]
			p = nuke.Panel("Rename Transform Node")
			p.addEnumerationPulldown('type: ', ' '.join(ls_transform_type))
			p.addSingleLineInput('rename: ')
			if p.show():
				sel_type = p.value('type: ')
				sel_rename = p.value('rename: ')

				node_transform.setName('%s_%s' % (sel_rename, sel_type))
			else:
				op_cancel = True


	elif len(sel)==2:

		node_roto = [r for r in sel if r.Class() in type_roto][0]
		node_trans = [t for t in sel if t.Class() in type_transform][0]

		# c. Selected Roto and Transform, prompt for Curve
		if node_roto and node_trans:
			print "Selected Roto and Transform"
			k = node_roto['curves']
			all_curves = [c.name for c in k.rootLayer if isinstance(c, nuke.rotopaint.Shape)]
			all_curves.insert(0,'all')
			p = nuke.Panel("Select Shape")
			p.addEnumerationPulldown('Shape', ' '.join(all_curves))
			if p.show():
				sel_shape = p.value('Shape')
				roto_curve = k.toElement(sel_shape) if sel_shape != 'all' else k.rootLayer
			else:
				op_cancel = True


	return {'r': node_roto, 't': node_trans, 'c': roto_curve, 'op': op_cancel}




def linkRoto(node_roto, node_trans, roto_curve):
	'''
	source: https://gist.github.com/jedypod/759871a41a35482704af

	Utility function: Creates a layer in node_roto linked to node_trans
	if node_roto is False, creates a roto node next to tracker node to link to
	'''

	name_trans = node_trans.name()
	node_trans.setSelected(False)

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
	transform_attr = roto_curve.getTransform()
	transform_attr.setTranslationAnimCurve(0, trans_curve_x)
	transform_attr.setTranslationAnimCurve(1, trans_curve_y)
	transform_attr.setRotationAnimCurve(2, rot_curve)
	transform_attr.setScaleAnimCurve(0, scale_curve)
	transform_attr.setScaleAnimCurve(1, scale_curve)
	#transform_attr.setPivotPointAnimCurve(0, center_curve_x)
	#transform_attr.setPivotPointAnimCurve(1, center_curve_y)






########## Main Functions ##########




def TrackedRoto():
	'''Roto with expression linked transform'''

	sel = nuke.selectedNodes()

	if len(sel)<=0:
		nuke.message("Please select a Roto node or Transform node")
	else:
		elem = findElements(sel)
		if elem['op'] == True:
			print "Operation Cancelled"
			pass
		else:
			linkRoto(elem['r'],elem['t'],elem['c'])
			print "{}.{} linked to {}".format(elem['r'].name(),elem['c'].name,elem['t'].name())
