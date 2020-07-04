
class Dialog(object):
    def __init__(self):
        pass

class panels:
    pass

class PythonPanel(Dialog):
    def show(self):
        """None"""
        pass

    def finishModalDialog(self, result):
        """None"""
        pass

    def showModal(self, defaultKnobText):
        """None"""
        pass

    def writeKnobs(self, flags):
        """None"""
        pass

    def accept(self):
        """None"""
        pass

    def addToPane(self, pane):
        """None"""
        pass

    def _makeOkCancelButton(self):
        """None"""
        pass

    def cancel(self):
        """None"""
        pass

    def ok(self):
        """None"""
        pass

    def __init__(self, title, id, scrollable):
        """None"""
        pass

    def showModalDialog(self, defaultKnobText):
        """None"""
        pass

    def knobChangedCallback(self, knob):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def hide(self):
        """None"""
        pass

    def create(self):
        """None"""
        pass

    def addKnob(self, knob):
        """None"""
        pass

    def removeKnob(self, knob):
        """None"""
        pass

    def reject(self):
        """None"""
        pass

    def knobs(self):
        """None"""
        pass

    def addCallback(self):
        """None"""
        pass

    def readKnobs(self, s):
        """None"""
        pass

    def removeCallback(self):
        """None"""
        pass

    def setMinimumSize(self, x, y):
        """None"""
        pass

class ClassInfo(object):
    def __call__(self):
        """x.__call__(...) <==> x(...)"""
        pass

    def __new__(self, S):
        """T.__new__(S, ...) -> a new object with type S, a subtype of T"""
        pass

    def __init__(self):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        pass


class CreateNodePresetsPanel(PythonPanel):
    def knobChanged(self, knob):
        """None"""
        pass

    def createPreset(self):
        """None"""
        pass

    def getPresetPath(self):
        """None"""
        pass

    def __init__(self, node):
        """None"""
        pass


class CreateToolsetsPanel(PythonPanel):
    def getPresetPath(self):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def createPreset(self):
        """None"""
        pass

    def buildFolderList(self, fullPath, menuPath):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass


class DialogState(object):
    def setKnob(self, knob, defaultValue):
        """Convenience method for setting a value straight on a knob."""
        pass

    def get(self, knob, defaultValue):
        """Return the given knob's stored last state value.
    If none exists, defaultValue is returned.
    Values are stored in a dict referenced by knob name, so names must be unique!"""
        pass

    def getValue(self, id, defaultValue):
        """Recalls the value. If it was not set before, it will return the defaultValue."""
        pass

    def save(self, knob):
        """Store the knob's current value as the 'last state' for the next time the dialog is opened.
    Values are stored in a dict referenced by knob name, so names must be unique!"""
        pass

    def __init__(self):
        """None"""
        pass

    def saveValue(self, id, value):
        """Stores the value with the given id."""
        pass


class ExecuteDialog(PythonPanel):
    def run(self):
        """None"""
        pass

    def _addViewKnob(self):
        """Add knobs for view selection."""
        pass

    def _titleString(self):
        """None"""
        pass

    def _getDefaultViews(self):
        """None"""
        pass

    def _frameRangeFromViewer(self, viewer):
        """"Set the framerange knob to have the framerange from the given viewer."""
        pass

    def _addPreKnobs(self):
        """Add knobs that must appear before the render knobs."""
        pass

    def _setFrameRangeFromSource(self, source):
        """None"""
        pass

    def addToPane(self):
        """None"""
        pass

    def __init__(self, dialogState, groupContext, nodeSelection, exceptOnError):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def _addPostKnobs(self):
        """Add knobs that must appear after the render knobs."""
        pass

    def _idString(self):
        """None"""
        pass

    def addKnob(self, knob):
        """Add the knob and make sure it cannot be animated."""
        pass

    def _addTrailingKnobs(self):
        """Add knobs that must appear at the very end."""
        pass

    def _selectedViews(self):
        """None"""
        pass


class FlipbookApplication(object):
    def run(self, path, frameRanges, views, options):
        """Execute the flipbook on a path.
       @param path: The path to run the flipbook on. This will be similar to /path/to/foo%03d.exr
       @param frameRanges: A FrameRanges object representing the range that should be flipbooked. Note that in 6.2v1-2 this was a FrameRange object.
       @param views: A list of strings comprising of the views to flipbook. Willnot be more than the maximum supported by the flipbook.
       @param options: A dictionary of options to use. This may contain the keys pixelAspect, roi, dimensions, audio and lut. These contain a float, a dict with bounding box dimensions, a dict with width and height, a path to audio file and a string indicating the LUT conversion to apply.
       @return: None"""
        pass

    def name(self):
        """ Return the name of the flipbook.
       @return: String"""
        pass

    def dialogKnobChanged(self, dialog, knob):
        """Called whenever this flipbook is selected and one of the knobs added in dialogKnobs was changed.
       @param dialog: The FlipbookDialog that contains the knob
       @param knob: The knob added in dialogKnobs that was modified.
       @return: None"""
        pass

    def capabilities(self):
        """Return the capabilities of the flipbook application. Currently used are:
       proxyScale: bool, whether the flipbook supports proxies
       crop: bool, whether the flipbook supports crops
       canPreLaunch: bool, whether the flipbook can display a frames that are still being rendered by Nuke.
       maximumViews: int, the number of views supported by this flipbook, should be 1 or higher.
       fileTypes: list, the extensions of the file types supported by this format. Must all be lowercase, e.g ["exr", "jpg", ...]
       @return: dict with the capabilities above."""
        pass

    def cacheDir(self):
        """Return the preferred directory for rendering.
       @return: String"""
        pass

    def runFromNode(self, nodeToFlipbook, frameRanges, views, options):
        """Execute the flipbook on a node.
       This method will use the node's filename to call run()
       @param node: The node to run the flipbook
       @param frameRanges: A FrameRanges object representing the range that should be flipbooked. Note that in 6.2v1-2 this was a FrameRange object.
       @param views: A list of strings comprising of the views to flipbook. Willnot be more than the maximum supported by the flipbook.
       @param options: A dictionary of options to use. This may contain the keys pixelAspect, roi, dimensions, audio and lut. These contain a float, a dict with bounding box dimensions, a dict with width and height, a path to audio file and a string indicating the LUT conversion to apply.
       @return: None"""
        pass

    def path(self):
        """Return the executable path required to run a flipbook.
       @return: String"""
        pass

    def getExtraOptions(self, flipbookDialog, nodeToFlipbook):
        """Called whenever this flipbook is selected to retrieve extra options from the node selected to flipbook
        and the flipbook dialog.
        @param flipbookDialog: the flipbook dialog
        @param nodeToFlipbook: node selected to flipbook
        @return: a dictionary with the extra options """
        pass

    def dialogKnobs(self, dialog):
        """This is called when the user has selected this flipbook application, and will be interested in any knobs that you might have to show for custom settings.
       @param dialog: The FlipbookDialog that has requested the knobs to be added to it, e.g. dialog.addKnob(...)
       @return: None"""
        pass

    def __init__(self):
        """None"""
        pass


