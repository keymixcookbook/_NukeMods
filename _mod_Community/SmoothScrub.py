# Max van Leeuwen - maxvanleeuwen.com
#
# SmoothScrub 1.0
# Temporarily play at 0 fps to make scrubbing on already cached frames a lot smoother. Weird performance hack.




import nuke



# store which pyside is used
scr_pySide2 = True

# get pyside
try:
	from PySide2 import QtCore
	from PySide2 import QtWidgets as q
	from PySide2 import QtGui
	
except:
	scr_pySide2 = False
	from PySide import QtCore
	from PySide import QtGui as q
	




################
# global scope variables to store information inbetween user input events (always available in session)
################


# text to add to window title
scr_titleAppendText = ' (SmoothScrub enabled)'

# smooth scrubbing enabled
scr_enabled = False

# scrubbing speed multiplier
scr_scrubSpeed = 0.0

# use smooth scrubbing (playing at 0fps)
scr_useSmooth = True

# screen width in pixels
scr_scrWidth = -1

# frame range length to scrub through (last - first, mapped to screen width)
scr_rangeLength = -1

# original frame rate to return to later
scr_frameRate = -1

# current scrubbing mode (0: Smooth Scrubbing, 1: Forward Playing, 2: Backward Playing)
scr_scrubMode = 0

# active viewer
scr_activeViewer = None



# class storage
scr_inputCatcherEventClass = None
scr_mouseTrackerEventClass = None

# is mouse hijacked to click/drag anywhere on the screen
scr_timelineScrubOnly = False

# is mouse pressed or released when moving
scr_mouseDown = False

# playing mode when mouse was pressed down (to reset on mouse release)
scr_playingModeDown = 0

# placeholders for last mouse position x and last frame while scrubbing
scr_lastPos = 0
scr_lastFrame = 0

# bool to determine if mouse is in viewer panel now
scr_mouseInWidget = True

# store this viewer panel and its title
scr_viewerWidget = None
scr_viewerTitle = ''



################




