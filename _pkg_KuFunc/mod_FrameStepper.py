
'''

Stepping Over set list of frames

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 
import platform
import os
import json
import logging
from Qt import QtWidgets, QtGui, QtCore
import re
import subprocess




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__VERSION__		= '1.0'
__OS__			= platform.system()
__AUTHOR__		= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		= "FrameStepper v%s" % __VERSION__


def _version_():
	ver='''

	version 1.0
    - UI to get a list of frames
	- saved as JSON data as /SHOW/SHOT/

	'''
	return ver




#-------------------------------------------------------------------------------
#-Logging
#-------------------------------------------------------------------------------




LOG = logging.getLogger('kplogger')




#-------------------------------------------------------------------------------
#-GLOBAL VARIABLE
#-------------------------------------------------------------------------------




DIR_NUKE = os.path.join(os.getenv('HOME', ''), '.nuke')

VAR_SHOW = 'KP_SHOW'
VAR_SHOT = 'KP_SHOT'
SHOW = os.getenv(VAR_SHOW, 'show')
SHOT = os.getenv(VAR_SHOT, 'shot')

JSON_STR = os.path.join(DIR_NUKE, "FrameStepper", (os.getenv(VAR_SHOW)+'.json'))




#-------------------------------------------------------------------------------
#-Main Function
#-------------------------------------------------------------------------------




def FrameStepper(mode=1):
	"""Main Function to step over frames
	@mode: (int) 1 for stepping next, 0 prev
	"""

	LOG.debug("%s | %s" % (SHOW, SHOT))

	ls_frames = get_ls_frames()
	len_frames = len(ls_frames)
	LOG.debug("show: %s | shot: %s | %s" % (SHOW, SHOT, ls_frames))
	frame_cur = nuke.frame()
	LOG.debug("Current Frame: %s" % frame_cur)

	# Find the nearest frame, - and +
	frame_nearest = None
	frame_stepped = [] 
	frame_prev, frame_next = None, None

	if frame_cur in ls_frames: 
		frame_nearest = frame_cur
		idx_cur = ls_frames.index(frame_nearest)

		frame_prev = ls_frames[len_frames-1] 	if idx_cur == 0 else ls_frames[ max([0, idx_cur-1]) ]
		frame_next = ls_frames[0] 				if idx_cur == len_frames-1 else ls_frames[ min([len_frames-1, idx_cur+1]) ]

	else:
		ls_distance = [f-frame_cur for f in ls_frames]
		LOG.debug("Distance between Nearst frames: %s" % ls_distance)
		dis_min = [f for f in ls_distance if f>0]
		dis_max = [f for f in ls_distance if f<0]
		LOG.debug("Distance Next: %s" % dis_min)
		LOG.debug("Distance Prev: %s" % dis_max)

		frame_prev = ls_frames[len_frames-1] 	if dis_max == [] else frame_cur+max(dis_max)
		frame_next = ls_frames[0] 				if dis_min == [] else frame_cur+min(dis_min) 
	
	frame_stepped = [frame_prev, frame_next]
	LOG.debug("Nearest frames: %s" % frame_stepped)
	
	nuke.frame(frame_stepped[mode])




#-------------------------------------------------------------------------------
#-Supporting Functions
#-------------------------------------------------------------------------------




def get_ls_frames():
	"""read and crawl the list of frames from JSON file
	return: (list of int) list of frames
	"""
	JSON_FILE = get_json_file(JSON_STR) 
	json_data = {}
	with open(JSON_FILE, 'r') as f:
		json_data = json.load(f)
	
	return json_data[SHOT]




#-------------------------------------------------------------------------------
#-Util Functions
#-------------------------------------------------------------------------------




def get_json_file(JSON_STR):
	"""System check to return json file, create if not exist
	@JSON_STR: (str) json full file path
	return: (str) json full file path confirmed
	"""

	if not os.path.isfile(JSON_STR):
		LOG.info("JSON file %s does not exist, creating one" % os.path.basename(JSON_STR))
		LOG.debug("Make dir and json file")

		os.makedirs(os.path.dirname(JSON_STR))
		LOG.info("%s created" % JSON_STR)
		
		data = {}
		data[SHOT] = []
		with open(JSON_STR, 'w') as f:
			json_data = json.dumps(data, indent=2)
			f.write(json_data)

		return JSON_STR
	
	else:
		LOG.debug("JSON file %s exist" % JSON_STR)
		return JSON_STR




#-------------------------------------------------------------------------------
#-Custom Widgets
#-------------------------------------------------------------------------------




class FrameSetter(QtWidgets.QWidget):
	def __init__(self, json_file):
		super(FrameSetter, self).__init__()

		self.json_file = json_file

		self.frame_label = QtWidgets.QLabel("Frames to set")
		self.frame_str = QtWidgets.QLineEdit()
		self.frame_str.setMinimumWidth(300)
		self.btn_append = QtWidgets.QPushButton(u"\u2795")
		self.btn_append.setToolTip("Append Current Frame")
		self.btn_append.setStyleSheet("QPushButton {font-weight: bold; font-size: 24pt; background-color: darkgreen}")
		self.btn_append.clicked.connect(self.frame_append)
		self.btn_set = QtWidgets.QPushButton("Set Frames")
		self.btn_set.clicked.connect(self.frames_set)
		self.btn_cancel = QtWidgets.QPushButton("Cancel")
		self.btn_cancel.clicked.connect(self.close)

		self.layout_master = QtWidgets.QVBoxLayout()
		self.layout_frames = QtWidgets.QHBoxLayout()
		self.layout_buttons = QtWidgets.QHBoxLayout()

		self.setLayout(self.layout_master)
		self.layout_master.addLayout(self.layout_frames)
		self.layout_master.addWidget(self.btn_append)
		self.layout_master.addLayout(self.layout_buttons)

		# self.layout_frames.addWidget(self.frame_label)
		self.layout_frames.addWidget(self.frame_str)
		self.layout_buttons.addWidget(self.btn_set)
		self.layout_buttons.addWidget(self.btn_cancel)

		self.setWindowTitle("FrameSetter")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

		#LineEdit Validation
		re = QtCore.QRegExp("[0-9 ]+")
		frame_str_validator = QtGui.QRegExpValidator(re)
		self.frame_str.setValidator(frame_str_validator)
		self.frame_str.editingFinished.connect(self.validate_str)

	def frame_append(self):
		"""Append current frame to string edit"""
		cur_frame = nuke.frame()
		cur_str_frames = self.frame_str.text()

		ls_frames = self.str_to_list(cur_str_frames)
		ls_frames.append(str(cur_frame))
		self.frame_str.setText(self.list_to_str(ls_frames))

		self.validate_str()

	def frames_set(self):
		"""convert and set frames to list and json file"""
		
		_cur_ls_frames = self.str_to_list(self.frame_str.text())
		
		with open(self.json_file, 'r') as f:
			_json_data = json.load(f) 
			_json_data[SHOT] = _cur_ls_frames

			with open(self.json_file, 'w') as fw:
				_out = json.dumps(_json_data, indent=2)
				fw.write(_out)
		
		LOG.info("Frames: %s saved to file" % _cur_ls_frames)
		self.close()
		
	def validate_str(self):
		"""validates str for only digit output
		return: (str) str with only digit and spaces
		"""

		str_cur = self.frame_str.text()
		LOG.debug("validating str '%s'" % str_cur)

		ls_frames = self.str_to_list(re.sub('\s+', ' ', str_cur))
		ls_frames = list(dict.fromkeys(ls_frames))

		self.frame_str.setText(self.list_to_str(ls_frames))
		self.frame_str.setToolTip("%s frames recorded\n%s" % (len(ls_frames), self.frame_str.text()))

	def str_to_list(self, str_in):
		"""convert str_ining to list
		@str_in: (str_in) input str_ining of frames saperated but spaces
		return: (list of int) list of frames in int
		"""

		char_div = ' '
		_ls =[]

		if self.frame_str.text() != '': 
			for f in str_in.split(char_div):
				if f != '': _ls.append(int(f))
		_ls.sort()
		LOG.debug("Str to List: %s" % _ls)

		return _ls

	def list_to_str(self, ls):
		"""convert list to str"""

		ls_str = [str(l) for l in sorted(ls)]
		str_out = (' '.join(ls_str)).strip()
		LOG.debug("list to str: %s" % str_out)

		return str_out 

	def run(self):
		"""main calling function"""

		ls_frames = []
		with open(self.json_file, 'r') as f:
			ls_frames = json.load(f)[SHOT]
		self.frame_str.setText(self.list_to_str(ls_frames))
		self.validate_str()

		self.show()




#-------------------------------------------------------------------------------
#-debug
#-------------------------------------------------------------------------------



ui_FrameSetter = FrameSetter(get_json_file(JSON_STR))

def debug():
	# subprocess.call('cls', shell=True)
	LOG.setLevel(logging.DEBUG)
	# FrameStepper(1)
	ui_FrameSetter.run()