class FlipbookDialog(object):
    def _requireIntermediateNodeNew(self, nodeToTest):
        """None"""
        pass

    def run(self):
        """None"""
        pass

    def _addViewKnob(self):
        """None"""
        pass

    def _titleString(self):
        """None"""
        pass

    def _getDefaultViews(self):
        """None"""
        pass

    def _addPreKnobs(self):
        """None"""
        pass

    def _getIntermediateFileType(self):
        """None"""
        pass

    def fixedAudioFlipbookDialogPostKnobs(self):
        """None"""
        pass

    def __init__(self, dialogState, groupContext, node, takeNodeSettings):
        """None"""
        pass

    def _getOptions(self, nodeToFlipbook):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def flipbookKnobs(self):
        """None"""
        pass

    def _deleteTemporaries(self):
        """Delete all the files in the range to be rendered."""
        pass

    def _selectedFlipbook(self):
        """None"""
        pass

    def _lutFromViewer(self, viewerName):
        """None"""
        pass

    def _createIntermediateNode(self):
        """Create a write node to render out the current node so that output may be used for flipbooking."""
        pass

    def _getIntermediatePath(self):
        """Get the path for the temporary files. May be filled in using printf syntax."""
        pass

    def _getAudio(self):
        """None"""
        pass

    def _idString(self):
        """None"""
        pass

    def _addTrailingKnobs(self):
        """None"""
        pass

    def _getLUT(self):
        """None"""
        pass

    def _setKnobAndStore(self, knob, val):
        """None"""
        pass

    def _isViewerSettingKnob(self, knob):
        """None"""
        pass


class FlipbookFactory(object):
    def isRegistered(self, flipbook):
        """ Return whether a flipbook app with that name has already been registered.
    @param flipbook: FlipBookApplication object that's tested for.
    @return: bool"""
        pass

    def getApplication(self, name):
        """Returns the flipbook app implementation with the given name, raises an exception if none could be found.
    @param name: The name of a flipbook that was registered.
    @return: FlipBookApplication"""
        pass

    def register(self, flipbookApplication):
        """Register a flipbook app. It will fail if the flipbook app name isn't unique.
    @param flipbook: FlipBookApplication object to register
    @return: None"""
        pass

    def getNames(self):
        """Returns a list of the names of all available flipbook apps.
    @return: list"""
        pass

    def __init__(self):
        """None"""
        pass


class FlipbookLUTPathRegistry(object):
    def registerLUTPathForFlipbook(self, flipbook, lut, path):
        """Register the given LUT file.
       @param flipbook: The unique name of the flipbook
       @param lut: The unique name for the LUT, e.g. 'sRGB' and 'rec709'
       @param path: Location of the flipbook specific file."""
        pass

    def getLUTPathForFlipbook(self, flipbook, lut):
        """Return the path for the given flipbook and lut. May return an empty string if none registered.
       @param flipbook: The unique name of the flipbook
       @param lut: The unique name for the LUT, e.g. 'sRGB' and 'rec709'"""
        pass

    def __init__(self):
        """None"""
        pass


class FrameRangePanel(PythonPanel):
    def __init__(self, initalStart, initialEnd):
        """Constructor that takes 2 arguments for the initial start and end frame numbers"""
        pass

    def showDialog(self):
        """show panel dialog, returns if accept was pressed"""
        pass



class LinkToTrackPanel(PythonPanel):
    def knobChanged(self, knob):
        """None"""
        pass

    def _updatePointsEnabled(self):
        """Enable the track point bools when linking to position; disable otherwise."""
        pass

    def _updateEverything(self):
        """None"""
        pass

    def addToPane(self):
        """None"""
        pass

    def _updateLinkableKnobInfo(self):
        """None"""
        pass

    def _updateExpression(self):
        """Update the expression to reflect the current settings."""
        pass

    def __init__(self, groupContext):
        """None"""
        pass


class MetaFunction(object):
    def __call__(self):
        """x.__call__(...) <==> x(...)"""
        pass

    def __new__(self, S, ):
        """T.__new__(S, ...) -> a new object with type S, a subtype of T"""
        pass


class NukeProfiler(object):
    def endProfile(self):
        """None"""
        pass

    def indentString(self):
        """None"""
        pass

    def NodeProfile(self, nukeNode, maxEngineVal):
        """None"""
        pass

    def writeXMLInfo(self):
        """None"""
        pass

    def CloseTag(self, tagName):
        """None"""
        pass

    def WriteDictInner(self, dictToWrite):
        """None"""
        pass

    def addFrameProfileAndResetTimers(self):
        """None"""
        pass

    def setPathToFile(self, filename):
        """None"""
        pass

    def resetTimersAndStartProfile(self):
        """None"""
        pass

    def initProfileDesc(self):
        """None"""
        pass

    def writeProfileDesc(self):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass

    def OpenTag(self, tagName, optionsDict, closeTag):
        """None"""
        pass