# main function(toggles on/off)
def SmoothScrub(useSmooth=True, timelineScrubOnly=False, scrubSpeed=1.0, key=''):

	global scr_enabled
	global scr_scrubSpeed
	global scr_useSmooth
	global scr_rangeLength
	global scr_frameRate
	global scr_scrubMode
	global scr_activeViewer
	global scr_inputCatcherEventClass
	global scr_mouseTrackerEventClass
	global scr_timelineScrubOnly
	global scr_viewerWidget
	global scr_viewerTitle




	# if user pressed one of these keys during scrubbing, start playing on normal frame rate but keep scrubbing enabled
	if(key == 'j'):

		# cancel if already playing backward (do not cancel if function called from mouse release)
		if(scr_scrubMode == 2 and not scr_playingModeDown == 2):

			scr_scrubMode = 0

			if scr_useSmooth:
				scr_activeViewer.node()['fps'].setValue(0)

			scr_activeViewer.stop()

			if scr_useSmooth:
				scr_activeViewer.play(1)

		else:

			# play backward with normal frame rate
			scr_scrubMode = 2

			if scr_useSmooth:
				scr_activeViewer.node()['fps'].setValue(scr_frameRate)
			
			scr_activeViewer.stop()
			scr_activeViewer.play(0)


	elif(key == 'k'):

		# reset to default SmoothScrub mode
		scr_scrubMode = 0

		if scr_useSmooth:
			scr_activeViewer.node()['fps'].setValue(0)
		
		scr_activeViewer.stop()
		
		if scr_useSmooth:
			scr_activeViewer.play(1)


	elif(key == 'l'):

		# cancel if already playing forward (do not cancel if function called from mouse release)
		if(scr_scrubMode == 1 and not scr_playingModeDown == 1):

			scr_scrubMode = 0

			if scr_useSmooth:
				scr_activeViewer.node()['fps'].setValue(0)
			
			scr_activeViewer.stop()
			
			if scr_useSmooth:
				scr_activeViewer.play(1)
				scr_activeViewer.play(1)


		else:

			# play forward with normal frame rate
			scr_scrubMode = 1

			if scr_useSmooth:
				scr_activeViewer.node()['fps'].setValue(scr_frameRate)
			
			scr_activeViewer.stop()
			scr_activeViewer.play(1)
			
			# if start playing and not resume playing, it needs another 'start' for some reason
			if not scr_playingModeDown == 1:
				scr_activeViewer.play(1)



	# if no input
	else:

		# toggle off if already on
		if(scr_enabled):

			# disable
			scr_enabled = False


			if(scr_useSmooth):

				# set fps to original value and stop playing
				scr_activeViewer.node()['fps'].setValue(scr_frameRate)
				scr_activeViewer.stop()


			# clear class
			scr_inputCatcherEventClass = None
			scr_mouseTrackerEventClass = None

			# reset window titles for all widgets
			for widget in q.QApplication.instance().allWidgets():
				thisTitle = widget.windowTitle()
				if scr_titleAppendText in thisTitle:
					widget.setWindowTitle(thisTitle.replace(scr_titleAppendText, ''))


			scr_viewerWidget.setWindowTitle(scr_viewerTitle)
			scr_viewerWidget = None
			scr_viewerTitle = ''


			
		# toggle on if off
		else:

			# enable
			scr_enabled = True

			# set smooth scrub
			scr_useSmooth = useSmooth

			# reset scrub mode
			scr_scrubMode = 0


			# get scrubbing speed (if 1, the mouse left-right in nuke window width aligns with the frame range start-end)
			scr_scrubSpeed = scrubSpeed

			# get active viewer
			scr_activeViewer = nuke.activeViewer()

			# get original frame rate from active viewer window
			if(scr_useSmooth):
				scr_frameRate = scr_activeViewer.node()['fps'].getValue()

			# get range
			readRange = str(scr_activeViewer.node().playbackRange()).split('-')
			scr_rangeLength = int(readRange[1]) - int(readRange[0])


			if(scr_useSmooth):

				# set frame rate to 0, and 'play' on this frame (has to be set manually to avoid going back to first_frame when at last_frame)
				getFrame = nuke.frame()
				scr_activeViewer.node()['fps'].setValue(0)
				scr_activeViewer.stop()
				scr_activeViewer.play(1)
				nuke.frame(getFrame)


			# only listen to user input for clicking anywhere to drag if PySide2 is loaded (newer versions of Nuke) - otherwise use timeline scrub mode only
			scr_timelineScrubOnly = timelineScrubOnly if scr_pySide2 else True


			# start class with event filter (listens to keyboard/mouse inputs)
			scr_inputCatcherEventClass = InputCatcher()
			scr_mouseTrackerEventClass = MouseTracker()
			



# class that picks up mouse events
class MouseTracker(QtCore.QObject):

	def __init__(self):

		global scr_viewerWidget
		global scr_viewerTitle
		global scr_scrWidth


		super(MouseTracker, self).__init__()



		# get application
		app = q.QApplication

		# placeholder for final widget
		w = None


		# if mouse is on top of a viewer right now, pick that as the widget
		pos = QtGui.QCursor.pos() if scr_pySide2 else q.QCursor.pos()
		widget = app.widgetAt(pos)

		# check if widget was found
		if not widget == 0:

			w = widget

			# get screen width
			scr_scrWidth = widget.frameGeometry().width()



		# get active viewer title
		activeTitle = scr_activeViewer.node().name()

		# go through all widgets to change titles
		for widget in app.instance().allWidgets():

			# get current widget title
			scr_viewerTitle = widget.windowTitle()

			# if this is the right widget (title is same and widget is not hidden)
			if scr_viewerTitle.startswith(activeTitle):

				# change title
				widget.setWindowTitle(scr_viewerTitle + scr_titleAppendText)

				# if no widget was found yet
				if (w is None) and (not widget.isHidden()):

					# store first found match as active widget
					w = widget

				
		
		# store widget and set new title
		scr_viewerWidget = w
		
		# install filter
		scr_viewerWidget.installEventFilter(self)




	# event filter for viewer panel	
	def eventFilter(self, widget, event):

		# is mouse enters or leaves, update bool
		if event.type() == QtCore.QEvent.Enter:
			setMousePosition(True)

		elif event.type() == QtCore.QEvent.Leave:
			setMousePosition(False)


		# always let everything through this filter
		return False




