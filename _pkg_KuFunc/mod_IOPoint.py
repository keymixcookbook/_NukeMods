
'''

Sets Viewer In and Out point with timeline zoom

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
import platform
import os
from Qt import QtWidgets, QtGui
import re
import logging




#-------------------------------------------------------------------------------
#-Logging
#-------------------------------------------------------------------------------




LOG = logging.getLogger("kplogger")
# LOG.setLevel(logging.DEBUG)
LOG.propagate = False # Turn off nuke logger (https://community.foundry.com/discuss/topic/157139/python-logging?mode=Post&postID=1223446#1223446)




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '1.0'
__OS__			= platform.system()
__AUTHOR__		= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "IOPoint v%s" % __VERSION__


def _version_():
	ver='''

	version 1.0
    - Pop ui for in and out point with str-to-int validation
	- following str validation are accepted:
		- `#-#`: frame to frame
		- `#+#`: frame + duration
		- `-#` : start frame to frame
		- `#-` : frame to end frame
		- `- ` : reset
	- zooming timeline based on in and out point 
	- landing frame set to user defined, else set to In point

	'''
	return ver




#-------------------------------------------------------------------------------
#-GLOBAL VARIABLES
#-------------------------------------------------------------------------------




RE_FF = re.compile("\d+-\d+") 	# Frame to Frame
RE_FD = re.compile("\d+\+\d+") 	# Frame + Duration
RE_SF = re.compile("-\d+") 		# Start to Frame
RE_FE = re.compile("\d+-") 		# Frame to End
RE_RS = re.compile("-") 		# Reset

class CompRangeClass:
	def __init__(self):
		self.first = 1001
		self.last = 1100

	def getRange(self):
		return "%s-%s" % (self.first, self.last)

	def __str__(self):
		return self.getRange()




#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




def IOPoint():
	""" Main Function to call"""

	LOG.debug("IOPoint Called")

	CompRange = CompRangeClass()
	CompRange.first = nuke.root().firstFrame()
	CompRange.last = nuke.root().lastFrame()
	LOG.debug("Comp Range: %s" % CompRange)

	str_in = nuke.getInput("Set In/Out Point")

	if str_in:
		io_range = validate(str_in, CompRange)
		LOG.debug("Validated range: %s" % io_range)
		timeline_zoom(io_range, CompRange)
		LOG.info("Timeline set to %s-%s" % (io_range[0], io_range[1]))	




#-------------------------------------------------------------------------------
#-Supporting Function
#-------------------------------------------------------------------------------




def validate(str_in, CompRange):
	"""validate str input and output corresponding int
	@str_in: (str) user input frame range in string form
	@CompRange: (obj) comp framerange for this session
	return: (str) "####-####" in and out point
	"""
	
	io_range = None 
	str_in = str_in.replace(' ', '')
	ls_frames = [f for f in re.split("\D|\W", str_in)]

	if RE_FF.match(str_in):
		LOG.debug("%s: Frame to Frame" % str_in)
		ls_frames = [int(f) for f in ls_frames]
		io_range = "%s-%s" % (max(ls_frames[0], CompRange.first),min(ls_frames[1], CompRange.last)) 

	elif RE_FD.match(str_in):
		LOG.debug("%s: Frame plus Duration" % str_in)
		ls_frames = [int(f) for f in ls_frames]
		io_range = "%s-%s" % (max(ls_frames[0], CompRange.first),min((ls_frames[0]+ls_frames[1]), CompRange.last))

	elif RE_SF.match(str_in):
		LOG.debug("%s: Start to Frame" % str_in)
		io_range = "%s-%s" % (CompRange.first, ls_frames[1])

	elif RE_FE.match(str_in):
		LOG.debug("%s: Frame to End" % str_in)
		io_range = "%s-%s" % (ls_frames[0], CompRange.last)

	elif RE_RS.match(str_in):
		LOG.debug("%s: Reset" % str_in)
		io_range = "%s-%s" % (CompRange.first, CompRange.last) 

	else:
		io_range = "%s-%s" % (CompRange.first, CompRange.last) 
	
	return io_range


def timeline_zoom(io_range, CompRange):
	"""zooms the timeline to in and out point
	resets if in and out is full range.
	@io_range: (list of ints) user defined in and out point
	@CompRange: (obj) comp frame range for this session
	"""

	node_viewer = nuke.activeViewer().node()
	lock_activate = True if io_range != CompRange.getRange() else False
	node_viewer['frame_range'].setValue(io_range)
	node_viewer['frame_range_lock'].setValue(lock_activate)
	nuke.frame(int(io_range.split('-')[0]))

	app = QtWidgets.QApplication
	slider_widget = None
	for n in app.allWidgets():
		if n.toolTip() == "FrameSlider Range": slider_widget = n
	a = slider_widget.actions()[0]
	mode = 2 if lock_activate else 0
	a.menu().actions()[mode].trigger()