class PrecompOptions(object):
    def askUserForOptions(self):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass


class PrecompOptionsDialog(PythonPanel):
    def __init__(self):
        """None"""
        pass


class PresetsDeletePanel(PythonPanel):
    def deletePreset(self):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass


class PresetsLoadPanel(PythonPanel):
    def knobChanged(self, knob):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass

    def loadPreset(self):
        """None"""
        pass


class Property(object):
    def __new__(self, S, ):
        """T.__new__(S, ...) -> a new object with type S, a subtype of T"""
        pass

    def read(self):
        """None"""
        pass

    def write(self):
        """None"""
        pass

    def getter(self):
        """None"""
        pass

    def __call__(self):
        """x.__call__(...) <==> x(...)"""
        pass

    def __init__(self):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        pass

    def setter(self):
        """None"""
        pass


def PythonPanelKnobChanged(widget):
    """None"""
    pass


class RenderDialog(ExecuteDialog):
    def isBackgrounded(self):
        """Return whether the background rendering option is enabled."""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def _addPostKnobs(self):
        """None"""
        pass

    def isTimelineWrite(self):
        """None"""
        pass

    def _titleString(self):
        """None"""
        pass

    def _addPreKnobs(self):
        """None"""
        pass

    def _idString(self):
        """None"""
        pass

    def _getBackgroundLimits(self):
        """None"""
        pass

    def run(self):
        """None"""
        pass

    def __init__(self, dialogState, groupContext, nodeSelection, exceptOnError):
        """None"""
        pass


def SIGNAL():
    """None"""
    pass


def SLOT():
    """None"""
    pass


class ScriptEditor(object):
    def updateValue(self):
        """None"""
        pass

    def __init__(self, knob, parent):
        """None"""
        pass

    def printText(self):
        """None"""
        pass

    def storeTextOnKnob(self):
        """None"""
        pass

    def getText(self):
        """None"""
        pass


class ScriptEditorWidgetKnob(object):
    def makeUI(self):
        """None"""
        pass

    def __init__(self, knob):
        """None"""
        pass


class ScriptInputArea(QObject):
    def updateLineNumberArea(self, rect, dy):
        """None"""
        pass

    def runScript(self):
        """None"""
        pass

    def insertIndent(self, tc):
        """None"""
        pass

    def focusOutEvent(self, event):
        """None"""
        pass

    def completerHighlightChanged(self, highlighted):
        """None"""
        pass

    def highlightCurrentLine(self):
        """None"""
        pass

    def keyPressEvent(self, event):
        """None"""
        pass

    def completeTokenUnderCursor(self, token):
        """None"""
        pass

    def increaseIndentationSelected(self):
        """None"""
        pass

    def commentSelected(self):
        """None"""
        pass

    def highlightErrorLine(self):
        """None"""
        pass

    def ExtendSelectionToCompleteLines(self, tc):
        """None"""
        pass

    def setFontFromPrefs(self):
        """None"""
        pass

    def completionsForToken(self, token):
        """None"""
        pass

    def updateLineNumberAreaWidth(self):
        """None"""
        pass

    def getErrorLineFromTraceback(self, tracebackStr):
        """None"""
        pass

    def lineNumberAreaWidth(self):
        """None"""
        pass

    def decreaseIndentationSelected(self):
        """None"""
        pass

    def __init__(self, output, editor, parent):
        """None"""
        pass

    def getFontFromNukePrefs(self):
        """None"""
        pass

    def getFontFromHieroPrefs(self):
        """None"""
        pass

    def showEvent(self, event):
        """None"""
        pass

    def resizeEvent(self, event):
        """None"""
        pass

    def insertCompletion(self, completion):
        """None"""
        pass

    def lineNumberAreaPaintEvent(self, event):
        """None"""
        pass


class Signal(object):
    def __new__(self, S, ):
        """T.__new__(S, ...) -> a new object with type S, a subtype of T"""
        pass

    def __getitem__(self, y):
        """x.__getitem__(y) <==> x[y]"""
        pass

    def __str__(self):
        """x.__str__() <==> str(x)"""
        pass

    def __call__(self):
        """x.__call__(...) <==> x(...)"""
        pass

    def __init__(self):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        pass


class Slot(object):
    def __call__(self):
        """x.__call__(...) <==> x(...)"""
        pass

    def __new__(self, S, ):
        """T.__new__(S, ...) -> a new object with type S, a subtype of T"""
        pass

    def __init__(self):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        pass


