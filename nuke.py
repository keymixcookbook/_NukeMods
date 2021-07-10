class AColor_Knob(Color_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class AnimationCurve(object):

	def fixSlopes(self):
		pass

	def constant(self):
		pass

	def removeKey(self, keys):
		pass

	def size(self):
		pass

	def knobIndex(self):
		pass

	def inverse(self, y):
		pass

	def __new__(self, S, ):
		pass

	def selected(self):
		pass

	def setKey(self):
		pass

	def addKey(self, keys):
		pass

	def changeInterpolation(self):
		pass

	def toScript(self, selected):
		pass

	def knob(self):
		pass

	def keys(self):
		pass

	def evaluate(self, t):
		pass

	def integrate(self):
		pass

	def derivative(self):
		pass

	def setExpression(self, s):
		pass

	def identity(self):
		pass

	def clear(self):
		pass

	def fromScript(self, s):
		pass

	def knobAndFieldName(self):
		pass

	def noExpression(self):
		pass

	def expression(self):
		pass

	def view(self):
		pass


class AnimationKey(object):

	def __init__(self):
		pass

	def __new__(self, S, ):
		pass


class Array_Knob(Knob):

	def clearAnimated(self):
		pass

	def removeKey(self):
		pass

	def setValueAt(self):
		pass

	def frame(self):
		pass

	def removeKeyAt(self):
		pass

	def height(self):
		pass

	def minimum(self):
		pass

	def unsplitView(self, view):
		pass

	def array(self):
		pass

	def getIntegral(self):
		pass

	def singleValue(self, view):
		pass

	def isKeyAt(self):
		pass

	def hasExpression(self, index):
		pass

	def __new__(self, S, ):
		pass

	def setKeyAt(self):
		pass

	def min(self):
		pass

	def defaultValue(self):
		pass

	def getKeyTime(self):
		pass

	def deleteAnimation(self, curve):
		pass

	def width(self):
		pass

	def getNumKeys(self):
		pass

	def valueAt(self):
		pass

	def arraySize(self):
		pass

	def max(self):
		pass

	def setSingleValue(self):
		pass

	def toScript(self):
		pass

	def notDefault(self):
		pass

	def splitView(self, view):
		pass

	def setValue(self):
		pass

	def isAnimated(self):
		pass

	def copyAnimations(self):
		pass

	def setDefaultValue(self, s):
		pass

	def dimensions(self):
		pass

	def vect(self):
		pass

	def animations(self, view):
		pass

	def setAnimated(self):
		pass

	def getDerivative(self):
		pass

	def setExpression(self):
		pass

	def animation(self):
		pass

	def resize(self):
		pass

	def setRange(self):
		pass

	def getValueAt(self):
		pass

	def getNthDerivative(self):
		pass

	def isKey(self):
		pass

	def fromScript(self, s):
		pass

	def maximum(self):
		pass

	def value(self):
		pass

	def getValue(self):
		pass

	def getKeyIndex(self):
		pass

	def copyAnimation(self):
		pass


class Axis_Knob(Knob):

	def uniformScale(self):
		pass

	def rotate(self):
		pass

	def __new__(self, S, ):
		pass

	def skew(self):
		pass

	def value(self):
		pass

	def scale(self):
		pass

	def pivot(self):
		pass

	def translate(self):
		pass

	def __init__(self):
		pass


class BBox_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def setT(self):
		pass

	def fromDict(self, box):
		pass

	def r(self):
		pass

	def names(self):
		pass

	def setR(self):
		pass

	def toDict(self):
		pass

	def y(self):
		pass

	def x(self):
		pass

	def setX(self):
		pass

	def setY(self):
		pass

	def __init__(self):
		pass

	def t(self):
		pass


class BackdropNode(Node):

	def __getitem__(self, y):
		pass

	def __str__(self):
		pass

	def selectNodes(self):
		pass

	def getNodes(self):
		pass

	def __repr__(self):
		pass

	def __len__(self):
		pass


class BeginTabGroup_Knob(Knob):

	def __new__(self, S, ):
		pass


class Bitmask_Knob(Enumeration_Knob):

	def __new__(self, S, ):
		pass


class Boolean_Knob(Array_Knob):

	def value(self):
		pass

	def setValue(self, b):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Box(object):

	def set(self):
		pass

	def move(self):
		pass

	def isConstant(self):
		pass

	def clampY(self, y):
		pass

	def clampX(self, x):
		pass

	def __init__(self):
		pass

	def __new__(self, S, ):
		pass

	def pad(self):
		pass

	def centerX(self):
		pass

	def centerY(self):
		pass

	def intersect(self):
		pass

	def setH(self, n):
		pass

	def setT(self, n):
		pass

	def setW(self, n):
		pass

	def setR(self, n):
		pass

	def setX(self, n):
		pass

	def setY(self, n):
		pass

	def h(self):
		pass

	def clear(self):
		pass

	def merge(self):
		pass

	def r(self):
		pass

	def t(self):
		pass

	def w(self):
		pass

	def y(self):
		pass

	def x(self):
		pass


class Box3_Knob(Array_Knob):

	def setF(self, far):
		pass

	def __new__(self, S, ):
		pass

	def f(self, ar):
		pass

	def setN(self, near):
		pass

	def value(self):
		pass

	def n(self, ear):
		pass

	def setT(self, top):
		pass

	def r(self, ight):
		pass

	def names(self):
		pass

	def setR(self, right):
		pass

	def y(self):
		pass

	def x(self):
		pass

	def setX(self):
		pass

	def setY(self):
		pass

	def __init__(self):
		pass

	def t(self, op):
		pass


class CancelledError(Exception):
	pass

class CascadingEnumeration_Knob(Enumeration_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class ChannelMask_Knob(Channel_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Channel_Knob(Knob):

	def inputNumber(self):
		pass

	def __new__(self, S, ):
		pass

	def enableChannel(self):
		pass

	def layerSelector(self):
		pass

	def setEnable(self, name):
		pass

	def value(self):
		pass

	def checkMarks(self):
		pass

	def channelSelector(self):
		pass

	def depth(self):
		pass

	def setValue(self, name):
		pass

	def setInput(self, num):
		pass

	def inputKnob(self):
		pass

	def isChannelEnabled(self, name):
		pass

	def __init__(self):
		pass


class ColorChip_Knob(Unsigned_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Color_Knob(Array_Knob):

	def inputNumber(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass

	def names(self, n):
		pass


class ColorspaceLookupError(Exception):
	pass

class Disable_Knob(Boolean_Knob):

	def value(self):
		pass

	def setValue(self, b):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Double_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class EditableEnumeration_Knob(Enumeration_Knob):

	def setValue(self, item):
		pass

	def __new__(self, S, ):
		pass

	def numValues(self):
		pass

	def value(self):
		pass

	def enumName(self, n):
		pass

	def values(self):
		pass

	def setValues(self, items):
		pass

	def __init__(self):
		pass


class EndTabGroup_Knob(Knob):

	def __new__(self, S, ):
		pass


class Enumeration_Knob(Unsigned_Knob):

	def setValue(self, item):
		pass

	def __new__(self, S, ):
		pass

	def numValues(self):
		pass

	def value(self):
		pass

	def enumName(self, n):
		pass

	def values(self):
		pass

	def setValues(self, items):
		pass

	def __init__(self):
		pass


class EvalString_Knob(String_Knob):

	def evaluate(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Eyedropper_Knob(AColor_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class File_Knob(EvalString_Knob):

	def fromUserText(self, s):
		pass

	def setValue(self, s):
		pass

	def __new__(self, S, ):
		pass

	def fromScript(self, s):
		pass

	def value(self):
		pass

	def getValue(self):
		pass

	def getEvaluatedValue(self, oc):
		pass

	def __init__(self):
		pass


class FnPySingleton(object):

	def __new__(self, type):
		pass


class Font_Knob(Knob):

	def value(self):
		pass

	def setValue(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Format(object):

	def setPixelAspect(self, aspectRatio):
		pass

	def height(self):
		pass

	def scaled(self):
		pass

	def setWidth(self, newWidth):
		pass

	def __init__(self):
		pass

	def __new__(self, S, ):
		pass

	def width(self):
		pass

	def add(self, name):
		pass

	def setName(self, name):
		pass

	def setT(self, newT):
		pass

	def setR(self, newR):
		pass

	def fromUV(self):
		pass

	def setX(self, newX):
		pass

	def setY(self, newY):
		pass

	def setHeight(self, newHeight):
		pass

	def pixelAspect(self):
		pass

	def name(self):
		pass

	def r(self):
		pass

	def t(self):
		pass

	def toUV(self):
		pass

	def y(self):
		pass

	def x(self):
		pass


class Format_Knob(Knob):

	def setValue(self, format):
		pass

	def __new__(self, S, ):
		pass

	def fromScript(self, s):
		pass

	def value(self):
		pass

	def actualValue(self):
		pass

	def toScript(self):
		pass

	def notDefault(self):
		pass

	def __init__(self):
		pass

	def name(self):
		pass


class FrameRange(object):

	def minFrame(self):
		pass

	def last(self):
		pass

	def __new__(self, S, ):
		pass

	def setLast(self, n):
		pass

	def __str__(self):
		pass

	def getFrame(self, n):
		pass

	def stepFrame(self):
		pass

	def setFirst(self, n):
		pass

	def next(self):
		pass

	def isInRange(self, n):
		pass

	def maxFrame(self):
		pass

	def __iter__(self):
		pass

	def setIncrement(self, n):
		pass

	def increment(self):
		pass

	def frames(self):
		pass

	def __init__(self):
		pass

	def first(self):
		pass


class FrameRanges(object):

	def compact(self):
		pass

	def getRange(self):
		pass

	def __new__(self, S, ):
		pass

	def toFrameList(self):
		pass

	def __str__(self):
		pass

	def minFrame(self):
		pass

	def add(self, r):
		pass

	def next(self):
		pass

	def maxFrame(self):
		pass

	def __iter__(self):
		pass

	def clear(self):
		pass

	def __init__(self):
		pass

	def size(self):
		pass


class FreeType_Knob(Knob):

	def setValue(self, family, style):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass

	def getValue(self):
		pass


class GeoSelect_Knob(Knob):

	def __setattr__(self):
		pass

	def getSelection(self):
		pass

	def __getattribute__(self, name):
		pass

	def getGeometry(self):
		pass

	def __delattr__(self, name):
		pass


class Gizmo(Group):

	def __getitem__(self, y):
		pass

	def __str__(self):
		pass

	def filename(self):
		pass

	def command(self):
		pass

	def __repr__(self):
		pass

	def makeGroup(self):
		pass

	def __len__(self):
		pass


class GlobalsEnvironment(object):

	def __delitem__(self, y):
		pass

	def __new__(self, S, ):
		pass

	def __getitem__(self, y):
		pass

	def __contains__(self):
		pass

	def keys(self):
		pass

	def items(self):
		pass

	def get(self):
		pass

	def __setitem__(self):
		pass

	def has_key(self):
		pass

	def values(self):
		pass

	def __repr__(self):
		pass

	def __len__(self):
		pass


class Group(Node):

	def node(self, s):
		pass

	def __exit__(self):
		pass

	def begin(self):
		pass

	def __enter__(self):
		pass

	def run(self, callable):
		pass

	def __getitem__(self, y):
		pass

	def numNodes(self):
		pass

	def connectSelectedNodes(self):
		pass

	def __str__(self):
		pass

	def selectedNode(self):
		pass

	def selectedNodes(self):
		pass

	def __reduce_ex__(self):
		pass

	def __repr__(self):
		pass

	def output(self):
		pass

	def expand(self):
		pass

	def end(self):
		pass

	def nodes(self):
		pass

	def splaySelectedNodes(self):
		pass

	def subgraphLocked(self):
		pass

	def __len__(self):
		pass


class Hash(object):

	def reset(self):
		pass

	def __ne__(self, y):
		pass

	def __setattr__(self):
		pass

	def __new__(self, S, ):
		pass

	def setHash(self):
		pass

	def __getattribute__(self, name):
		pass

	def __delattr__(self, name):
		pass

	def __le__(self, y):
		pass

	def append(self):
		pass

	def __gt__(self, y):
		pass

	def __hash__(self):
		pass

	def getHash(self):
		pass

	def __lt__(self, y):
		pass

	def __eq__(self, y):
		pass

	def __ge__(self, y):
		pass


class Help_Knob(Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Histogram_Knob(Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class IArray_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def height(self):
		pass

	def width(self):
		pass

	def __init__(self):
		pass

	def dimensions(self):
		pass


class Info(object):

	def __new__(self, S, ):
		pass

	def h(self):
		pass

	def w(self):
		pass

	def y(self):
		pass

	def x(self):
		pass

	def __init__(self):
		pass


class Int_Knob(Array_Knob):

	def value(self):
		pass

	def setValue(self, val):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Keyer_Knob(Array_Knob):

	def highTol(self):
		pass

	def lowSoft(self):
		pass

	def lowTol(self):
		pass

	def value(self):
		pass

	def names(self, n):
		pass

	def highSoft(self):
		pass

	def __init__(self):
		pass

	def __new__(self, S, ):
		pass


class Knob(object):

	def clearAnimated(self):
		pass

	def setLabel(self, s):
		pass

	def setTooltip(self, s):
		pass

	def removeKey(self):
		pass

	def getFlag(self, f):
		pass

	def setEnabled(self, enabled):
		pass

	def removeKeyAt(self):
		pass

	def visible(self):
		pass

	def warning(self, message):
		pass

	def getIntegral(self):
		pass

	def __init__(self):
		pass

	def isKeyAt(self):
		pass

	def hasExpression(self, index=-1):
		pass

	def __new__(self, S, ):
		pass

	def getKeyTime(self):
		pass

	def tooltip(self):
		pass

	def label(self):
		pass

	def setFlag(self, f):
		pass

	def getNumKeys(self):
		pass

	def critical(self, message):
		pass

	def toScript(self):
		pass

	def getKeyList(self):
		pass

	def clearFlag(self, f):
		pass

	def Class(self):
		pass

	def node(self):
		pass

	def fullyQualifiedName(self, channel=-1):
		pass

	def setValue(self):
		pass

	def setName(self, s):
		pass

	def isAnimated(self):
		pass

	def setAnimated(self):
		pass

	def getDerivative(self):
		pass

	def setExpression(self):
		pass

	def setValueAt(self):
		pass

	def getNthDerivative(self):
		pass

	def getValueAt(self):
		pass

	def name(self):
		pass

	def isKey(self):
		pass

	def fromScript(self):
		pass

	def enabled(self):
		pass

	def value(self):
		pass

	def getValue(self):
		pass

	def getKeyIndex(self):
		pass

	def error(self, message):
		pass

	def debug(self, message):
		pass

	def setVisible(self, visible):
		pass


class KnobScripterPane(KnobScripter):

	def hideEvent(self, the_event):
		pass

	def showEvent(self, the_event):
		pass

	def __init__(self, node, knob):
		pass


class KnobType(object):
	pass

class Layer(object):

	def __new__(self, S, ):
		pass

	def setName(self, newName):
		pass

	def channels(self):
		pass

	def visible(self):
		pass

	def name(self):
		pass


class Link_Knob(Knob):

	def setValue(self):
		pass

	def getLinkedKnob(self):
		pass

	def __new__(self, S, ):
		pass

	def revertOverride(self):
		pass

	def value(self):
		pass

	def getLink(self):
		pass

	def __init__(self):
		pass

	def setLink(self, s):
		pass

	def applyOverride(self):
		pass

	def makeLink(self):
		pass


class LinkableKnobInfo(object):

	def knob(self):
		pass

	def __setattr__(self):
		pass

	def displayName(self):
		pass

	def enabled(self):
		pass

	def __getattribute__(self, name):
		pass

	def __delattr__(self, name):
		pass

	def indices(self):
		pass

	def absolute(self):
		pass


class LiveGroup(Precomp):

	def applyOverrides(self):
		pass

	def revertOverrides(self):
		pass

	def isLocal(self):
		pass

	def __getitem__(self, y):
		pass

	def __str__(self):
		pass

	def makeEditable(self):
		pass

	def publish(self, file):
		pass

	def anyOverrides(self):
		pass

	def modified(self):
		pass

	def makeLocal(self):
		pass

	def __repr__(self):
		pass

	def published(self):
		pass

	def __len__(self):
		pass


class LookupCurves_Knob(Knob):

	def delCurve(self, curve):
		pass

	def __new__(self, S, ):
		pass

	def editCurve(self):
		pass

	def addCurve(self):
		pass

	def __init__(self):
		pass


class Lut(object):

	def __new__(self, S, ):
		pass

	def toByte(self, float):
		pass

	def fromByteSingle(self, float):
		pass

	def fromFloat(self):
		pass

	def toFloat(self):
		pass

	def isLinear(self):
		pass

	def toByteSingle(self, float):
		pass

	def fromByte(self, float):
		pass

	def isZero(self):
		pass


class Menu(MenuItem):

	def addAction(self, action):
		pass

	def name(self):
		pass

	def addSeparator(self, **kwargs):
		pass

	def menu(self, name):
		pass

	def addCommand(self):
		pass

	def addMenu(self, **kwargs):
		pass

	def removeItem(self, name):
		pass

	def updateMenuItems(self):
		pass

	def items(self):
		pass

	def findItem(self, name):
		pass

	def clearMenu(self):
		pass


class MenuBar(object):

	def addAction(self, action):
		pass

	def name(self):
		pass

	def addSeparator(self, **kwargs):
		pass

	def menu(self, name):
		pass

	def addCommand(self):
		pass

	def addMenu(self, **kwargs):
		pass

	def removeItem(self, name):
		pass

	def updateMenuItems(self):
		pass

	def items(self):
		pass

	def findItem(self, name):
		pass

	def clearMenu(self):
		pass


class MenuItem(object):

	def setEnabled(self):
		pass

	def name(self):
		pass

	def invoke(self):
		pass

	def script(self):
		pass

	def setScript(self, script):
		pass

	def setIcon(self, icon):
		pass

	def setShortcut(self, keySequence):
		pass

	def shortcut(self):
		pass

	def action(self):
		pass

	def setVisible(self, visible):
		pass

	def icon(self):
		pass


class MultiView_Knob(Knob):

	def toScriptPrefix(self):
		pass

	def setValue(self, s):
		pass

	def __new__(self, S, ):
		pass

	def fromScript(self, s):
		pass

	def value(self):
		pass

	def toScriptPrefixUserKnob(self):
		pass

	def toScript(self):
		pass

	def notDefault(self):
		pass

	def __init__(self):
		pass


class Multiline_Eval_String_Knob(EvalString_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Node(object):

	def help(self):
		pass

	def lastFrame(self):
		pass

	def __str__(self):
		pass

	def maxOutputs(self):
		pass

	def performanceInfo(self, category):
		pass

	def minimumInputs(self):
		pass

	def setXpos(self, x):
		pass

	def resetKnobsToDefault(self):
		pass

	def hideControlPanel(self):
		pass

	def setYpos(self, y):
		pass

	def connectInput(self):
		pass

	def input(self, i):
		pass

	def executePythonCallback(self, string):
		pass

	def treeHasError(self):
		pass

	def knob(self):
		pass

	def __getitem__(self, y):
		pass

	def format(self):
		pass

	def dependent(self):
		pass

	def forceValidate(self):
		pass

	def bbox(self):
		pass

	def locked(self):
		pass

	def name(self):
		pass

	def forceUpdateLocalization(self):
		pass

	def screenHeight(self):
		pass

	def rootNode(self):
		pass

	def redraw(self):
		pass

	def getNumKnobs(self):
		pass

	def writeKnobs(self, i):
		pass

	def deepSample(self):
		pass

	def fileDependencies(self):
		pass

	def unlock(self):
		pass

	def maximumOutputs(self):
		pass

	def screenWidth(self):
		pass

	def shown(self):
		pass

	def isLocalized(self):
		pass

	def isSelected(self):
		pass

	def allKnobs(self):
		pass

	def deepSampleCount(self):
		pass

	def frameRange(self):
		pass

	def Class(self):
		pass

	def metadata(self):
		pass

	def parent(self):
		pass

	def setXYpos(self):
		pass

	def ypos(self):
		pass

	def dependencies(self, what):
		pass

	def proxy(self):
		pass

	def showInfo(self, s):
		pass

	def __repr__(self):
		pass

	def addCallback(self):
		pass

	def setSelected(self, selected):
		pass

	def localizationProgress(self):
		pass

	def upstreamFrameRange(self, i):
		pass

	def height(self):
		pass

	def channels(self):
		pass

	def setInput(self):
		pass

	def canSetInput(self):
		pass

	def fullName(self):
		pass

	def firstFrame(self):
		pass

	def numKnobs(self):
		pass

	def width(self):
		pass

	def removeKnob(self, k):
		pass

	def __len__(self):
		pass

	def hasError(self):
		pass

	def setName(self):
		pass

	def clones(self):
		pass

	def pixelAspect(self):
		pass

	def selectOnly(self):
		pass

	def readKnobs(self, s):
		pass

	def autoplace(self):
		pass

	def optionalInput(self):
		pass

	def clearCallbacks(self):
		pass

	def clearCustomIcon(self):
		pass

	def error(self):
		pass

	def lock(self):
		pass

	def maximumInputs(self):
		pass

	def xpos(self):
		pass

	def sample(self):
		pass

	def setCustomIcon(self):
		pass

	def __reduce_ex__(self):
		pass

	def __new__(self, S, ):
		pass

	def maxInputs(self):
		pass

	def opHashes(self):
		pass

	def showControlPanel(self):
		pass

	def knobs(self):
		pass

	def removeCallback(self, string):
		pass

	def inputs(self):
		pass

	def running(self):
		pass

	def linkableKnobs(self, knobType):
		pass

	def minInputs(self):
		pass

	def addKnob(self, k):
		pass

	def setTab(self, tabIndex):
		pass

	def isLocalizationOutdated(self):
		pass


class NodeConstructor(object):

	def __call__(self):
		pass

	def __new__(self, S, ):
		pass


class Nodes(object):

	def __new__(self, S, ):
		pass


class Obsolete_Knob(Knob):

	def setValue(self):
		pass

	def value(self):
		pass

	def __init__(self):
		pass


class OneView_Knob(Enumeration_Knob):

	def __new__(self, S, ):
		pass


class OutputContext(object):

	def viewcount(self):
		pass

	def __new__(self, S, ):
		pass

	def viewname(self, n):
		pass

	def setFrame(self, f):
		pass

	def frame(self):
		pass

	def viewFromName(self, name):
		pass

	def setView(self, n):
		pass

	def viewshort(self, n):
		pass

	def view(self):
		pass


class Panel(object):

	def addEnumerationPulldown(self):
		pass

	def show(self):
		pass

	def setTitle(self, val):
		pass

	def addButton(self):
		pass

	def addPasswordInput(self):
		pass

	def value(self, name):
		pass

	def setWidth(self, val):
		pass

	def __new__(self, S, ):
		pass

	def title(self):
		pass

	def addMultilineTextInput(self):
		pass

	def width(self):
		pass

	def addRGBColorChip(self):
		pass

	def addClipnameSearch(self):
		pass

	def addNotepad(self):
		pass

	def addScriptCommand(self):
		pass

	def addSingleLineInput(self):
		pass

	def addTextFontPulldown(self):
		pass

	def execute(self, name):
		pass

	def clear(self):
		pass

	def addFilenameSearch(self):
		pass

	def addBooleanCheckBox(self):
		pass

	def addExpressionInput(self):
		pass


class PanelNode(object):

	def writeKnobs(self, i):
		pass

	def createWidget(self):
		pass

	def __new__(self, S, ):
		pass

	def __str__(self):
		pass

	def addKnob(self, k):
		pass

	def removeKnob(self, k):
		pass

	def knobs(self):
		pass

	def readKnobs(self, s):
		pass


class Password_Knob(Knob):

	def setValue(self):
		pass

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def getText(self):
		pass

	def __init__(self):
		pass


class Precomp(Group):

	def __getitem__(self, y):
		pass

	def __str__(self):
		pass

	def reload(self):
		pass

	def __repr__(self):
		pass

	def __len__(self):
		pass


class ProgressTask(object):

	def setProgress(self, i):
		pass

	def isCancelled(self):
		pass

	def __new__(self, S, ):
		pass

	def setMessage(self, s):
		pass


class Pulldown_Knob(Enumeration_Knob):

	def commands(self, n):
		pass

	def __new__(self, S, ):
		pass

	def numValues(self):
		pass

	def value(self):
		pass

	def setValues(self, items):
		pass

	def itemName(self, n):
		pass

	def __init__(self):
		pass


class PyCustom_Knob(Script_Knob):

	def getObject(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class PyScript_Knob(Script_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class PythonCustomKnob(Script_Knob):

	def getObject(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class PythonKnob(String_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Radio_Knob(Enumeration_Knob):

	def setValue(self, item):
		pass

	def __new__(self, S, ):
		pass

	def numValues(self):
		pass

	def value(self):
		pass

	def enumName(self, n):
		pass

	def values(self):
		pass

	def setValues(self, items):
		pass

	def __init__(self):
		pass


class Range_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Root(Group):

	def lastFrame(self):
		pass

	def __str__(self):
		pass

	def maximumInputs(self):
		pass

	def modified(self):
		pass

	def channels(self):
		pass

	def setInput(self):
		pass

	def canSetInput(self):
		pass

	def maximumOutputs(self):
		pass

	def minimumInputs(self):
		pass

	def firstFrame(self):
		pass

	def layers(self):
		pass

	def __new__(self, S, ):
		pass

	def realFps(self):
		pass

	def connectInput(self):
		pass

	def fps(self):
		pass

	def setProxy(self, b):
		pass

	def input(self):
		pass

	def __len__(self):
		pass

	def addView(self):
		pass

	def deleteView(self, s):
		pass

	def inputs(self):
		pass

	def __getitem__(self, y):
		pass

	def mergeFrameRange(self):
		pass

	def setModified(self, b):
		pass

	def getOCIOColorspaceFamily(self, colorspace):
		pass

	def proxy(self):
		pass

	def clones(self):
		pass

	def setView(self, s):
		pass

	def setFrame(self, n):
		pass

	def optionalInput(self):
		pass

	def getOCIOColorspaceFromViewTransform(self):
		pass

	def __repr__(self):
		pass


class RunInMainThread(object):

	def request(self):
		pass

	def result(self):
		pass


class Scale_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def names(self, n):
		pass

	def y(self, oc):
		pass

	def x(self, oc):
		pass

	def z(self, oc):
		pass

	def __init__(self):
		pass


class SceneView_Knob(Unsigned_Knob):

	def getHighlightedItem(self):
		pass

	def __new__(self, S, ):
		pass

	def setSelectedItems(self):
		pass

	def setImportedItems(self, items):
		pass

	def setAllItems(self):
		pass

	def removeItems(self):
		pass

	def getAllItems(self):
		pass

	def getImportedItems(self):
		pass

	def getSelectedItems(self):
		pass

	def __init__(self):
		pass

	def addItems(self):
		pass


class Script_Knob(String_Knob):

	def execute(self):
		pass

	def setValue(self, cmd):
		pass

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def command(self):
		pass

	def setCommand(self, cmd):
		pass

	def __init__(self):
		pass


class String_Knob(Knob):

	def splitView(self, view):
		pass

	def setValue(self):
		pass

	def __new__(self, S, ):
		pass

	def setText(self):
		pass

	def getText(self, oc):
		pass

	def getValue(self, oc):
		pass

	def value(self, oc):
		pass

	def unsplitView(self, view):
		pass

	def __init__(self):
		pass


class Tab_Knob(Knob):

	def setValue(self):
		pass

	def __new__(self, S, ):
		pass

	def value(self):
		pass


class Text_Knob(Knob):

	def value(self):
		pass

	def setValue(self):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class ToolBar(object):

	def addAction(self, action):
		pass

	def __new__(self, S, ):
		pass

	def addSeparator(self, **kwargs):
		pass

	def menu(self, name):
		pass

	def addCommand(self):
		pass

	def addMenu(self, **kwargs):
		pass

	def name(self):
		pass

	def removeItem(self, name):
		pass

	def updateMenuItems(self):
		pass

	def items(self):
		pass

	def findItem(self, name):
		pass

	def clearMenu(self):
		pass


class Transform2d_Knob(Knob):

	def value(self, oc):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class UV_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass

	def names(self, n):
		pass


class Undo(object):

	def disabled(self):
		pass

	def undoDescribe(self):
		pass

	def cancel(self):
		pass

	def redo(self):
		pass

	def undoSize(self):
		pass

	def end(self):
		pass

	def __new__(self, S, ):
		pass

	def redoDescribe(self):
		pass

	def __enter__(self):
		pass

	def redoDescribeFully(self):
		pass

	def new(self):
		pass

	def redoTruncate(self):
		pass

	def undoTruncate(self):
		pass

	def begin(self):
		pass

	def enable(self):
		pass

	def __exit__(self):
		pass

	def undo(self):
		pass

	def disable(self):
		pass

	def redoSize(self):
		pass

	def name(self):
		pass

	def undoDescribeFully(self):
		pass


class Unsigned_Knob(Array_Knob):

	def value(self):
		pass

	def setValue(self, val):
		pass

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class View(object):

	def __new__(self, S, ):
		pass

	def __str__(self):
		pass

	def value(self):
		pass

	def __init__(self):
		pass

	def string(self):
		pass


class ViewView_Knob(Knob):

	def __new__(self, S, ):
		pass

	def __init__(self):
		pass


class Viewer(Node):

	def roi(self):
		pass

	def frameCached(self, f):
		pass

	def sendMouseEvent(self):
		pass

	def setRoi(self, box):
		pass

	def isPlayingOrRecording(self):
		pass

	def __getitem__(self, y):
		pass

	def playbackRange(self):
		pass

	def __str__(self):
		pass

	def recordMouse(self):
		pass

	def toggleWaitOnReplayEvents(self):
		pass

	def recordMouseStop(self):
		pass

	def toggleMouseTrails(self):
		pass

	def capture(self, file):
		pass

	def replayMouseSync(self, xmlRecordingFilename):
		pass

	def __repr__(self):
		pass

	def roiEnabled(self):
		pass

	def replayMouseAsync(self, xmlRecordingFilename):
		pass

	def __len__(self):
		pass


class ViewerProcess(object):

	def unregister(self, name):
		pass

	def node(self):
		pass

	def register(self):
		pass

	def registeredNames(self):
		pass


class ViewerWindow(object):

	def node(self):
		pass

	def activeInput(self, secondary=False):
		pass

	def play(self):
		pass

	def previousView(self):
		pass

	def nextView(self):
		pass

	def getGLCameraMatrix(self):
		pass

	def getGeometryNodes(self):
		pass

	def stop(self):
		pass

	def activateInput(self):
		pass

	def setView(self, s):
		pass

	def frameControl(self, i):
		pass

	def view(self):
		pass


class WH_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def y_at(self):
		pass

	def names(self):
		pass

	def y(self):
		pass

	def x(self):
		pass

	def x_at(self):
		pass

	def __init__(self):
		pass


class XYZ_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def parent(self):
		pass

	def value(self):
		pass

	def names(self, n):
		pass

	def y(self, oc):
		pass

	def x(self, oc):
		pass

	def z(self, oc):
		pass

	def __init__(self):
		pass


class XY_Knob(Array_Knob):

	def __new__(self, S, ):
		pass

	def value(self):
		pass

	def names(self, n):
		pass

	def y(self, oc):
		pass

	def x(self, oc):
		pass

	def __init__(self):
		pass


def __filterNames(name):
		pass


def activeViewer():
		pass


def addAfterBackgroundFrameRender(call, args, kwargs):
	pass

	def foo(context):
		pass

def addAfterBackgroundRender(call,args,kwargs):
	pass

	def foo(context):
		pass

def addAfterFrameRender(call,args,kwargs,nodeClass):
		pass

def addAfterRecording(call,args,kwargs,nodeClass):
		pass

def addAfterRender(call,args,kwargs,nodeClass):
		pass

def addAfterReplay(call,args,kwargs,nodeClass):
		pass

def addAutoSaveDeleteFilter(filter):
		pass

def addAutoSaveFilter(filter):
		pass

def addAutoSaveRestoreFilter(filter):
		pass

def addAutolabel(call,args,kwargs,nodeClass):
		pass

def addBeforeBackgroundRender(call,args,kwargs):
	pass

	def foo(context):
		pass

def addBeforeFrameRender(call,args,kwargs,nodeClass):
		pass

def addBeforeRecording(call,args,kwargs,nodeClass):
		pass

def addBeforeRender(call,args,kwargs,nodeClass):
		pass

def addBeforeReplay(call,args,kwargs,nodeClass):
		pass

def addDefaultColorspaceMapper(call,args,kwargs,nodeClass):
		pass

def addFavoriteDir():
		pass

def addFilenameFilter(call,args,kwargs,nodeClass):
		pass

def addFormat(s):
		pass

def addKnobChanged(call,args,kwargs,nodeClass,node):
		pass

def addNodePresetExcludePaths( paths ):
		pass

def addOnCreate(call,args,kwargs,nodeClass):
		pass

def addOnDestroy(call,args,kwargs,nodeClass):
		pass

def addOnScriptClose(call,args,kwargs,nodeClass):
		pass

def addOnScriptLoad(call,args,kwargs,nodeClass):
		pass

def addOnScriptSave(call,args,kwargs,nodeClass):
		pass

def addOnUserCreate(call,args,kwargs,nodeClass):
		pass

def addRenderProgress(call,args,kwargs,nodeClass):
		pass

def addSequenceFileExtension( fileExtension ):
		pass

def addToolsetExcludePaths( paths ):
		pass

def addUpdateUI(call,args,kwargs,nodeClass):
		pass

def addValidateFilename(call,args,kwargs,nodeClass):
		pass

def addView(s):
		pass

def afterBackgroundFrameRender(context):
		pass

def afterBackgroundRender(context):
		pass

def afterFrameRender():
		pass

def afterRecording():
		pass

def afterRender():
		pass

def afterReplay():
		pass

def alert(prompt):
		pass

def allNodes():
		pass

def animation():
		pass

def animationEnd():
		pass

def animationIncrement():
		pass

def animationStart():
		pass

def animations():
		pass

def applyPreset():
		pass

def applyUserPreset():
		pass

def ask(prompt):
		pass

def askWithCancel(prompt):
		pass

def autoSaveDeleteFilter(filename):
		pass

def autoSaveFilter(filename):
		pass

def autoSaveRestoreFilter(filename):
		pass

def autolabel():
		pass

def autoplace(n):
		pass

def autoplaceSnap(n):
		pass

def autoplace_all():
		pass

def autoplace_snap_all():
		pass

def autoplace_snap_selected():
		pass

def beforeBackgroundRender(context):
		pass

def beforeFrameRender():
		pass

def beforeRecording():
		pass

def beforeRender():
		pass

def beforeReplay():
		pass

def cacheUsage():
		pass

def canCreateNode(name):
		pass

def cancel():
		pass

def center():
		pass

def channels(n=None):
		pass

def choice():
		pass

def clearDiskCache():
		pass

def clearRAMCache():
		pass

def clearTabMenuFavorites():
		pass

def clearTabMenuWeighting():
		pass

def clone():
		pass

def cloneSelected(action):
		pass

def collapseToGroup(show=True):
		pass

def collapseToLiveGroup(show=True):
		pass

def connectNodes():
		pass

def connectViewer():
		pass

def createLiveInput():
		pass

def createNode():
		pass

def createScenefileBrowser():
		pass

def createToolset():
		pass

def critical(message):
		pass

def debug(message):
		pass

def defaultColorspaceMapper(colorspace,dataTypeHint):
		pass

def defaultFontPathname():
		pass

def defaultNodeColor(s):
		pass

def delete(n):
		pass

def deletePreset():
		pass

def deleteUserPreset():
		pass

def deleteView(s):
		pass

def dependencies(nodes,what):
		pass

def dependentNodes(what,nodes,evaluateAll):
		pass

def display():
		pass

def duplicateSelectedNodes():
		pass

def endGroup():
		pass

def error(message):
		pass

def execute():
		pass

def executeBackgroundNuke():
		pass

def executeInMainThread(call,args,kwargs):
		pass

def executeInMainThreadWithResult(call,args,kwargs):
		pass

def executeMultiple():
		pass

def executing():
		pass

def exists(s):
		pass

def expandSelectedGroup():
		pass

def expr(s):
		pass

def expression(s):
		pass

def extractSelected():
		pass

def filename():
		pass

def filenameFilter(filename):
		pass

def forceClone():
		pass

def forceLoad(n):
		pass

def fork():
		pass

def formats():
		pass

def frame(f):
		pass

def fromNode(n):
		pass

def getAllUserPresets():
		pass

def getClipname():
		pass

def getColor(initial):
		pass

def getColorspaceList(colorspaceKnob):
		pass

def getDeletedPresets():
		pass

def getFileNameList():
		pass

def getFilename():
		pass

def getFonts():
		pass

def getFramesAndViews():
		pass

def getInput():
		pass

def getNodeClassName():
		pass

def getNodePresetExcludePaths():
		pass

def getNodePresetID():
		pass

def getOcioColorSpaces():
		pass

def getPaneFor( panelName ):
		pass

def getPresetKnobValues():
		pass

def getPresets():
		pass

def getPresetsMenu(Node):
		pass

def getReadFileKnob(node):
		pass

def getRenderProgress():
		pass

def getToolsetExcludePaths():
		pass

def getUserPresetKnobValues():
		pass

def getUserPresets(Node):
		pass

def hotkeys():
		pass

def import_module(name,filterRule):
		pass

def inputs():
		pass

def invertSelection():
		pass

def knob():
		pass

def knobChanged():
		pass

def knobDefault():
		pass

def knobTooltip():
		pass

def layers(node=None):
		pass

def licenseInfo():
		pass

def load(s):
		pass

def loadToolset():
		pass

def localisationEnabled(knob):
		pass

def localiseFiles(readKnobs):
		pass

def localizationEnabled(knob):
		pass

def makeGroup(show=True):
		pass

def maxPerformanceInfo():
		pass

def memory():
		pass

def menu(name):
		pass

def message(prompt):
		pass

def modified(status):
		pass

def nodeCopy(s):
		pass

def nodeDelete(s):
		pass

def nodePaste(s):
		pass

def nodesSelected():
		pass

def numvalue():
		pass

def oculaPresent():
		pass

def ofxAddPluginAliasExclusion(fullOfxEffectName):
		pass

def ofxMenu():
		pass

def ofxPluginPath():
		pass

def ofxRemovePluginAliasExclusion(fullOfxEffectName):
		pass

def onCreate():
		pass

def onDestroy():
		pass

def onScriptClose():
		pass

def onScriptLoad():
		pass

def onScriptSave():
		pass

def onUserCreate():
		pass

def openPanels():
		pass

def pan():
		pass

def performanceProfileFilename():
		pass

def pluginAddPath(args,addToSysPath):
		pass

def pluginAppendPath(args,addToSysPath):
		pass

def pluginExists(name):
		pass

def pluginInstallLocation():
		pass

def pluginPath():
		pass

def plugins():
		pass

def recentFile(index):
		pass

def redo():
		pass

def removeAfterBackgroundFrameRender(call,args,kwargs):
		pass

def removeAfterBackgroundRender(call,args,kwargs):
		pass

def removeAfterFrameRender(call,args,kwargs,nodeClass):
		pass

def removeAfterRecording(call,args,kwargs,nodeClass):
		pass

def removeAfterRender(call,args,kwargs,nodeClass):
		pass

def removeAfterReplay(call,args,kwargs,nodeClass):
		pass

def removeAutoSaveDeleteFilter(filter):
		pass

def removeAutoSaveFilter(filter):
		pass

def removeAutoSaveRestoreFilter(filter):
		pass

def removeAutolabel(call,args,kwargs,nodeClass):
		pass

def removeBeforeBackgroundRender(call,args,kwargs):
		pass

def removeBeforeFrameRender(call,args,kwargs,nodeClass):
		pass

def removeBeforeRecording(call,args,kwargs,nodeClass):
		pass

def removeBeforeRender(call,args,kwargs,nodeClass):
		pass

def removeBeforeReplay(call,args,kwargs,nodeClass):
		pass

def removeDefaultColorspaceMapper(call,args,kwargs,nodeClass):
		pass

def removeFavoriteDir():
		pass

def removeFilenameFilter(call,args,kwargs,nodeClass):
		pass

def removeFilenameValidate(call,args,kwargs,nodeClass):
		pass

def removeKnobChanged(call,args,kwargs,nodeClass,node):
		pass

def removeOnCreate(call,args,kwargs,nodeClass):
		pass

def removeOnDestroy(call,args,kwargs,nodeClass):
		pass

def removeOnScriptClose(call,args,kwargs,nodeClass):
		pass

def removeOnScriptLoad(call,args,kwargs,nodeClass):
		pass

def removeOnScriptSave(call,args,kwargs,nodeClass):
		pass

def removeOnUserCreate(call,args,kwargs,nodeClass):
		pass

def removeRenderProgress(call,args,kwargs,nodeClass):
		pass

def removeUpdateUI(call,args,kwargs,nodeClass):
		pass

def render():
		pass

def renderProgress():
		pass

def rescanFontFolders():
		pass

def resetPerformanceTimers():
		pass

def restoreWindowLayout():
		pass

def resumePathProcessing():
		pass

def root():
		pass

def runIn():
		pass

def sample():
		pass

def saveEventGraphTimers(filePath):
		pass

def saveToScript():
		pass

def saveUserPreset():
		pass

def saveWindowLayout():
		pass

def scriptClear():
		pass

def scriptSaveAndClear(filename,ignoreUnsavedChanges):
		pass

def scriptExit():
		pass

def scriptName():
		pass

def scriptNew():
		pass

def scriptOpen():
		pass

def scriptReadFile():
		pass

def scriptReadText():
		pass

def scriptSave(filename=None):
		pass

def scriptSaveAndClear(filename,ignoreUnsavedChanges):
		pass

def scriptSaveAs():
		pass

def scriptSaveToTemp(string):
		pass

def scriptSource():
		pass

def script_directory():
		pass

def selectAll():
		pass

def selectConnectedNodes():
		pass

def selectPattern():
		pass

def selectSimilar(matchType):
		pass

def selectedNode():
		pass

def selectedNodes(filter):
		pass

def setPreset():
		pass

def setReadOnlyPresets(readOnly):
		pass

def setUserPreset():
		pass

def show():
		pass

def showBookmarkChooser(n):
		pass

def showCreateViewsDialog(views):
		pass

def showDag(n):
		pass

def showInfo(n):
		pass

def showSettings():
		pass

def splayNodes():
		pass

def startEventGraphTimers():
		pass

def startPerformanceTimers():
		pass

def stopEventGraphTimers():
		pass

def stopPerformanceTimers():
		pass

def stripFrameRange(clipname):
		pass

def suspendPathProcessing():
		pass

def tabClose():
		pass

def tabNext():
		pass

def tcl():
		pass

def thisClass():
		pass

def thisGroup():
		pass

def thisKnob():
		pass

def thisNode():
		pass

def thisPane():
		pass

def thisParent():
		pass

def thisRoot():
		pass

def thisView():
		pass

def toNode(s):
		pass

def toggleFullscreen():
		pass

def toggleViewers():
		pass

def toolbar():
		pass

def tprint():
		pass

def undo():
		pass

def updateUI():
		pass

def usingOcio():
		pass

def usingPerformanceTimers():
		pass

def validateFilename(filename):
		pass

def value():
		pass

def views():
		pass

def waitForThreadsToFinish():
		pass

def warning(message):
		pass

def zoom():
		pass

def zoomToFitSelected():
		pass

