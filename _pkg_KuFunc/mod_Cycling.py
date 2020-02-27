def _version_():
	ver='''

	version 0.0
	- one hotkey cycling channels and merge operations

	'''
	return ver


import nuke, nukescripts




########## Supporting Functions ##########




def setKnob(node, knob, ls_k):
	'''loop and set knob values
	@n: node, obj
	@knob:knob name, str
	@ls_k: list of knob values, list
	'''
	try:
		k = node[knob]
		k_cur = k.value()
		k_new = None
		if k_cur in ls_k:
			k_count = ls_k.index(k_cur)
			k_new_idx = 0 if k_count==len(ls_k)-1 else k_count+1
			k_new = ls_k[int(k_new_idx)]
		else:
			k_new = ls_k[0]
		k.setValue(k_new)
		print "%s set to %s" % (node.name(), k_new)
	except:
		print "knob %s not in %s" % (knob, node.name())



def coreCycle(knob, node, mode):
	'''main cycling operation
	@knob='ch': channels for nodes with channels knob
	@knob='op': operation for merge node
	@mode='regular': often used channels/operations in merge node
	@mode='all': all channels/operations in last selected node
	@node: input node, obj
	'''
	if knob=='ch':
		ls_ch = []
		if mode == 'regular':
			ls_ch = ['rgb', 'rgba', 'alpha','all']
		elif mode == 'all':
			# unconnected nodes will return empty list
			ls_ch = nuke.layers(node) if nuke.layers(node) else ['rgb', 'rgba', 'alpha','all']

		if node.Class() == 'Shuffle':
			try:
				ls_ch.remove('all')
			except: pass
			setKnob(node,'in',ls_ch)
		else:
			setKnob(node,'channels', ls_ch)
	elif knob=='op':
		ls_op = []
		if mode == 'regular':
			ls_op = ['plus', 'minus', 'mask', 'stencil', 'over', 'under', 'max', 'min', 'hypot']
		elif mode == 'all':
			ls_op = node['operation'].values()
		setKnob(node, 'operation', ls_op)




########## Main Functions ##########




def Cycling(mode='regular'):
	'''main fucntion
	@mode='regular': often used channels/operations in merge node
	@mode='all': all channels/operations in last selected node
	'''
	n = nuke.selectedNode()
	if n == None:
		nuke.message('Please select a node')
	else:
		if n.Class()=='Merge2':
			rgbOnly = ['plus', 'minus', 'multiply', 'hypot']
			coreCycle('op',n,mode)
			if n['operation'].value() in rgbOnly:
				n['output'].setValue('rgb')
			else:
				n['output'].setValue('rgba')
		else:
			coreCycle('ch',n,mode)