class StringIO(StringIO):
    def isatty(self):
        """Returns False because StringIO objects are not connected to a
        tty-like device.
        """
        pass

    def truncate(self, size):
        """Truncate the file's size.

        If the optional size argument is present, the file is truncated to
        (at most) that size. The size defaults to the current position.
        The current file position is not changed unless the position
        is beyond the new file size.

        If the specified size exceeds the file's current size, the
        file remains unchanged.
        """
        pass

    def read(self, n):
        """Read at most size bytes from the file
        (less if the read hits EOF before obtaining size bytes).

        If the size argument is negative or omitted, read all data until EOF
        is reached. The bytes are returned as a string object. An empty
        string is returned when EOF is encountered immediately.
        """
        pass

    def writelines(self, iterable):
        """Write a sequence of strings to the file. The sequence can be any
        iterable object producing strings, typically a list of strings. There
        is no return value.

        (The name is intended to match readlines(); writelines() does not add
        line separators.)
        """
        pass

    def readlines(self, sizehint):
        """Read until EOF using readline() and return a list containing the
        lines thus read.

        If the optional sizehint argument is present, instead of reading up
        to EOF, whole lines totalling approximately sizehint bytes (or more
        to accommodate a final whole line).
        """
        pass

    def next(self):
        """A file object is its own iterator, for example iter(f) returns f
        (unless f is closed). When a file is used as an iterator, typically
        in a for loop (for example, for line in f: print line), the next()
        method is called repeatedly. This method returns the next input line,
        or raises StopIteration when EOF is hit.
        """
        pass

    def write(self, s):
        """Write a string to the file.

        There is no return value.
        """
        pass

    def __iter__(self):
        """None"""
        pass

    def tell(self):
        """Return the file's current position."""
        pass

    def flush(self):
        """Flush the internal buffer
        """
        pass

    def close(self):
        """Free the memory buffer.
        """
        pass

    def readline(self, length):
        """Read one entire line from the file.

        A trailing newline character is kept in the string (but may be absent
        when a file ends with an incomplete line). If the size argument is
        present and non-negative, it is a maximum byte count (including the
        trailing newline) and an incomplete line may be returned.

        An empty string is returned only when EOF is encountered immediately.

        Note: Unlike stdio's fgets(), the returned string contains null
        characters ('\0') if they occurred in the input.
        """
        pass

    def getvalue(self):
        """
        Retrieve the entire contents of the "file" at any time before
        the StringIO object's close() method is called.

        The StringIO object can accept either Unicode or 8-bit strings,
        but mixing the two may take some care. If both are used, 8-bit
        strings that cannot be interpreted as 7-bit ASCII (that use the
        8th bit) will cause a UnicodeError to be raised when getvalue()
        is called.
        """
        pass

    def seek(self, pos, mode):
        """Set the file's current position.

        The mode argument is optional and defaults to 0 (absolute file
        positioning); other values are 1 (seek relative to the current
        position) and 2 (seek relative to the file's end).

        There is no return value.
        """
        pass

    def __init__(self, buf):
        """None"""
        pass


class TableDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        """None"""
        pass


class Thread(_Verbose):
    def isAlive(self):
        """None"""
        pass

    def setName(self, name):
        """None"""
        pass

    def __bootstrap(self):
        """None"""
        pass

    def setDaemon(self, daemonic):
        """None"""
        pass

    def isDaemon(self):
        """None"""
        pass

    def exc_clear(self):
        """exc_clear() -> None

Clear global information on the current exception.  Subsequent calls to
exc_info() will return (None,None,None) until another exception is raised
in the current thread or the execution stack returns to a frame where
another exception is being handled."""
        pass

    def _set_daemon(self):
        """None"""
        pass

    def __init__(self, group, target, name, args, kwargs, verbose):
        """None"""
        pass

    def join(self, timeout):
        """None"""
        pass

    def start(self):
        """None"""
        pass

    def _reset_internal_locks(self):
        """None"""
        pass

    def getName(self):
        """None"""
        pass

    def exc_info(self):
        """exc_info() -> (type, value, traceback)

Return information about the most recent exception caught by an except
clause in the current stack frame or in an older stack frame."""
        pass

    def _set_ident(self):
        """None"""
        pass

    def __delete(self):
        """Remove current thread from the dict of currently running threads."""
        pass

    def run(self):
        """None"""
        pass

    def __repr__(self):
        """None"""
        pass

    def isAlive(self):
        """None"""
        pass

    def __bootstrap_inner(self):
        """None"""
        pass

    def __stop(self):
        """None"""
        pass


class UDIMErrorDialog(QDialog):
    def __init__(self, parent, error_msg, udim_label):
        """None"""
        pass


class UDIMFile(UDIMFile):
    def __init__(self, udim, uv, filename):
        """None"""
        pass


class UDIMOptionsDialog(QDialog):
    def cellChanged(self, row, column):
        """None"""
        pass

    def importUdimFiles(self):
        """None"""
        pass

    def updateTableWidget(self):
        """None"""
        pass

    def addUdimFile(self, udim_file):
        """None"""
        pass

    def __init__(self, parent, parsing_func, udim_label):
        """None"""
        pass


class UserPresetsDeletePanel(PythonPanel):
    def deletePreset(self):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass


class UserPresetsLoadPanel(PythonPanel):
    def knobChanged(self, knob):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass

    def loadPreset(self):
        """None"""
        pass


class VertexInfo(VertexInfo):
    def __init__(self, objnum, index, value, position):
        """None"""
        pass


class VertexSelection(VertexSelection):
    def scale(self, vector):
        """None"""
        pass

    def __iter__(self):
        """None"""
        pass

    def add(self, vertexInfo):
        """None"""
        pass

    def points(self):
        """None"""
        pass

    def inverseRotate(self, vector, order):
        """None"""
        pass

    def __init__(self):
        """None"""
        pass

    def indices(self):
        """None"""
        pass

    def translate(self, vector):
        """None"""
        pass

    def __len__(self):
        """None"""
        pass


class ViewerCaptureDialog(FlipbookDialog):
    def _getIntermediateFileType(self):
        """None"""
        pass

    def knobChanged(self, knob):
        """None"""
        pass

    def captureViewer(self):
        """ Return an instance of a CaptureViewer class, which when executed captures the viewer.
    """
        pass

    def _titleString(self):
        """None"""
        pass

    def _idString(self):
        """None"""
        pass

    def __init__(self, dialogState, groupContext, node):
        """None"""
        pass


class ViewerCaptureDialogThread(Thread):
    def run(self):
        """None"""
        pass

    def __init__(self, captureViewer):
        """None"""
        pass


class WidgetKnob(WidgetKnob):
    def makeUI(self):
        """None"""
        pass

    def __init__(self, widget):
        """None"""
        pass


def addDropDataCallback(callback):
    """Add a function to the list of callbacks. This function will called whenever data is dropped onto the DAG. Override it to perform other actions.
  If you handle the drop, return True, otherwise return None."""
    pass


