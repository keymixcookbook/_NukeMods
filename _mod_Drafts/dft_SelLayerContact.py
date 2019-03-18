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
			
			
		
