"""

Connect to a node with hidden inputs to keep script logically clean

"""




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
import platform
import os




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__='1.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__WEBSITE__="jiangovfx.com"
__COPYRIGHT__="copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__=__name__.split('_')[1].split('.')[0]

def _version_():
	ver="""

	version 3.4
	- add deep data output check
	- adding marking function
	- use nuke built-in setName()
	- disable knobChanged callback

	version 3.3
	- added shortcut to reconnect

	version 3.2
	- Change Deep node linkStamp from Dot to NoOp
	- Dynamically change knobChanged() effected Class
	- remove node name from autolabel
	- change note_font when disconnected

	version 3.1
	- if topnode is a roto node, change tile_color to match
	- add a PyScript button, copy current LinkedStamp and its input
	- If selected node is `Deep`, use `Dot` node

	version 3.0
	- added Button, Show Parent Node in DAG
	- Change name to "LinkedStamp"

	version 2.1
	- added Python_button, connect to a node listed in Label

	version 2.0
	- added Callback, label changes when input changed

	version 0
	- Postage Stamp with hidden inputs
	"""
	return ver




# ------------------------------------------------------------------------------
# Globale Variable
# ------------------------------------------------------------------------------




MARKER_NAME = 'tb_linkedstamp_marker'
MARKED_LABEl = '\nLinkedStamp Marked'
BASE_NAME = 'LinkedStamp'



# ------------------------------------------------------------------------------
# Main Functions
# ------------------------------------------------------------------------------




def LinkedStamp(mode='set'):
	"""Main function
	mode='set': creating link (default)
	mode='reconnect': reconnect
	mode='marking': marking a node for LinkedStamp to connect to
	"""

	node_parent = nuke.selectedNode()

	if mode == 'set':
		node_parent_nam = node_parent.name()
		node_slave = None

		if isOutputDeep(node_parent):
			node_slave = nuke.nodes.NoOp()
		else:
			node_slave = nuke.nodes.PostageStamp()
			node_slave['postage_stamp'].setValue(True)

		stpMarking(node_parent)
		node_slave.setInput(0, node_parent)

		node_slave['hide_input'].setValue(1)
		node_slave['label'].setValue('linked to: [value tx_nodename]')
		node_slave['tile_color'].setValue(stpColor(node_parent))
		node_slave.setName(BASE_NAME)
		node_slave.setXYpos(node_parent.xpos()+75,node_parent.ypos()+25)

		node_slave['postage_stamp'].setValue(False) if node_parent.Class().startswith('Roto') else node_slave['postage_stamp'].setValue(True)

		# Add User knobs
		py_cmd_restore= "n=nuke.thisNode()\nn.setInput(0, nuke.toNode(n['connect'].value()))"
		py_cmd_orig = "origNode = nuke.thisNode().input(0);\
						origXpos = origNode.xpos();\
						origYpos = origNode.ypos();\
						nuke.zoom(2, [origXpos,origYpos]);\
						nuke.thisNode()['selected'].setValue(False);\
						origNode['selected'].setValue(True);\
						nuke.show(origNode)"

		py_cmd_copy = "origNode = nuke.thisNode().input(0);\
						filter(lambda n: n.setSelected(False), nuke.selectedNodes());\
						nuke.thisNode().setSelected(True);\
						nuke.nodeCopy('%clipboard%');\
						new_node = nuke.nodePaste('%clipboard%');\
						new_node.setInput(0, origNode);\
						new_node.setXpos(nuke.thisNode().xpos()+120)"


		k_tab = nuke.Tab_Knob("LinkedStamp")
		k_text = nuke.String_Knob('tx_nodename', "Set Input to: ")
		k_enable = nuke.Boolean_Knob('ck_enable', "Enable")
		k_setInput = nuke.PyScript_Knob('link', "Set Input", py_cmd_restore)
		k_showParent = nuke.PyScript_Knob('orig', "Show Parent Node", py_cmd_orig)
		k_copy = nuke.PyScript_Knob('copy', "Copy this Node", py_cmd_copy)
		k_connect = nuke.String_Knob('connect','toConnect',node_parent_nam)

		k_setInput.setFlag(nuke.STARTLINE)
		k_text.setEnabled(False)
		k_enable.clearFlag(nuke.STARTLINE)
		k_showParent.clearFlag(nuke.STARTLINE)
		k_copy.clearFlag(nuke.STARTLINE)
		k_connect.setFlag(nuke.INVISIBLE)

		node_slave.addKnob(k_tab)
		node_slave.addKnob(k_text)
		node_slave.addKnob(k_enable)
		node_slave.addKnob(k_setInput)
		node_slave.addKnob(k_showParent)
		node_slave.addKnob(k_copy)
		node_slave.addKnob(k_connect)

		k_text.setValue(node_slave['connect'].value())
		k_setInput.setTooltip("Taking the node name from label and connect")
		k_showParent.setTooltip("Show parent node in DAG")
		k_copy.setTooltip("Copy this node with its inputs")

		node_slave['knobChanged'].setValue('k=nuke.thisKnob()\nif k.name()=="ck_enable":\n\tnuke.thisNode()["tx_nodename"].setEnabled(k.value())')
		node_slave['autolabel'].setValue("('Disconnected from\\n' if len(nuke.thisNode().dependencies())<=0 else 'Linked to\\n')+nuke.thisNode()['tx_nodename'].value()")
	
	elif mode=='reconnect':
		node_parents = nuke.selectedNodes()
		for n in node_parents:
			if n['LinkedStamp'].value():
				n.setInput(0, nuke.toNode(n['connect'].value()))

	elif mode =='marking':
		for n in nuke.selectedNodes():
			stpMarking(n)