def addSnapFunc(label, func):
    """
  addSnapFunc(label, func) -> None
  Add a new snapping function to the list.

  The label parameter is the text that will appear in (eg.) an Enumeration_Knob
  for the function. It cannot be the same as any existing snap function label
  (if it is, the function will abort without changing anything).

  The func parameter is the snapping function. It must be a callable object
  taking a single parameter: the node to perform the snapping on.
  """
    pass


def addToolsetsPanel():
    """None"""
    pass


def allNodes(node):
    """
  allNodes() -> iterator
  Return an iterator which yields all nodes in the current script.

  This includes nodes inside groups. They will be returned in top-down,
  depth-first order.
  """
    pass


def allNodesWithGeoSelectKnob():
    """None"""
    pass


def allign_nodes(nodes, base):
    """None"""
    pass


def animation_loop():
    """None"""
    pass


def animation_move():
    """None"""
    pass


def animation_negate():
    """None"""
    pass


def animation_reverse():
    """None"""
    pass


def anySelectedPoint(selectionThreshold):
    """
  anySelectedPoint(selectionThreshold) -> _nukemath.Vector3
  Return a selected point from the active viewer or the first viewer with a selection.
  The selectionThreshold parameter is used when working with a soft selection.
  Only points with a selection level >= the selection threshold will be returned by this function.
  """
    pass


def anySelectedVertexInfo(selectionThreshold):
    """
  anySelectedVertexInfo(selectionThreshold) -> VertexInfo

  Returns a single VertexInfo for a selected point. If more than one point is
  selected, one of them will be chosen arbitrarily.

  The selectionThreshold parameter is used when working with a soft selection.
  Only points with a selection level >= the selection threshold will be
  returned by this function.
  """
    pass


def autoBackdrop():
    """
  Automatically puts a backdrop behind the selected nodes.

  The backdrop will be just big enough to fit all the select nodes in, with room
  at the top for some text in a large font.
  """
    pass


def autocrop(first, last, inc, layer):
    """Run the CurveTool's AutoCrop function on each selected node over the
  specified frame range and channels. If the range values are None, the
  project first_frame and last_frame are used; if inc is None, 1 is used.
  After execution, the CurveTool AutoCrop results are copied into a Crop
  node attached to each selected node."""
    pass


def averageNormal(vertexSelection):
    """
  averageNormal(selectionThreshold -> _nukemath.Vector3
  Return a _nukemath.Vector3 which is the average of the normals of all selected points
  """
    pass


def bboxToTopLeft(height, roi):
    """Convert the roi passed from a origin at the bottom left to the top left.
     Also replaces the r and t keys with w and h keys.
     @param height: the height used to determine the top.
     @param roi: the roi with a bottom left origin, must have x, y, r & t keys.
     @result dict with x, y, w & h keys"""
    pass


def branch():
    """None"""
    pass


def buildPresetDeletePanel():
    """None"""
    pass


def buildPresetFileList(fullPath):
    """None"""
    pass


def buildPresetLoadPanel():
    """None"""
    pass


def buildPresetSavePanel(nodeName, node):
    """None"""
    pass


def buildUserPresetDeletePanel():
    """None"""
    pass


def buildUserPresetLoadPanel():
    """None"""
    pass


def cache_clear(args):
    """
  Clears the buffer memory cache by calling nuke.memory("free")
  If args are supplied they are passed to nuke.memory as well
  eg. nuke.memory( "free", args )
  """
    pass


def cache_particles_panel(particleCacheNode):
    """None"""
    pass


def cache_report(args):
    """
  Gets info on memory by calling nuke.memory("info")
  If args are supplied they are passed to nuke.memory as well
  eg. nuke.memory( "info", args )
  """
    pass


def calcAveragePosition(vertexSelection):
    """
  Calculate the average position of all points.

  @param points: An iterable sequence of _nukemath.Vector3 objects.
  @return: A _nukemath.Vector3 containing the average of all the points.
  """
    pass


def calcBounds(vertexSelection):
    """None"""
    pass


def calcRotationVector(vertexSelection, norm):
    """None"""
    pass


def callSnapFunc(nodeToSnap):
    """
  callSnapFunc(nodeToSnap) -> None
  Call the snapping function on a node.

  The nodeToSnap parameter is optional. If it's not specified, or is None, we
  use the result of nuke.thisNode() instead.

  The node must have an Enumeration_Knob called "snapFunc" which selects the
  snapping function to call.
  """
    pass


def cameraProjectionMatrix(cameraNode):
    """Calculate the projection matrix for the camera based on its knob values."""
    pass


def camera_down():
    """All new camera_down that uses the version_get/set functions.
  This script takes the render camera up one in selected iread/writes.
  Camera may be _c# or _p# for previs camera number"""
    pass


def camera_up():
    """All new camera_up that uses the version_get/set functions.
  This script takes the render camera up one in selected iread/writes.
  Camera may be _c# or _p# for previs camera number"""
    pass


def checkForEmptyToolsetDirectories(currPath):
    """None"""
    pass


def checkUdimValue(udim):
    """None"""
    pass


def clearAllCaches():
    """
  Clears all caches. The disk cache, viewer playback cache and memory buffers.
  """
    pass


def clear_selection_recursive(group):
    """Sets all nodes to unselected, including in child groups."""
    pass


def color_nodes():
    """Set all selected nodes to be the same colour as the first selected node."""
    pass


def compare_UDIMFile(a, b):
    """None"""
    pass


def connect_selected_to_viewer(inputIndex):
    """Connects the selected node to the given viewer input index, ignoring errors if no node is selected."""
    pass


def copy_knobs(args):
    """None"""
    pass


def createCurveTool():
    """None"""
    pass


def createKronos():
    """None"""
    pass


def createNodePreset(node, name):
    """None"""
    pass


def createNodePresetsMenu():
    """None"""
    pass


def createOFlow():
    """None"""
    pass


def createPlanartracker():
    """None"""
    pass


def createPrmanRender():
    """None"""
    pass


def createToolsetMenuItems(m, rootPath, fullPath, delete, allToolsetsList, isLocal):
    """None"""
    pass


