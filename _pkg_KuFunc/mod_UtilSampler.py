
'''

Module to Sample utility passes from viewer

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
import platform
import os




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '1.0'
__OS__			= platform.system()
__AUTHOR__		= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "UtilSampler v%s" % __VERSION__


def _version_():
	ver='''

	version 1.0
    - Features

	'''
	return ver




#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




def UtilSampler(aov):
	"""Sample aov passe of a active viewer and its input
	Copy to xyz translate knob with node selected, print out values otherwise
	@aov: (str) name of the aov layer to sample
	"""

	node_viewer = nuke.activeViewer().node()
	active_input = nuke.ViewerWindow.activeInput(nuke.activeViewer())
	node_sample = node_viewer.input(active_input)

	bbox_sample = node_viewer['colour_sample_box']
	bbox = [bbox_sample.x(), bbox_sample.y()*aspect]

	viewer_format = [node_sample.width(), node_sample.height()]
	dim = [d/2 for d in viewer_format]
	aspect = float(dim[0])/float(dim[1])

	coord = [
		int(round(bbox[0]*dim[0]+dim[0])),
		int(round(bbox[1]*dim[1]+dim[1]))
	]

	if aov in nuke.layers(node_sample):
		sample_value = [
			nuke.sample(node_sample, aov+'.red', coord[0], coord[1], 1, 1),
			nuke.sample(node_sample, aov+'.green', coord[0], coord[1], 1, 1),
			nuke.sample(node_sample, aov+'.blue', coord[0], coord[1], 1, 1)
		]
		print("Sample %s: %s" % (node_sample.name(), sample_value))

		if nuke.selectedNodes() != []:
			node = nuke.selectedNode()
			k = node.knob('translate')
			if k:
				if k.Class() == 'XYZ_Knob':
					k.setValue(sample_value)
	else:
		print("Layer (%s) does not exist" % aov)



