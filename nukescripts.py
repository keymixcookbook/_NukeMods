class Dialog(object):

    def __init__(self):
		pass


class panels:


class PythonPanel(Dialog):

    def show(self):
		pass

    def finishModalDialog(self, result):
		pass

    def showModal(self, defaultKnobText):
		pass

    def writeKnobs(self, flags):
		pass

    def accept(self):
		pass

    def addToPane(self, pane):
		pass

    def _makeOkCancelButton(self):
		pass

    def cancel(self):
		pass

    def ok(self):
		pass

    def __init__(self, title, id, scrollable):
		pass

    def showModalDialog(self, defaultKnobText):
		pass

    def knobChangedCallback(self, knob):
		pass

    def knobChanged(self, knob):
		pass

    def hide(self):
		pass

    def create(self):
		pass

    def addKnob(self, knob):
		pass

    def removeKnob(self, knob):
		pass

    def reject(self):
		pass

    def knobs(self):
		pass

    def addCallback(self):
		pass

    def readKnobs(self, s):
		pass

    def removeCallback(self):
		pass

    def setMinimumSize(self, x, y):
		pass


class ClassInfo(object):

    def __call__(self):
		pass

    def __new__(self, S):
		pass

    def __init__(self):
		pass


class CreateNodePresetsPanel(PythonPanel):

    def knobChanged(self, knob):
		pass

    def createPreset(self):
		pass

    def getPresetPath(self):
		pass

    def __init__(self, node):
		pass


class CreateToolsetsPanel(PythonPanel):

    def getPresetPath(self):
		pass

    def knobChanged(self, knob):
		pass

    def createPreset(self):
		pass

    def buildFolderList(self, fullPath, menuPath):
		pass

    def __init__(self):
		pass


class DialogState(object):

    def setKnob(self, knob, defaultValue):
		pass

    def get(self, knob, defaultValue):
		pass

    def getValue(self, id, defaultValue):
		pass

    def save(self, knob):
		pass

    def __init__(self):
		pass

    def saveValue(self, id, value):
		pass


class ExecuteDialog(PythonPanel):

    def run(self):
		pass

    def _addViewKnob(self):
		pass

    def _titleString(self):
		pass

    def _getDefaultViews(self):
		pass

    def _frameRangeFromViewer(self, viewer):
		pass

    def _addPreKnobs(self):
		pass

    def _setFrameRangeFromSource(self, source):
		pass

    def addToPane(self):
		pass

    def __init__(self, dialogState, groupContext, nodeSelection, exceptOnError):
		pass

    def knobChanged(self, knob):
		pass

    def _addPostKnobs(self):
		pass

    def _idString(self):
		pass

    def addKnob(self, knob):
		pass

    def _addTrailingKnobs(self):
		pass

    def _selectedViews(self):
		pass


class FlipbookApplication(object):

    def run(self, path, frameRanges, views, options):
		pass

    def name(self):
		pass

    def dialogKnobChanged(self, dialog, knob):
		pass

    def capabilities(self):
		pass

    def cacheDir(self):
		pass

    def runFromNode(self, nodeToFlipbook, frameRanges, views, options):
		pass

    def path(self):
		pass

    def getExtraOptions(self, flipbookDialog, nodeToFlipbook):
		pass

    def dialogKnobs(self, dialog):
		pass

    def __init__(self):
		pass


class FlipbookDialog(object):

    def _requireIntermediateNodeNew(self, nodeToTest):
		pass

    def run(self):
		pass

    def _addViewKnob(self):
		pass

    def _titleString(self):
		pass

    def _getDefaultViews(self):
		pass

    def _addPreKnobs(self):
		pass

    def _getIntermediateFileType(self):
		pass

    def fixedAudioFlipbookDialogPostKnobs(self):
		pass

    def __init__(self, dialogState, groupContext, node, takeNodeSettings):
		pass

    def _getOptions(self, nodeToFlipbook):
		pass

    def knobChanged(self, knob):
		pass

    def flipbookKnobs(self):
		pass

    def _deleteTemporaries(self):
		pass

    def _selectedFlipbook(self):
		pass

    def _lutFromViewer(self, viewerName):
		pass

    def _createIntermediateNode(self):
		pass

    def _getIntermediatePath(self):
		pass

    def _getAudio(self):
		pass

    def _idString(self):
		pass

    def _addTrailingKnobs(self):
		pass

    def _getLUT(self):
		pass

    def _setKnobAndStore(self, knob, val):
		pass

    def _isViewerSettingKnob(self, knob):
		pass