def createToolsetsMenu(toolbar):
    """None"""
    pass


def createUVTile():
    """None"""
    pass


def create_camera_here():
    """None"""
    pass


def create_curve():
    """None"""
    pass


def create_matrix():
    """None"""
    pass


def create_read(defaulttype):
    """Create a Read node for a file selected from the file browser.
  If a node is currently selected in the nodegraph and it has a 'file'
  (or failing that a 'proxy') knob, the value (if any) will be used as the default
  path for the file browser."""
    pass


def create_time_warp():
    """None"""
    pass


def create_viewsplitjoin():
    """None"""
    pass


def cut_paste_file():
    """None"""
    pass


def declone(node):
    """None"""
    pass


def deleteNodePreset(classname, presetName):
    """None"""
    pass


def deleteToolset(rootPath, fileName):
    """None"""
    pass


def deleteUserNodePreset(classname, presetName):
    """None"""
    pass


def dropData(mimeType, text):
    """Handle data drops by invoking the list of callback functions until one has
     handled the event"""
    pass


def executeDeferred(call, args, kwargs):
    """None"""
    pass


def executeInMainThread(call, args, kwargs):
    """ Execute the callable 'call' with optional arguments 'args' and named arguments 'kwargs' i
n Nuke's main thread and return immediately. """
    pass


def executeInMainThreadWithResult(call, args, kwargs):
    """ Execute the callable 'call' with optional arguments 'args' and named arguments 'kwargs' in
      Nuke's main thread and wait for the result to become available. """
    pass


def execute_panel(_list, exceptOnError):
    """None"""
    pass


def export_nodes_as_script():
    """None"""
    pass


def extract():
    """Disconnect all arrows between selected and unselected nodes, and move selected nodes to the right.
  This function is maintained only for compatibility.  Please use nuke.extractSelected() instead."""
    pass


def findNextName(name):
    """None"""
    pass


def findNextNodeName(name):
    """None"""
    pass


def flipbook(command, node, framesAndViews):
    """Runs an arbitrary command on the images output by a node. This checks
  to see if the node is a Read or Write and calls the function directly
  otherwise it creates a temporary Write, executes it, and then calls
  the command on that temporary Write, then deletes it.

  By writing your own function you can use this to launch your own
  flipbook or video-output programs.

  Specify framesAndViews as a tuple if desired, like so: ("1,5", ["main"])
  This can be useful when running without a GUI."""
    pass


def getItemDirName(d, item):
    """None"""
    pass


def getLUTPath(flipbookAppliction, lut):
    """Returns a path to a LUT file for the given flipbook. The contents of the file will be different for each flipbook application. Please see the relevant documentation for the specific flipbook applications.
   @param flipbook: The unique name of the flipbook
   @param lut: The unique name for the LUT, e.g. 'sRGB' and 'rec709'"""
    pass


def getNukeUserFolder():
    """None"""
    pass


def getSelection(selectionThreshold):
    """None"""
    pass


def get_reads(method):
    """Returns file names from all Read nodes.

  Options:
    file - outputs only file names
    dir  - outputs only directory names
    long - outputs the entire path"""
    pass


def get_script_data():
    """None"""
    pass


def getallnodeinfo():
    """None"""
    pass


def goofy_title():
    """Returns a random message for use as an untitled script name.
  Can be assigned to nuke.untitled as a callable.
  Put a goofy_title.txt somewhere in your NUKE_PATH to customise."""
    pass


def goto_frame():
    """None"""
    pass


def groupmake():
    """Builds a group from the current node selection.
  This function is only maintained for backwards compatibility.
  Please use nuke.makeGroup() instead."""
    pass


def import_boujou():
    """None"""
    pass


def import_script():
    """None"""
    pass


def infoviewer():
    """None"""
    pass


def isAbcFilename(filename):
    """None"""
    pass


def isAudioFilename(filename):
    """None"""
    pass


def isDeepFilename(filename):
    """None"""
    pass


def isGeoFilename(filename):
    """None"""
    pass


def load_all_plugins():
    """None"""
    pass


def makeScriptEditorKnob():
    """None"""
    pass


def nodeIsInside(node, backdropNode):
    """Returns true if node geometry is inside backdropNode otherwise returns false"""
    pass


def node_copypaste():
    """None"""
    pass


def node_delete(popupOnError, evaluateAll):
    """None"""
    pass


def parseUdimFile(f):
    """Parsing a filename string in search of the udim number.
     The function returns the udim number, and None if it is not able to decode the udim value.

     The udim value is a unique number that defines the tile coordinate.
     If u,v are the real tile coordinates the equivalent udim number is calculated with the following formula:
     udim = 1001 + u + 10 * v    (Note: u >=0 && u < 10 && udim > 1000 && udim < 2000)

     Redefine this function if the parsing function is not appropriate with your filename syntax."""
    pass


def planeRotation(tri, norm):
    """
  Calculate the rotations around the X, Y and Z axes that will align a plane
  perpendicular to the Z axis with the given triangle.

  @param tri: A list or tuple of 3 _nukemath.Vector3 objects. The 3 points must
   describe the plane (i.e. they must not be collinear).
  @return: A _nukemath.Vector3 object where the x coordinate is the angle of
   rotation around the x axis and so on.
  @raise ValueError: if the three points are collinear.
  """
    pass


def populatePresetsMenu(nodeName, className):
    """None"""
    pass


def populateToolsetsMenu(m, delete):
    """None"""
    pass


def precomp_copyToGroup(precomp):
    """None"""
    pass


def precomp_open(precomp):
    """None"""
    pass


def precomp_render(precomp):
    """None"""
    pass


def precomp_selected():
    """None"""
    pass


def print_callback_info(verbose, callbackTypes):
    """
  Returns a list of all currently active callbacks, with the following optional
  arguments:
      verbose = False      : prints the documentation as well as the callback
      callbackTypes = None : limit the callback info to a particular callback
                             type (e.g. ['OnCreates'])
  """
    pass


