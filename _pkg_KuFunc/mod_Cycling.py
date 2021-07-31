'''

one hotkey cycling channels and merge operations

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import platform
import os
from Qt import QtWidgets, QtGui, QtCore
import nuke, nukescripts




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '2.0'
__OS__			= platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "Cycling v%s" % __VERSION__



def _version_():
	ver='''

	version 2.0
	- merge knobChange for output channels
	- add prev mode

	version 1.0
	- one hotkey cycling channels and merge operations

	'''
	return ver




#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




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
			coreCycle('op',n,mode)
		else:
			coreCycle('ch',n,mode)



#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------




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
			if k_count==len(ls_k)-1:
				k_new_idx = 0
			elif k_count < 0:
				k_new_idx = len(ls_k)
			elif mode == 'regular':
				k_new_idx = k_count+1
			elif mode == 'prev'
				k_new_idx = k_count-1
			k_new = ls_k[int(k_new_idx)]
		else:
			k_new = ls_k[0]
		k.setValue(k_new)
		print("%s set to %s" % (node.name(), k_new))
	except:
		print("knob %s not in %s" % (knob, node.name()))


def coreCycle(knob, node, mode):
	'''main cycling operation
	@knob='ch': channels for nodes with channels knob
	@knob='op': operation for merge node
	@mode='regular': often used channels/operations in merge node
	@mode='all': all channels/operations in last selected node
	@mode='prev': switch to previous operation in list
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
		if mode in ['regular', 'prev']:
			ls_op = ['plus', 'minus', 'mask', 'stencil', 'over', 'under', 'max', 'min', 'multiply', 'divide', 'hypot']
		elif mode == 'all':
			ls_op = node['operation'].values()
		setKnob(node, 'operation', ls_op)







#-------------------------------------------------------------------------------
#-Callback Functions
#-------------------------------------------------------------------------------




def ch_merge_out():
	"""channel output for merge node"""
	n = nuke.thisNode()
	k = nuke.thisKnob()
	
	rgbOnly = [
		'plus', 'minus', 'multiply', 'hypot', 
		'color-dodge',  'color-burn', 'average',
		'geometric', 'overlay', 'soft-light',
		]
	
	if k:
		if k.name() == 'operation':
			if k.value() in rgbOnly:
				n['output'].setValue('rgb')
			else:
				n['output'].setValue('rgba')
	else:
		if n['operation'].value() in rgbOnly:
			n['output'].setValue('rgb')
		else:
			n['output'].setValue('rgba')





#-------------------------------------------------------------------------------
#-Adding Callbacks
#-------------------------------------------------------------------------------




nuke.addKnobChanged(ch_merge_out, nodeClass='Merge2')
