'''

Read and process _configShow.json and _configShot.json

'''




def _version_():
	ver='''

	version 0.0
	- Read WSLENV slate variable, find cooresponding config file
	- set nuke root settings on start

	'''
	return ver




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts
import json
import os
import slate
from kputl import *




#------------------------------------------------------------------------------
#-Main Function
#------------------------------------------------------------------------------




def ShotConfig():
	'''set startup settins when launch nuke'''

	if slate.SHOW_CONFIG and slate.SHOT_CONFIG != None:
		# Format
		format_name = slate.SHOW_CONFIG['kp_show']+'-format'
		showFormat = '%s %s %s' % (slate.SHOW_CONFIG['root_format'][0], slate.SHOW_CONFIG['root_format'][1], format_name)
		nuke.addFormat(showFormat)

		root = nuke.root()
		root['format'].setValue(format_name)
		root['fps'].setValue(slate.SHOW_CONFIG['fps'])
		root['first_frame'].setValue(slate.SHOT_CONFIG['frameStart'])
		root['last_frame'].setValue(slate.SHOT_CONFIG['frameEnd'])
		root['lock_range'].setValue(True)
		root['frame'].setValue(slate.SHOT_CONFIG['frameStart'])
		os.environ['OCIO'] = slate.SHOW_CONFIG['colorspace']

		if 'NUKE_PATH' in os.environ.keys():
			os.environ['NUKE_PATH'] += ';%s' % slate.SHOW_TOOL_DIR
		else:
			os.environ['NUKE_PATH'] = slate.SHOW_TOOL_DIR

		print("...nuke configured")




#------------------------------------------------------------------------------
#-Default startup settings root add on create
#------------------------------------------------------------------------------



#ShotConfig()
nuke.addOnCreate(ShotConfig, nodeClass='Root')