def processPresetFile(location):
    """None"""
    pass


def projectPoint(camera, point):
    """
  projectPoint(camera, point) -> nuke.math.Vector2

  Project the given 3D point through the camera to get 2D pixel coordinates.

  @param camera: The Camera node or name of the Camera node to use for projecting
                 the point.
  @param point: A nuke.math.Vector3 or of list/tuple of three float values
                representing the 3D point.
  @raise ValueError: If camera or point is invalid.
  """
    pass


def projectPoints(camera, points):
    """
  projectPoint(camera, points) -> list of nuke.math.Vector2

  Project the given 3D point through the camera to get 2D pixel coordinates.

  @param camera: The Camera node or name of the Camera node to use for projecting
                 the point.
  @param points: A list or tuple of either nuke.math.Vector3 or of list/tuples of
                 three float values representing the 3D points.
  @raise ValueError: If camera or point is invalid.
  """
    pass


def projectSelectedPoints(cameraName):
    """
  projectSelectedPoints(cameraName='Camera1') -> iterator yielding nuke.math.Vector2

  Using the specified camera, project all of the selected points into 2D pixel
  coordinates and return their locations.

  @param cameraName: Optional name of the Camera node to use for projecting the
                     points. If omitted, will look for a node called Camera1.
  """
    pass


def refreshToolsetsMenu():
    """None"""
    pass


def register(flipbookApplication):
    """Register a flipbook. Convenience function that simple calls register() on the FlipbookFactory."""
    pass


def registerLUTPath(flipbookApplication, lut, path):
    """Register a LUT for a specific flipbook. The path should refer to a file that contains the LUT for the given flipbook identified by the name in flipbookApplication. It is up to the flipbook subimplementation to actually use this file and the format may vary.
   @param flipbook: The unique name of the flipbook
   @param lut: The unique name for the LUT, e.g. 'sRGB' and 'rec709'
   @param path: Location of the flipbook specific file."""
    pass


def registerPanel(id, command):
    """None"""
    pass


def registerWidgetAsPanel(widget, name, id, create):
    """registerWidgetAsPanel(widget, name, id, create) -> PythonPanel

    Wraps and registers a widget to be used in a Nuke panel.

    widget - should be a string of the class for the widget
    name - is is the name as it will appear on the Pane menu
    id - should the the unique ID for this widget panel
    create - if this is set to true a new NukePanel will be returned that wraps this widget

    Example ( using PyQt )

    import nuke
    import PyQt4.QtCore as QtCore
    import PyQt4.QtGui as QtGui
    from nukescripts import panels

    class NukeTestWindow(QtGui.QWidget):
      def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout( QtGui.QVBoxLayout() )
        self.myTable	= QtGui.QTableWidget( )
        self.myTable.header = ['Date', 'Files', 'Size', 'Path' ]
        self.myTable.size = [ 75, 375, 85, 600 ]
        self.layout().addWidget( self.myTable )

    nukescripts.registerWidgetAsPanel('NukeTestWindow', 'NukeTestWindow', 'uk.co.thefoundry.NukeTestWindow' )

  """
    pass


def remove_inputs():
    """None"""
    pass


def render_panel(_list, exceptOnError):
    """None"""
    pass


def replaceHashes(filename):
    """replaceHashes(filename) -> string
  Replace any sequences of 1 or more hash marks (#) with a printf-style %0nd specifier."""
    pass


def restorePanel(id):
    """None"""
    pass


def rotateToPointsVerified(nodeToSnap, vertexSelection):
    """None"""
    pass


def saveNodePresets():
    """None"""
    pass


def scaleToPointsVerified(nodeToScale, vertexSelection):
    """None"""
    pass


def script_and_write_nodes_version_up():
    """ Increments the versioning in the script name and the path of the timeline write nodes, then saves the new version. """
    pass


def script_command(default_cmd):
    """None"""
    pass


def script_data():
    """None"""
    pass


def script_directory():
    """None"""
    pass


def script_version_up():
    """Adds 1 to the _v## at the end of the script name and saves a new version."""
    pass


def search_replace():
    """ Search/Replace in Reads and Writes. """
    pass


def select_by_name():
    """Menu command to select nodes by a glob-pattern name.
  This function is only maintained for backwards compatibility.
  Please use nuke.selectPattern() instead."""
    pass


def select_similar(_type):
    """Included only for compatibility.  Use nuke.selectSimilar()."""
    pass


def selectedPoints(selectionThreshold):
    """
  selectedPoints(selectionThreshold) -> iterator

  Return an iterator which yields the position of every point currently
  selected in the Viewer in turn.

  The selectionThreshold parameter is used when working with a soft selection.
  Only points with a selection level >= the selection threshold will be
  returned by this function.
  """
    pass


def selectedVertexInfos(selectionThreshold):
    """
  selectedVertexInfos(selectionThreshold) -> iterator

  Return an iterator which yields a tuple of the index and position of each
  point currently selected in the Viewer in turn.

  The selectionThreshold parameter is used when working with a soft selection.
  Only points with a selection level >= the selection threshold will be
  returned by this function.
  """
    pass


def setFlipbookDefaultOption(name, value):
    """ Set a particular option to the given value. The type of the value differs per option, giving the wrong value may result in exceptions. The options are read every time the dialog is opened, though not every knob in the dialog has it's value stored."""
    pass


def setRenderDialogDefaultOption(name, value):
    """ Set a particular option to the given value. The type of the value differs per option, giving the wrong value may result in exceptions. The options are read every time the dialog is opened, though not every knob in the dialog has it's value stored."""
    pass


def setup_toolbars():
    """None"""
    pass


def showExecuteDialog(nodesToExecute, exceptOnError):
    """Present a dialog that executes the given list of nodes."""
    pass


def showFlipbookDialog(node, takeNodeSettings):
    """Present a dialog that flipbooks the given node."""
    pass