class FlipbookFactory(object):

    def isRegistered(self, flipbook):
		pass

    def getApplication(self, name):
		pass

    def register(self, flipbookApplication):
		pass

    def getNames(self):
		pass

    def __init__(self):
		pass


class FlipbookLUTPathRegistry(object):

    def registerLUTPathForFlipbook(self, flipbook, lut, path):
		pass

    def getLUTPathForFlipbook(self, flipbook, lut):
		pass

    def __init__(self):
		pass


class FrameRangePanel(PythonPanel):

    def __init__(self, initalStart, initialEnd):
		pass

    def showDialog(self):
		pass


class LinkToTrackPanel(PythonPanel):

    def knobChanged(self, knob):
		pass

    def _updatePointsEnabled(self):
		pass

    def _updateEverything(self):
		pass

    def addToPane(self):
		pass

    def _updateLinkableKnobInfo(self):
		pass

    def _updateExpression(self):
		pass

    def __init__(self, groupContext):
		pass


class MetaFunction(object):

    def __call__(self):
		pass

    def __new__(self, S, ):
		pass


class NukeProfiler(object):

    def endProfile(self):
		pass

    def indentString(self):
		pass

    def NodeProfile(self, nukeNode, maxEngineVal):
		pass

    def writeXMLInfo(self):
		pass

    def CloseTag(self, tagName):
		pass

    def WriteDictInner(self, dictToWrite):
		pass

    def addFrameProfileAndResetTimers(self):
		pass

    def setPathToFile(self, filename):
		pass

    def resetTimersAndStartProfile(self):
		pass

    def initProfileDesc(self):
		pass

    def writeProfileDesc(self):
		pass

    def __init__(self):
		pass

    def OpenTag(self, tagName, optionsDict, closeTag):
		pass


class PrecompOptions(object):

    def askUserForOptions(self):
		pass

    def __init__(self):
		pass


class PrecompOptionsDialog(PythonPanel):

    def __init__(self):
		pass


class PresetsDeletePanel(PythonPanel):

    def deletePreset(self):
		pass

    def knobChanged(self, knob):
		pass

    def __init__(self):
		pass


class PresetsLoadPanel(PythonPanel):

    def knobChanged(self, knob):
		pass

    def __init__(self):
		pass

    def loadPreset(self):
		pass


class Property(object):

    def __new__(self, S, ):
		pass

    def read(self):
		pass

    def write(self):
		pass

    def getter(self):
		pass

    def __call__(self):
		pass

    def __init__(self):
		pass

    def setter(self):
		pass


def PythonPanelKnobChanged(widget):
		pass


class RenderDialog(ExecuteDialog):

    def isBackgrounded(self):
		pass

    def knobChanged(self, knob):
		pass

    def _addPostKnobs(self):
		pass

    def isTimelineWrite(self):
		pass

    def _titleString(self):
		pass

    def _addPreKnobs(self):
		pass

    def _idString(self):
		pass

    def _getBackgroundLimits(self):
		pass

    def run(self):
		pass

    def __init__(self, dialogState, groupContext, nodeSelection, exceptOnError):
		pass


def SIGNAL():
		pass


def SLOT():
		pass


class ScriptEditor(object):

    def updateValue(self):
		pass

    def __init__(self, knob, parent):
		pass

    def printText(self):
		pass

    def storeTextOnKnob(self):
		pass

    def getText(self):
		pass


class ScriptEditorWidgetKnob(object):

    def makeUI(self):
		pass

    def __init__(self, knob):
		pass


