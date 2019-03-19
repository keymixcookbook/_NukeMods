'''

- Show the type of channels selected
- ie. only "id", "spec", "multi", "multiSpecs", or "data"

- Renderman Light: multi[0-9], diffMulti[0-9], specMulti[0-9]. id[0-10], diffCol, diffDir, diffInd, specDir, specInd, emission, subserface
- Renderman Data: depth2, norm, position2, refPosition2, uv2, vel, shadow

- Have Options to view: single layer OR group of layers with a given type[multiLights, diffMulti, specMulti, diff, spec, shading, data]
- Only keep selected layer/layer groups
- Output with LayerContactSheet

'''

import nuke
import collections
import math





########## Supporting Function ###########




def listRemove(ls_main, ls_remove):
	
	for n in ls_remove:
		if n in ls_main:
			ls_main.remove(n)
	
	return ls_main



def removeLayers(node, num_remove, aovs_remove):
	
	'''
	built for works in a group
	'''
	
	remove_nodes = []
	
	# Create Remove node in a chain
	for n in range(num_remove):
		r = nuke.createNode('Remove')
		if n == 0: # first node
			r.setInput(0, node)
		node_remove.append(r)
	
	# Removing Channels
	node_counter = 1
	node_knob_counter = 0
	
	for nr in node_remove:
		print nr.name()
		
		for k in range(4):
			if len(aovs_remove)<=0:
				break
			else:
				if node_knob_counter == 0:
					cur_k = 'channels'
				else:
					cur_k = 'channels%s' % node_knob_counter

				nr[cur_k].setValue(aovs_remove[0])
				print "%s <- %s" % (cur_k, aovs_remove[0])
				del aovs_remove[0]

				node_knob_counter += 1

	# Create Crop and LayerContactSheet node
	node_crop = nuke.createNode('Crop')
	nuke.createNode('LayerContactSheet')
	
	node_crop['box'].setExpression('input.bbox.x', 0)
	node_crop['box'].setExpression('input.bbox.y', 1)
	node_crop['box'].setExpression('input.bbox.r', 2)
	node_crop['box'].setExpression('input.bbox.t', 3)


	
	
	
########## Main Function ###########




def AOVContactSheet():

	node_sel = nuke.selectedNode()

	if node_sel:

		# Collecting Data
		aovs_all = [l for l in nuke.layers(node_sel)]
		mu_sel = ['multi', 'diffMulti', 'specMulti', 'Shading', 'spec', 'diff', 'Data', 'id', 'all']

		# Select AOVs
		p = nuke.Panel('SelLayerContact')
		p.addEnumerationPulldown('AOV Group', ' '.join(aovs_all))

		if p.show():
			aovs_group = p.value('AOV Group')
		else:
			print "Operation Cancelled"
			break

		# Find Matching AOVs
		aovs_sel = []

		for l in aovs_all:
			if aovs_group in l: # diff, spec, multiLights, id
				aovs_sel.append(l)
			elif aovs_group == 'Shading' and l in ['diffDir', 'diffInd', 'specDir', 'specInd', 'emission', 'emission', 'subsurface']:
				aovs_sel.append(l)
			elif aovs_group == 'Data' and l in ['depth', 'norm', 'postion', 'refPosition', 'uv']:
				aovs_sel.append(l)
			elif aovs_group == 'all':
				aovs_sel = aovs_all
				
		# Filter aovs_sel
		## for Remove node, with operation set to 'remove'
		aovs_remove = ls_remove(aovs_all, aovs_sel)

		# Find how many remove nodes needed
		num_remove = int(math.ceil(len(aovs_remove)/4.0))
		
		# Removing unwanted layers
		