def showFlipbookDialogForSelected():
    """Present a dialog that flipbooks the currently selected node."""
    pass


def showRenderDialog(nodesToRender, exceptOnError):
    """Present a dialog that renders the given list of nodes."""
    pass


def showViewerCaptureDialog(node):
    """None"""
    pass


def showname():
    """Shows the current script path and, if the selected node is a Read or Write node, the filename from it."""
    pass


def splitInSequence(f):
    """None"""
    pass


def start(url):
    """Open a URL or file."""
    pass


def swapAB(n):
    """Swaps the first two inputs of a node."""
    pass


def toggle(knob):
    """ "Inverts" some flags on the selected nodes.

  What this really does is set all of them to the same value, by finding the
  majority value and using the inverse of that."""
    pass


def toggle_monitor_output():
    """Toggles monitor output (switches it on if it's off, or vice versa) for the currently active viewer."""
    pass


def toolbar_sticky_note():
    """None"""
    pass


def trackerlinkingdialog(groupContext):
    """None"""
    pass


def trackerlinkingdialogexpressionx():
    """None"""
    pass


def trackerlinkingdialogexpressiony():
    """None"""
    pass


def translateRotateScaleSelectionToPoints(nodeToSnap, vertexSelection):
    """None"""
    pass


def translateRotateScaleThisNodeToPoints():
    """None"""
    pass


def translateRotateScaleToPoints(nodeToSnap):
    """
  Translate the specified node to the average position of the current vertex selection in the active viewer,
  rotate to the orientation of the (mean squares) best fit plane for the selection
  and scale to the extents of the selection.
  The nodeToSnap must contain 'translate', 'rotate' and 'scale' knobs, the transform order must be 'SRT' and
  the rotation order must be 'ZXY'.

  @type nodeToSnap:   nuke.Node
  @param nodeToSnap:  Node to translate, rotate and scale
  """
    pass


def translateRotateScaleToPointsVerified(nodeToSnap, vertexSelection):
    """None"""
    pass


def translateRotateSelectionToPoints(nodeToSnap, vertexSelection):
    """None"""
    pass


def translateRotateThisNodeToPoints():
    """None"""
    pass


def translateRotateToPoints(nodeToSnap):
    """
  Translate the specified node to the average position of the current vertex selection in the active viewer
  and rotate to the orientation of the (mean squares) best fit plane for the selection.
  The nodeToSnap must contain 'translate' and 'rotate' knobs, the transform order must be 'SRT' and the
  rotation order must be 'ZXY'.

  @type nodeToSnap:   nuke.Node
  @param nodeToSnap:  Node to translate and rotate
  """
    pass


def translateRotateToPointsVerified(nodeToSnap, vertexSelection):
    """None"""
    pass


def translateSelectionToPoints(nodeToSnap, vertexSelection):
    """None"""
    pass


def translateThisNodeToPoints():
    """None"""
    pass


def translateToPoints(nodeToSnap):
    """
  Translate the specified node to the average position of the current vertex selection in the active viewer.
  The nodeToSnap must contain a 'translate' knob and the transform order must be 'SRT'.

  @type nodeToSnap:   nuke.Node
  @param nodeToSnap:  Node to translate
  """
    pass


def translateToPointsVerified(nodeToSnap, vertexSelection):
    """None"""
    pass


def transpose(m):
    """None"""
    pass


def traversePluginPaths(m, delete, allToolsetsList, isLocal):
    """None"""
    pass


def udimStr(s, label):
    """None"""
    pass


def udim_group(nodes):
    """None"""
    pass


def udim_import(udim_parsing_func, udim_column_label):
    """ Imports a sequence of UDIM files and creates the node material tree needed.
      This function simplifies the process of importing textures. It generates a tree of nodes which
      adjusts the texture coordinates at rendering time for a model containing multiple texture tiles.
      In general a tile texture coordinate can be expressed with a single value(UDIM) or with a tuple(ST or UV).
      The udim_import function can decode a UDIM number from a filename.
      To determine the tile coordinate encoding for a generic filename convention, the udim_import script can use an
      external parsing function.

      The redefined parsing function needs to decode a filename string and return the udim or the u,v tile coordinate
      as an integer or tuple of integers. It should return None if the tile coordinate id can not be determined.

  @param udim_parsing_func:   The parsing function. This parses a filename string and returns a tile id.
  @param udim_column_label:   The name of the column in the dialog box used to show the tile id.
  @return:                    None
  """
    pass


def unregisterPanel(id, command):
    """None"""
    pass


def update_plugin_menu(menuname):
    """None"""
    pass


def uv2udim(uv):
    """None"""
    pass


def verifyNodeOrder(node, knobName, orderName):
    """None"""
    pass


def verifyNodeToSnap(nodeToSnap, knobList):
    """None"""
    pass


def verifyVertexSelection(vertexSelection, minLen):
    """None"""
    pass


def version_down():
    """All new version_down that uses the version_get/set functions.
  This script takes the render version up one in selected iread/writes."""
    pass


def version_get(string, prefix, suffix):
    """Extract version information from filenames used by DD (and Weta, apparently)
  These are _v# or /v# or .v# where v is a prefix string, in our case
  we use "v" for render version and "c" for camera track version.
  See the version.py and camera.py plugins for usage."""
    pass


def version_latest():
    """Like version_up, but only goes up to the highest numbered version
  that exists.

  Works on all selected Read nodes, or all Read nodes if nothing is
  selected.

  Does not modify Write nodes."""
    pass


def version_set(string, prefix, oldintval, newintval):
    """Changes version information from filenames used by DD (and Weta, apparently)
  These are _v# or /v# or .v# where v is a prefix string, in our case
  we use "v" for render version and "c" for camera track version.
  See the version.py and camera.py plugins for usage."""
    pass


def version_up():
    """All new version_up that uses the version_get/set functions.
  This script takes the render version up one in selected iread/writes."""
    pass