class ScriptInputArea(QObject):

    def updateLineNumberArea(self, rect, dy):
		pass

    def runScript(self):
		pass

    def insertIndent(self, tc):
		pass

    def focusOutEvent(self, event):
		pass

    def completerHighlightChanged(self, highlighted):
		pass

    def highlightCurrentLine(self):
		pass

    def keyPressEvent(self, event):
		pass

    def completeTokenUnderCursor(self, token):
		pass

    def increaseIndentationSelected(self):
		pass

    def commentSelected(self):
		pass

    def highlightErrorLine(self):
		pass

    def ExtendSelectionToCompleteLines(self, tc):
		pass

    def setFontFromPrefs(self):
		pass

    def completionsForToken(self, token):
		pass

    def updateLineNumberAreaWidth(self):
		pass

    def getErrorLineFromTraceback(self, tracebackStr):
		pass

    def lineNumberAreaWidth(self):
		pass

    def decreaseIndentationSelected(self):
		pass

    def __init__(self, output, editor, parent):
		pass

    def getFontFromNukePrefs(self):
		pass

    def getFontFromHieroPrefs(self):
		pass

    def showEvent(self, event):
		pass

    def resizeEvent(self, event):
		pass

    def insertCompletion(self, completion):
		pass

    def lineNumberAreaPaintEvent(self, event):
		pass


class Signal(object):

    def __new__(self, S, ):
		pass

    def __getitem__(self, y):
		pass

    def __str__(self):
		pass

    def __call__(self):
		pass

    def __init__(self):
		pass


class Slot(object):

    def __call__(self):
		pass

    def __new__(self, S, ):
		pass

    def __init__(self):
		pass


class StringIO(StringIO):

    def isatty(self):
		pass

    def truncate(self, size):
		pass

    def read(self, n):
		pass

    def writelines(self, iterable):
		pass

    def readlines(self, sizehint):
		pass

    def next(self):
		pass

    def write(self, s):
		pass

    def __iter__(self):
		pass

    def tell(self):
		pass

    def flush(self):
		pass

    def close(self):
		pass

    def readline(self, length):
		pass

    def getvalue(self):
		pass

    def seek(self, pos, mode):
		pass

    def __init__(self, buf):
		pass


class TableDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
		pass


class Thread(_Verbose):

    def isAlive(self):
		pass

    def setName(self, name):
		pass

    def __bootstrap(self):
		pass

    def setDaemon(self, daemonic):
		pass

    def isDaemon(self):
		pass

    def exc_clear(self):
		pass

    def _set_daemon(self):
		pass

    def __init__(self, group, target, name, args, kwargs, verbose):
		pass

    def join(self, timeout):
		pass

    def start(self):
		pass

    def _reset_internal_locks(self):
		pass

    def getName(self):
		pass

    def exc_info(self):
		pass

    def _set_ident(self):
		pass

    def __delete(self):
		pass

    def run(self):
		pass

    def __repr__(self):
		pass

    def isAlive(self):
		pass

    def __bootstrap_inner(self):
		pass

    def __stop(self):
		pass


class UDIMErrorDialog(QDialog):

    def __init__(self, parent, error_msg, udim_label):
		pass


class UDIMFile(UDIMFile):

    def __init__(self, udim, uv, filename):
		pass


class UDIMOptionsDialog(QDialog):

    def cellChanged(self, row, column):
		pass

    def importUdimFiles(self):
		pass

    def updateTableWidget(self):
		pass

    def addUdimFile(self, udim_file):
		pass

    def __init__(self, parent, parsing_func, udim_label):
		pass


class UserPresetsDeletePanel(PythonPanel):

    def deletePreset(self):
		pass

    def knobChanged(self, knob):
		pass

    def __init__(self):
		pass


class UserPresetsLoadPanel(PythonPanel):

    def knobChanged(self, knob):
		pass

    def __init__(self):
		pass

    def loadPreset(self):
		pass


class VertexInfo(VertexInfo):

    def __init__(self, objnum, index, value, position):
		pass


class VertexSelection(VertexSelection):

    def scale(self, vector):
		pass

    def __iter__(self):
		pass

    def add(self, vertexInfo):
		pass

    def points(self):
		pass

    def inverseRotate(self, vector, order):
		pass

    def __init__(self):
		pass

    def indices(self):
		pass

    def translate(self, vector):
		pass

    def __len__(self):
		pass


class ViewerCaptureDialog(FlipbookDialog):

    def _getIntermediateFileType(self):
		pass

    def knobChanged(self, knob):
		pass

    def captureViewer(self):
		pass

    def _titleString(self):
		pass

    def _idString(self):
		pass

    def __init__(self, dialogState, groupContext, node):
		pass