# ------------------------------------------------------------------------------
# Supporting Functions
# ------------------------------------------------------------------------------




def stpRename(BASE_NAME):
	"""Replaced with built-in node.setName()"""
	"""Rename LinkedStamp to avoid conflict"""

	all_stp = [n.name() for n in nuke.allNodes() if BASE_NAME in n.name()]

	if len(all_stp) > 0:
		stp_max = max(all_stp)
	else:
		stp_max = BASE_NAME + "1"

	new_index = int(stp_max.strip(BASE_NAME))+1
	new_name = BASE_NAME+str(new_index)

	return new_name

def stpColor(node_parent):
	"""Find topnode Class and set tile_color"""

	node_top_name = nuke.tcl("full_name [topnode %s]" % node_parent.name())
	node_top_class = nuke.toNode(node_top_name).Class()
	node_color = 0

	if node_top_class.startswith('Roto'):
		node_color = 1908830719 # system roto class color
	elif node_top_class.startswith('Deep'):
		node_color = 24831 # system deep class color
	else:
		node_color = 12040191 # pascal cyan

	return node_color

def stpMarking(node_parent):
	"""mark node to be recongnized by LinkedStamp
	(called everytime in set mode before connect)
	@node: (obj) parent node that is initially selected
	"""

	if not node_parent.knob(MARKER_NAME):

		k_mark = nuke.Tab_Knob(MARKER_NAME,'LinkedStamp Marker')
		k_mark_label = nuke.Text_Knob('tx_linkedstamp_marker', "","This node is marked by LinkedStamp")
		node_parent.addKnob(k_mark)
		node_parent.addKnob(k_mark_label)
		node_parent['label'].setValue(node_parent['label'].value())
		print("%s LinkedStamp Marked" % node_parent.name())
	else:
		print("New LinkedStamp from: %s" % node_parent.name())


def isOutputDeep(node):
	"""check if node is outputing deep data
	@node: (obj) root node of the tree
	return: (bool) True if is deep, False otherwise
	"""
	outputdeep=None
	try: node.deepSampleCount(0,0); outputdeep = True
	except: outputdeep = False

	return outputDeep

# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------




def inputUpdate():

	n = nuke.thisNode()
	k = nuke.thisKnob()
	if n.Class() in ['PostageStamp', 'NoOp']:
		if k.name() == "inputChange":
			if len(n.dependencies())<=0:
				n['note_font'].setValue('bold')
				n['note_font_color'].setValue(3623878911) # Dark Red
				n['hide_input'].setValue(False)
				print '%s disconnected' % n.name()
			elif len(n.dependencies())>0:
				n['connect'].setValue(n.dependencies()[0].name())
				n['tx_nodename'].setValue(n['connect'].value())
				n['note_font'].setValue('')
				n['note_font_color'].setValue(0)
				n['hide_input'].setValue(True)
				print '%s connected' % n.name()
		elif k.name() == 'tx_nodename':
			n['connect'].setValue(k.value())


# nuke.addKnobChanged(inputUpdate, nodeClass='PostageStamp')
# nuke.addKnobChanged(inputUpdate, nodeClass='NoOp')