# class that picks up mouse events
class InputCatcher(QtCore.QObject):

	def __init__(self):

		super(InputCatcher, self).__init__()

		# install filter on whole application for mouse takeover
		app = q.QApplication.instance()
		app.installEventFilter(self)



	# event filter for full application
	def eventFilter(self, widget, event):

		# on left press
		if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.MouseButton.LeftButton and scr_mouseInWidget:
			
			if not scr_timelineScrubOnly:
				setMouseDown(True, event.pos().toTuple(), scr_scrWidth)
				return True

			else:
				return False

		# on left release
		elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.MouseButton.LeftButton and scr_mouseDown:
			
			if not scr_timelineScrubOnly:
				setMouseDown(False)
				return True

			else:
				return False

		# on move left mouse button
		elif event.type() == QtCore.QEvent.MouseMove and scr_mouseDown:
			
			if not scr_timelineScrubOnly:
				onMousePos(event.pos().toTuple())
				return True

			else:
				return False



		# catch keyboard key input overrides
		elif event.type() == QtCore.QEvent.ShortcutOverride and scr_mouseInWidget:

			# if user wants to play forward
			if event.key() == QtCore.Qt.Key_L:

				# only return key if in PySide2
				keyReturned('l' if scr_pySide2 else '')
				return True

			# these keys are not filtered when True is returned - so do not filter and instead stop SmoothScrub when user uses arrow keys to go through frames
			elif event.key() == QtCore.Qt.Key_Right or event.key() == QtCore.Qt.Key_Left:

				keyReturned()
				return False


			else:
				return False



		# any other keyboard input
		elif event.type() == QtCore.QEvent.KeyPress and scr_mouseInWidget:

			# on esc
			if event.key() == QtCore.Qt.Key_Escape:

				keyReturned()
				return True

			# if user wants to play backward
			elif event.key() == QtCore.Qt.Key_J:

				# only return key if in PySide2
				keyReturned('j' if scr_pySide2 else '')
				return True

			# if user wants to stop playing forwards/backwards and return to scrubbing
			elif event.key() == QtCore.Qt.Key_K:

				# only return key if in PySide2
				keyReturned('k' if scr_pySide2 else '')
				return True


			# if other key
			else:
				return False
		

		# if not in this filter
		else:
			return False




# when keyboard key pressed
def keyReturned(keyPressed=''):

	# call the main function again
	SmoothScrub(key=keyPressed)




# update current mouse press/release status
def setMouseDown(t, pos=0, width=-1):

	global scr_mouseDown
	global scr_playingModeDown
	global scr_scrubMode

	scr_mouseDown = t


	# if mouse down
	if t:

		global scr_lastPos
		global scr_lastFrame

		scr_lastPos = pos[0]
		scr_lastFrame = nuke.frame()


		# if was playing in a direction
		if not scr_scrubMode == 0:

			scr_playingModeDown = scr_scrubMode

			# reset to default SmoothScrub mode, stop playing forwards/backwards and play 'stationary' instead
			scr_scrubMode = 0
			
			if scr_useSmooth:
				scr_activeViewer.node()['fps'].setValue(0)
			
			scr_activeViewer.stop()
			
			if scr_useSmooth:
				scr_activeViewer.play(1)

	# if mouse release, reset scrub mode
	else:

		scr_scrubMode = scr_playingModeDown

		# resume playing in original direction
		if(scr_scrubMode == 1):
			keyReturned('l')
		elif(scr_scrubMode == 2):
			keyReturned('j')

		scr_playingModeDown = 0




def setMousePosition(m):

	global scr_mouseInWidget
	scr_mouseInWidget = m




# function that handles mouse position data
def onMousePos(pos):

	# set new frame if mouse is pressed
	if(scr_mouseDown):

		# get frame relative to screen width
		newFrameNorm = (pos[0] - scr_lastPos) / float(scr_scrWidth) * scr_scrubSpeed
		newFrame = newFrameNorm * scr_rangeLength + scr_lastFrame

		# set frame
		nuke.frame(newFrame)




# autostart (if not imported) - do timeline scrub mode only, no mouse takeover (because viewer panel might not be active)
if __name__ == "__main__":
	SmoothScrub(timelineScrubOnly=True)