class ViewerCaptureDialogThread(Thread):

    def run(self):
		pass

    def __init__(self, captureViewer):
		pass


class WidgetKnob(WidgetKnob):

    def makeUI(self):
		pass

    def __init__(self, widget):
		pass


def addDropDataCallback(callback):
		pass


def addSnapFunc(label, func):
		pass


def addToolsetsPanel():
		pass


def allNodes(node):
		pass


def allNodesWithGeoSelectKnob():
		pass


def allign_nodes(nodes, base):
		pass


def animation_loop():
		pass


def animation_move():
		pass


def animation_negate():
		pass


def animation_reverse():
		pass


def anySelectedPoint(selectionThreshold):
		pass


def anySelectedVertexInfo(selectionThreshold):
		pass


def autoBackdrop():
		pass


def autocrop(first, last, inc, layer):
		pass


def averageNormal(vertexSelection):
		pass


def bboxToTopLeft(height, roi):
		pass


def branch():
		pass


def buildPresetDeletePanel():
		pass


def buildPresetFileList(fullPath):
		pass


def buildPresetLoadPanel():
		pass


def buildPresetSavePanel(nodeName, node):
		pass


def buildUserPresetDeletePanel():
		pass


def buildUserPresetLoadPanel():
		pass


def cache_clear(args):
		pass


def cache_particles_panel(particleCacheNode):
		pass


def cache_report(args):
		pass


def calcAveragePosition(vertexSelection):
		pass


def calcBounds(vertexSelection):
		pass


def calcRotationVector(vertexSelection, norm):
		pass


def callSnapFunc(nodeToSnap):
		pass


def cameraProjectionMatrix(cameraNode):
		pass


def camera_down():
		pass


def camera_up():
		pass


def checkForEmptyToolsetDirectories(currPath):
		pass


def checkUdimValue(udim):
		pass


def clearAllCaches():
		pass


def clear_selection_recursive(group):
		pass


def color_nodes():
		pass


def compare_UDIMFile(a, b):
		pass


def connect_selected_to_viewer(inputIndex):
		pass


def copy_knobs(args):
		pass


def createCurveTool():
		pass


def createKronos():
		pass


def createNodePreset(node, name):
		pass


def createNodePresetsMenu():
		pass


def createOFlow():
		pass


def createPlanartracker():
		pass


def createPrmanRender():
		pass


def createToolsetMenuItems(m, rootPath, fullPath, delete, allToolsetsList, isLocal):
		pass


def createToolsetsMenu(toolbar):
		pass


def createUVTile():
		pass


def create_camera_here():
		pass


def create_curve():
		pass


def create_matrix():
		pass


def create_read(defaulttype):
		pass


def create_time_warp():
		pass


def create_viewsplitjoin():
		pass


def cut_paste_file():
		pass


def declone(node):
		pass


def deleteNodePreset(classname, presetName):
		pass


def deleteToolset(rootPath, fileName):
		pass


def deleteUserNodePreset(classname, presetName):
		pass


def dropData(mimeType, text):
		pass


def executeDeferred(call, args, kwargs):
		pass


def executeInMainThread(call, args, kwargs):
		pass


def executeInMainThreadWithResult(call, args, kwargs):
		pass


def execute_panel(_list, exceptOnError):
		pass


def export_nodes_as_script():
		pass


def extract():
		pass


def findNextName(name):
		pass


def findNextNodeName(name):
		pass


def flipbook(command, node, framesAndViews):
		pass


def getItemDirName(d, item):
		pass


def getLUTPath(flipbookAppliction, lut):
		pass


def getNukeUserFolder():
		pass


def getSelection(selectionThreshold):
		pass


def get_reads(method):
		pass


def get_script_data():
		pass


def getallnodeinfo():
		pass


def goofy_title():
		pass


def goto_frame():
		pass


def groupmake():
		pass


def import_boujou():
		pass


def import_script():
		pass


def infoviewer():
		pass


def isAbcFilename(filename):
		pass


def isAudioFilename(filename):
		pass


def isDeepFilename(filename):
		pass


def isGeoFilename(filename):
		pass


def load_all_plugins():
		pass


def makeScriptEditorKnob():
		pass


def nodeIsInside(node, backdropNode):
		pass


def node_copypaste():
		pass


