
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




__VERSION__		= '1.1'
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

	version 1.1
	- add landing frame; 
		- landing frame outside the range, set to in or out point, otherwise current frame
		- custom landing frame with a space and a input
	- crawl current frame range when prompt UI

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
RE_LF = re.compile(".+ \d")		# Range & landing Frame

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

	str_in = nuke.getInput("Set In/Out Point", nuke.activeViewer().node()['frame_range'].value())

	if str_in:
		io_range, frame_land = validate(str_in, CompRange)
		LOG.debug("Validated range: %s" % io_range)
		timeline_zoom(io_range, CompRange, frame_land)
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
	if RE_LF.match(str_in):
		LOG.debug("Landing Frame detected")
		str_in, frame_land = str_in.split(' ')
	else:
		str_in = str_in.replace(' ', '')
		frame_land = None

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
	
	return io_range, frame_land


def timeline_zoom(io_range, CompRange, frame_land=None):
	"""zooms the timeline to in and out point
	resets if in and out is full range.
	@io_range: (list of ints) user defined in and out point
	@CompRange: (obj) comp frame range for this session
	@frame_land: (str) landing frame, optional input
	"""

	node_viewer = nuke.activeViewer().node()
	frame_cur = nuke.frame()
	lock_activate = True if io_range != CompRange.getRange() else False
	node_viewer['frame_range'].setValue(io_range)
	node_viewer['frame_range_lock'].setValue(lock_activate)

	# Finds the landing frame
	if not frame_land:
		ls_io_range = [int(f) for f in io_range.split('-')]
		if frame_cur < ls_io_range[0]: frame_land = ls_io_range[0]
		elif frame_cur > ls_io_range[1]: frame_land = ls_io_range[1]
		else: frame_land = frame_cur
	
	nuke.frame(int(frame_land))

	# Zooming
	app = QtWidgets.QApplication
	slider_widget = None
	for n in app.allWidgets():
		if n.toolTip() == "FrameSlider Range": slider_widget = n
	a = slider_widget.actions()[0]
	mode = 2 if lock_activate else 0
	a.menu().actions()[mode].trigger()