def node_delete(popupOnError, evaluateAll):
		pass


def parseUdimFile(f):
		pass


def planeRotation(tri, norm):
		pass


def populatePresetsMenu(nodeName, className):
		pass


def populateToolsetsMenu(m, delete):
		pass


def precomp_copyToGroup(precomp):
		pass


def precomp_open(precomp):
		pass


def precomp_render(precomp):
		pass


def precomp_selected():
		pass


def print_callback_info(verbose, callbackTypes):
		pass


def processPresetFile(location):
		pass


def projectPoint(camera, point):
		pass


def projectPoints(camera, points):
		pass


def projectSelectedPoints(cameraName):
		pass


def refreshToolsetsMenu():
		pass


def register(flipbookApplication):
		pass


def registerLUTPath(flipbookApplication, lut, path):
		pass


def registerPanel(id, command):
		pass


def registerWidgetAsPanel(widget, name, id, create):
		pass

    class NukeTestWindow(QtGui.QWidget):

      def __init__(self, parent=None):
		pass

def remove_inputs():
		pass

def render_panel(_list, exceptOnError):
		pass

def replaceHashes(filename):
		pass

def restorePanel(id):
		pass

def rotateToPointsVerified(nodeToSnap, vertexSelection):
		pass

def saveNodePresets():
		pass

def scaleToPointsVerified(nodeToScale, vertexSelection):
		pass

def script_and_write_nodes_version_up():
		pass

def script_command(default_cmd):
		pass

def script_data():
		pass

def script_directory():
		pass

def script_version_up():
		pass

def search_replace():
		pass

def select_by_name():
		pass

def select_similar(_type):
		pass

def selectedPoints(selectionThreshold):
		pass

def selectedVertexInfos(selectionThreshold):
		pass

def setFlipbookDefaultOption(name, value):
		pass

def setRenderDialogDefaultOption(name, value):
		pass

def setup_toolbars():
		pass

def showExecuteDialog(nodesToExecute, exceptOnError):
		pass

def showFlipbookDialog(node, takeNodeSettings):
		pass

def showFlipbookDialogForSelected():
		pass

def showRenderDialog(nodesToRender, exceptOnError):
		pass

def showViewerCaptureDialog(node):
		pass

def showname():
		pass

def splitInSequence(f):
		pass

def start(url):
		pass

def swapAB(n):
		pass

def toggle(knob):
		pass

def toggle_monitor_output():
		pass

def toolbar_sticky_note():
		pass

def trackerlinkingdialog(groupContext):
		pass

def trackerlinkingdialogexpressionx():
		pass

def trackerlinkingdialogexpressiony():
		pass

def translateRotateScaleSelectionToPoints(nodeToSnap, vertexSelection):
		pass

def translateRotateScaleThisNodeToPoints():
		pass

def translateRotateScaleToPoints(nodeToSnap):
		pass

def translateRotateScaleToPointsVerified(nodeToSnap, vertexSelection):
		pass

def translateRotateSelectionToPoints(nodeToSnap, vertexSelection):
		pass

def translateRotateThisNodeToPoints():
		pass

def translateRotateToPoints(nodeToSnap):
		pass

def translateRotateToPointsVerified(nodeToSnap, vertexSelection):
		pass

def translateSelectionToPoints(nodeToSnap, vertexSelection):
		pass

def translateThisNodeToPoints():
		pass

def translateToPoints(nodeToSnap):
		pass

def translateToPointsVerified(nodeToSnap, vertexSelection):
		pass

def transpose(m):
		pass

def traversePluginPaths(m, delete, allToolsetsList, isLocal):
		pass

def udimStr(s, label):
		pass

def udim_group(nodes):
		pass

def udim_import(udim_parsing_func, udim_column_label):
		pass

def unregisterPanel(id, command):
		pass

def update_plugin_menu(menuname):
		pass

def uv2udim(uv):
		pass

def verifyNodeOrder(node, knobName, orderName):
		pass

def verifyNodeToSnap(nodeToSnap, knobList):
		pass

def verifyVertexSelection(vertexSelection, minLen):
		pass

def version_down():
		pass

def version_get(string, prefix, suffix):
		pass

def version_latest():
		pass

def version_set(string, prefix, oldintval, newintval):
		pass

def version_up():
		pass

