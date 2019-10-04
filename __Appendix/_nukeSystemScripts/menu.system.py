# User interface initialization for Nuke
# -*- coding: utf-8 -*-
# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

# During startup the nuke lib loads this module, and a couple others, in the following order:
#   _pathsetup.py
#   init.py
#   menu.py
# _pathsetup has to be first since it sets up the paths to be able to 'import nuke'.

import sys
import os.path
import nuke

# Create the temp directory
try:
  os.makedirs(os.environ["NUKE_TEMP_DIR"])
except OSError:
  pass

# Hack - need a better way for nuke to know it is running inside NukeStudio
isNukeStudio = nuke.env['studio']

nuke.pluginAddPath("./icons", addToSysPath=False);

import nukescripts
import nukescripts.toolbars
import nukescripts.snap3d
import nukescripts.cameratracker
import nukescripts.modelbuilder
import nukescripts.applymaterial

# Set up the toolbars.
nukescripts.toolbars.setup_toolbars()

# Menu definitions

# File menu

def doLocalise(localiseAll):
  raise RuntimeError("This functionality has been removed, please check the documentation.")

# Use the following options to set the shortcut context in the call to menu addCommand.
# Setting the shortcut context to a widget will mean the shortcut will only be triggered
# if that widget (or it's children) has focus. If no shortcut context is specified the
# default context is window context i.e. it can be triggered from anywhere in the window.
# The enum is defined in nk_menu_python_add_item in PythonObject.cpp
windowContext = 0
applicationContext = 1
dagContext = 2

menubar = nuke.menu("Nuke");
m = menubar.addMenu("File")
m.addCommand("New Comp...", "nuke.scriptNew(\"\")", "^n")
m.addCommand("Open Comp...", "nuke.scriptOpen(\"\")", "^o")
m.addCommand("Open Recent Comp/@recent_file1", "nuke.scriptOpen(nuke.recentFile(1))", "#+1")
m.addCommand("Open Recent Comp/@recent_file2", "nuke.scriptOpen(nuke.recentFile(2))", "#+2")
m.addCommand("Open Recent Comp/@recent_file3", "nuke.scriptOpen(nuke.recentFile(3))", "#+3")
m.addCommand("Open Recent Comp/@recent_file4", "nuke.scriptOpen(nuke.recentFile(4))", "#+4")
m.addCommand("Open Recent Comp/@recent_file5", "nuke.scriptOpen(nuke.recentFile(5))", "#+5")
m.addCommand("Open Recent Comp/@recent_file6", "nuke.scriptOpen(nuke.recentFile(6))", "#+6")
m.addCommand("Close Comp", "nuke.scriptClose()", "^w")
m.addCommand("-", "", "")
m.addCommand("Save Comp", "nuke.scriptSave(\"\")", "^s")
m.addCommand("Save Comp As...", "nuke.scriptSaveAs(\"\")", "^+S")
m.addCommand("Save New Comp Version", "nukescripts.script_and_write_nodes_version_up()", "#+S")
m.addCommand("-", "", "")

m.addCommand("Insert Comp Nodes...", "nukescripts.import_script()", "")
m.addCommand("Export Comp Nodes...", "nukescripts.export_nodes_as_script()", "")
m.addCommand("Comp Script Command...", "nukescripts.script_command('')", "x", shortcutContext=dagContext)

def tcl_file():
  try:
    s = nuke.getFilename("Source Script", "*.tcl;*.nk;*.py", "", "script")
    (root, ext) = os.path.splitext(s)
    if ext == ".py":
      execfile(s)
    else:
      nuke.tcl('source',s)
  except:
    pass

def frameForward():
  v = nuke.activeViewer()
  if v != None:
    v.frameControl( 1 )
  else:
    nuke.frame( nuke.frame()+1 )

def frameBackward():
  v = nuke.activeViewer()
  if v != None:
    v.frameControl( -1 )
  else:
    nuke.frame( nuke.frame()-1 )

m.addCommand("Run Script...", "tcl_file()", "#X")
if not isNukeStudio:
  m.addCommand("@;Next Frame", "frameBackward()", "Left")
  m.addCommand("@;Previous Frame", "frameForward()", "Right")
m.addCommand("Comp Info", "nukescripts.script_data()", "#i", shortcutContext=dagContext)
m.addCommand("-", "", "")
m.addCommand("Clear", "nuke.scriptClear()")

m = menubar.addMenu("Edit")
m.addCommand("Undo", "nuke.undo()", "^z")
m.addCommand("Redo", "nuke.redo()", "+^z")
m.addCommand("-", "", "")
m.addCommand("Cut", "nuke.nodeCopy(nukescripts.cut_paste_file()); nukescripts.node_delete(popupOnError=True)", "^x", shortcutContext=dagContext)
m.addCommand("Copy", "nuke.nodeCopy(nukescripts.cut_paste_file())", "^c", shortcutContext=dagContext)
m.addCommand("Paste", "nuke.nodePaste(nukescripts.cut_paste_file())", "^v", shortcutContext=dagContext)
# invisible item so you can shift+paste:
m.addCommand("@;Paste2", "nuke.nodePaste(nukescripts.cut_paste_file())", "+^v", shortcutContext=dagContext)
m.addCommand("Duplicate", "nukescripts.node_copypaste()", "#c", shortcutContext=dagContext)
m.addCommand("Delete", "nukescripts.node_delete(popupOnError=True)", "0xffff", shortcutContext=dagContext)
m.addCommand("@;Delete", "nukescripts.node_delete(popupOnError=True)", "0xff08", shortcutContext=dagContext)
m.addCommand("-", "", "")
m.addCommand("Clone", "nuke.cloneSelected()", "#k", shortcutContext=dagContext)
m.addCommand("Copy As Clones", "nuke.cloneSelected(\"copy\")", "^k", shortcutContext=dagContext)
m.addCommand("Force Clone", "nuke.forceClone()", "^#+k", shortcutContext=dagContext)
m.addCommand("Declone", "\n\
selnodes = nuke.selectedNodes()\n\
for i in selnodes:\n\
  nukescripts.declone(i)", "#+k", shortcutContext=dagContext)
m.addCommand("-", "", "")
m.addCommand("Search...", "nuke.selectPattern()", "/", shortcutContext=dagContext)
m.addCommand("Select All", "nuke.selectAll()", "^a", shortcutContext=dagContext)
m.addCommand("Select Similar/Color", "nuke.selectSimilar(nuke.MATCH_COLOR)", shortcutContext=dagContext)
m.addCommand("Select Similar/Class", "nuke.selectSimilar(nuke.MATCH_CLASS)", shortcutContext=dagContext)
m.addCommand("Select Similar/Label", "nuke.selectSimilar(nuke.MATCH_LABEL)", shortcutContext=dagContext)
m.addCommand("Select Connected Nodes", "nuke.selectConnectedNodes()", "^#A", shortcutContext=dagContext)
if not isNukeStudio:
  m.addCommand("@;Select Connected Nodes", "nuke.selectConnectedNodes()", "^#á", shortcutContext=dagContext)   # some keyboard layouts translate Ctrl+Alt+A to Ctrl+Alt+á
m.addCommand("Invert Selection", "nuke.invertSelection()", shortcutContext=dagContext)
m.addCommand("Bookmark/Jump to Bookmarked Node", "nuke.showBookmarkChooser()", "j", shortcutContext=dagContext )
m.addCommand("Bookmark/-", "", "")
m.addCommand("Bookmark/Restore Location 1", "nukescripts.bookmarks.quickRestore(1)", "+F7", shortcutContext=dagContext)
m.addCommand("Bookmark/Restore Location 2", "nukescripts.bookmarks.quickRestore(2)", "+F8", shortcutContext=dagContext)
m.addCommand("Bookmark/Restore Location 3", "nukescripts.bookmarks.quickRestore(3)", "+F9", shortcutContext=dagContext)
m.addCommand("Bookmark/Restore Location 4", "nukescripts.bookmarks.quickRestore(4)", "+F10", shortcutContext=dagContext)

m.addCommand("Bookmark/-", "", "")
m.addCommand("Bookmark/Save Location 1", "nukescripts.bookmarks.quickSave(1)", "^F7", shortcutContext=dagContext)
m.addCommand("Bookmark/Save Location 2", "nukescripts.bookmarks.quickSave(2)", "^F8", shortcutContext=dagContext)
m.addCommand("Bookmark/Save Location 3", "nukescripts.bookmarks.quickSave(3)", "^F9", shortcutContext=dagContext)
m.addCommand("Bookmark/Save Location 4", "nukescripts.bookmarks.quickSave(4)", "^F10", shortcutContext=dagContext)
m.addCommand("-", "", "")

isLinux = not nuke.env['WIN32'] and not nuke.env['MACOS']

n = m.addMenu("Node")
n.addCommand("Filename/Show", "nukescripts.showname()", "q", shortcutContext=dagContext)
n.addCommand("Filename/Search and Replace...", "nukescripts.search_replace()", "^+?" if isLinux else "^+/", shortcutContext=dagContext)
n.addCommand("Filename/Set Versions", "nuke.tcl('cam_ver_panel')", shortcutContext=dagContext)
n.addCommand("Filename/Version Up", "nukescripts.version_up()", "#Up", shortcutContext=dagContext)
n.addCommand("Filename/Version Down", "nukescripts.version_down()", "#Down", shortcutContext=dagContext)
n.addCommand("Filename/Version to Latest (Reads only)", "nukescripts.version_latest()", "#+Up", shortcutContext=dagContext)
n.addCommand("Filename/Camera Up", "nukescripts.camera_up()", "#Right", shortcutContext=dagContext)
n.addCommand("Filename/Camera Down", "nukescripts.camera_down()", "#Left", shortcutContext=dagContext)

n.addCommand("Group/Collapse To Group", "nuke.collapseToGroup()", "^g", shortcutContext=dagContext)
n.addCommand("Group/Expand Group", "nuke.expandSelectedGroup()", "^#g", shortcutContext=dagContext)
# Add another one hidden to get Ctrl+Enter (keypad) as well as Ctrl+Return
n.addCommand("Group/Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Enter", shortcutContext=dagContext)
n.addCommand("@;Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Return", shortcutContext=dagContext)
n.addCommand("Group/Copy Nodes To Group", "nuke.makeGroup()", "^#+g", shortcutContext=dagContext)
n.addCommand("Group/Copy Gizmo To Group", "nuke.tcl('copy_gizmo_to_group [ selected_node ]')", "^+g", shortcutContext=dagContext)

n.addCommand("Color...", "nukescripts.color_nodes()", "^+c", shortcutContext=dagContext)
n.addCommand("Un-color", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  i.knob(\"tile_color\").setValue(0)\n\
", shortcutContext=dagContext)
n.addCommand("Paste Knob Values", "nukescripts.copy_knobs(\"\")", "^#V", shortcutContext=dagContext)
n.addCommand("Input On\/Off", "nukescripts.toggle(\"hide_input\")", "#h", shortcutContext=dagContext)
n.addCommand("Postage Stamp On\/Off", "nukescripts.toggle(\"postage_stamp\")", "#p", shortcutContext=dagContext)
n.addCommand("Force Dope Sheet On\/Off", "nukescripts.toggle(\"dope_sheet\")", "#d", shortcutContext=dagContext)
n.addCommand("Bookmark On\/Off", "nukescripts.toggle(\"bookmark\")", "^+B", shortcutContext=dagContext)

def _autoplace():
  n = nuke.selectedNodes()
  for i in n:
    nuke.autoplace(i)

n.addCommand("Autoplace", "_autoplace()", "l", shortcutContext=dagContext)
n.addCommand("Buffer On\/Off", "nukescripts.toggle(\"cached\")", "^b", shortcutContext=dagContext)
n.addCommand("Disable\/Enable", "nukescripts.toggle(\"disable\")", "d")
n.addCommand("Info Viewer", "nukescripts.infoviewer()", "i", shortcutContext=dagContext)
n.addCommand("Open", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.show(i)\n\
", "0xff0d", shortcutContext=dagContext)
n.addCommand("Snap to Grid", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "|", shortcutContext=dagContext)
n.addCommand("Snap All to Grid", "\n\
n = nuke.allNodes();\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "\\", shortcutContext=dagContext)
n.addCommand("Swap A - B", "nukescripts.swapAB(nuke.selectedNode())", "+X", shortcutContext=dagContext)
n.addCommand("Connect", "nuke.connectNodes(False, False)", "y", shortcutContext=dagContext)
n.addCommand("Connect Backward", "nuke.connectNodes(True, False)", "+y", shortcutContext=dagContext)
n.addCommand("Connect A", "nuke.connectNodes(False, True)", "#y", shortcutContext=dagContext)
n.addCommand("Connect Backward - A", "nuke.connectNodes(True, True)", "+#y", shortcutContext=dagContext)
n.addCommand("Splay First", "nuke.splayNodes(False, False)", "u", shortcutContext=dagContext)
n.addCommand("Splay Last", "nuke.splayNodes(True, False)", "+u", shortcutContext=dagContext)
n.addCommand("Splay First to A", "nuke.splayNodes(False, True)", "#u", shortcutContext=dagContext)
n.addCommand("Splay Last to A", "nuke.splayNodes(True, True)", "+#u", shortcutContext=dagContext)

def _copyKnobsFromScriptToScript(n, m):
  k1 = n.knobs()
  k2 = m.knobs()
  excludedKnobs = ["name", "xpos", "ypos"]
  intersection = dict([(item, k1[item]) for item in k1.keys() if item not in excludedKnobs and k2.has_key(item)])
  for k in intersection.keys():
    x1 = n[k]
    x2 = m[k]
    x2.fromScript(x1.toScript(False))

def _useAsInputProcess():
  n = nuke.selectedNode()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  # FIXME: these two calls should have the arguments in the same order, or even better change the node bindings so they can go.
  if nuke.dependencies([n], nuke.INPUTS | nuke.HIDDEN_INPUTS) or nuke.dependentNodes(nuke.INPUTS | nuke.HIDDEN_INPUTS, [n]):
    m = nuke.createNode(n.Class())
  else:
    m = n
  if m is not n: _copyKnobsFromScriptToScript(n, m)
  viewer = nuke.activeViewer().node()
  viewer['input_process'].setValue(True)
  viewer['input_process_node'].setValue(m.name())

def _copyViewerProcessToDAG():
  vpNode = nuke.ViewerProcess.node()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  n = nuke.createNode(vpNode.Class())
  _copyKnobsFromScriptToScript(vpNode, n)

n.addCommand("Use as Input Process", "_useAsInputProcess()", shortcutContext=dagContext)
n.addCommand("Copy Viewer Process to Node Graph", "_copyViewerProcessToDAG()", shortcutContext=dagContext)

m.addCommand("Remove Input", "nukescripts.remove_inputs()", "^d", shortcutContext=dagContext)
m.addCommand("Extract", "nuke.extractSelected()", "+^x", shortcutContext=dagContext)
m.addCommand("Branch", "nukescripts.branch()", "#b", shortcutContext=dagContext)

def _internal_expression_arrow_cmd():
  p = nuke.toNode("preferences")
  ea = p.knob("expression_arrows");
  ca = p.knob("clone_arrows");
  ea.setValue(not ea.value())
  ca.setValue(not ca.value())

# FIXME expression arrows needs to be a checkmark toggle.
m.addCommand("Expression Arrows", "_internal_expression_arrow_cmd()", "#e", shortcutContext=dagContext)
m.addCommand("Project Settings...", "nuke.showSettings()", "s")

# Workspace menu
m = menubar.addMenu("Workspace")
# FIXME Hide floating viewers needs to be a checkmark toggle.
m.addCommand("Toggle Fullscreen", "nuke.toggleFullscreen()", "#s")
m.addCommand("Toggle Hide Floating Viewers", "nuke.toggleViewers()", "`")
m.addCommand("Show Curve Editor", "nuke.tcl('curve_editor')", "#`")
m.addCommand("-", "", "")
m.addCommand("Next Tab", "nuke.tabNext()", "Ctrl+T")
m.addCommand("Close Tab", "nuke.tabClose()", "Shift+Esc")

# Viewer menu
m = menubar.addMenu("Viewer")
m.addCommand("New Comp Viewer", "nuke.createNode(\"Viewer\")", "^I")
m.addCommand("-", "", "")
n = m.addMenu("Connect to A Side")
n.addCommand("Using Input 1", "nukescripts.connect_selected_to_viewer(0)", "1", shortcutContext=dagContext)
n.addCommand("Using Input 2", "nukescripts.connect_selected_to_viewer(1)", "2", shortcutContext=dagContext)
n.addCommand("Using Input 3", "nukescripts.connect_selected_to_viewer(2)", "3", shortcutContext=dagContext)
n.addCommand("Using Input 4", "nukescripts.connect_selected_to_viewer(3)", "4", shortcutContext=dagContext)
n.addCommand("Using Input 5", "nukescripts.connect_selected_to_viewer(4)", "5", shortcutContext=dagContext)
n.addCommand("Using Input 6", "nukescripts.connect_selected_to_viewer(5)", "6", shortcutContext=dagContext)
n.addCommand("Using Input 7", "nukescripts.connect_selected_to_viewer(6)", "7", shortcutContext=dagContext)
n.addCommand("Using Input 8", "nukescripts.connect_selected_to_viewer(7)", "8", shortcutContext=dagContext)
n.addCommand("Using Input 9", "nukescripts.connect_selected_to_viewer(8)", "9", shortcutContext=dagContext)
n.addCommand("Using Input 10", "nukescripts.connect_selected_to_viewer(9)", "0", shortcutContext=dagContext)
n = m.addMenu("Connect to B Side")
n.addCommand("Using Input 1", "nukescripts.connect_selected_to_viewer(10)", "+1", shortcutContext=dagContext)
n.addCommand("Using Input 2", "nukescripts.connect_selected_to_viewer(11)", "+2", shortcutContext=dagContext)
n.addCommand("Using Input 3", "nukescripts.connect_selected_to_viewer(12)", "+3", shortcutContext=dagContext)
n.addCommand("Using Input 4", "nukescripts.connect_selected_to_viewer(13)", "+4", shortcutContext=dagContext)
n.addCommand("Using Input 5", "nukescripts.connect_selected_to_viewer(14)", "+5", shortcutContext=dagContext)
n.addCommand("Using Input 6", "nukescripts.connect_selected_to_viewer(15)", "+6", shortcutContext=dagContext)
n.addCommand("Using Input 7", "nukescripts.connect_selected_to_viewer(16)", "+7", shortcutContext=dagContext)
n.addCommand("Using Input 8", "nukescripts.connect_selected_to_viewer(17)", "+8", shortcutContext=dagContext)
n.addCommand("Using Input 9", "nukescripts.connect_selected_to_viewer(18)", "+9", shortcutContext=dagContext)
n.addCommand("Using Input 10", "nukescripts.connect_selected_to_viewer(19)", "+0", shortcutContext=dagContext)
n = m.addMenu("View")
n.addCommand("Previous", "nuke.activeViewer().previousView()", ";")
n.addCommand("Next", "nuke.activeViewer().nextView()", "\'")
if not nuke.env['nc']:
  m.addCommand("Toggle Monitor Output", "nukescripts.toggle_monitor_output()", "^u")
m.addCommand("-", "", "")
m.addCommand("Goto Frame...", "nukescripts.goto_frame()", "#g")

# Render menu
m = menubar.addMenu("Render")
m.addCommand("Proxy Mode", "nuke.toNode(\"root\").knob(\"proxy\").setValue(not nuke.toNode(\"root\").knob(\"proxy\").value())", "^p")
m.addCommand("-", "", "")
m.addCommand("Render All Write Nodes...", "nukescripts.showRenderDialog([nuke.root()], False)", "F5")
m.addCommand("Render Selected Write Nodes...", "nukescripts.showRenderDialog(nuke.selectedNodes(), False)", "F7")
m.addCommand("Cancel", "nuke.cancel()", "0xff1b")
m.addCommand("-", "", "")
m.addCommand("Flipbook Selected", "nukescripts.showFlipbookDialogForSelected()", "#F")

# Performance monitor
if nuke.usingPerformanceTimers():
  m = menubar.addMenu("Performance")
  m.addCommand("Clear performance timers", "nuke.resetPerformanceTimers()")
  m.addCommand("Start performance timers", "nuke.startPerformanceTimers()")
  m.addCommand("Stop performance timers", "nuke.stopPerformanceTimers()")

m = menubar.addMenu("Cache")
m.addCommand("Buffer Report", "nuke.display(\"nukescripts.cache_report(str())\", nuke.root(), width = 800)")
m.addCommand("Clear Buffers", "nukescripts.cache_clear(\"\")", "F12")
m.addCommand("Clear Disk Cache", nuke.clearDiskCache)
m.addCommand("Clear Playback Cache", nuke.clearRAMCache)
m.addCommand("Clear All", nukescripts.clearAllCaches )
m.addCommand("-", "", "")


def FnOpenPluginInstaller():

  # TODO: this URL is hardcoded here and in SConscriptConfigureNuke.py; this URL should be made available from a single
  #       location (probably an XML file: see config.xml); alternatively, a script should be used for OSX (see Win/Linux)
  pluginsPageURL = "http://www.thefoundry.co.uk/products/nuke-product-family/nuke/nuke-plugins/"

  # MacOS is special. It needs to be done with open, or the PluginInstaller doesn't get
  # focus. The easiest way to do that is through os.system and calling open. open doesn't block, so that works fine.
  if nuke.env['MACOS']:
    os.system("open \"" + pluginsPageURL + "\"")
    return

  # get Nuke's directory
  path = nuke.env['ExecutablePath']
  path = "/".join(path.split("/")[:-1])
  path += "/PluginInstaller/PluginInstaller"
  if nuke.env['WIN32']:
    path += ".bat"
  path = os.path.normpath(path)

  args = []
  if nuke.env['WIN32']:
    args.append( "\"" + path + "\"" )
  else:
    args.append( path )

  os.spawnv(os.P_NOWAITO, path, args)


# Help menu
m = menubar.addMenu("Help")
if isNukeStudio:
  m.addCommand("Comp Keyboard Shortcuts", "nuke.display(\"nuke.hotkeys()\", None, title = \"Nuke key assignments\")")
else:
  m.addCommand("Keyboard Shortcuts", "nuke.display(\"nuke.hotkeys()\", None, title = \"Nuke key assignments\")")
m.addCommand("-", "", "")
m.addCommand("Documentation", "TopDir = os.path.dirname(nuke.env['ExecutablePath']) + '/';\n\
if nuke.env['MACOS']:\n\
  TopDir = os.path.abspath(TopDir + '../../../') + '/'\n\
nukescripts.start(TopDir + 'Documentation/index.html')")
m.addCommand("Release Notes", "nukescripts.start('http://www.thefoundry.co.uk/products/nuke-product-family/nuke/release-notes/')")
m.addCommand("Training and Tutorials", "nukescripts.start('http://www.thefoundry.co.uk/products/nuke/training')")
m.addCommand("Nukepedia", "nukescripts.start('http://www.nukepedia.com')")
m.addCommand("Mailing Lists", "nukescripts.start('http://support.thefoundry.co.uk/cgi-bin/mailman/listinfo')")
m.addCommand("-", "", "")
m.addCommand("License...", "nuke.licenseInfo()")
m.addCommand("Nuke Plug-ins", "FnOpenPluginInstaller()")

m = nuke.menu("Animation")
m.addCommand("File/Import Ascii...", "nuke.tcl('import_ascii')")
m.addCommand("File/Import Time+value Ascii...", "nuke.tcl('import_discreet')")
m.addCommand("File/Import Discreet LUT...", "nuke.tcl('import_discreet_lut')")
m.addCommand("File/Export Ascii...", "nuke.tcl('export_ascii')", readonly=True)
m.addCommand("File/Export Discreet LUT...", "nuke.tcl('export_discreet_lut')", readonly=True)
m.addCommand("Edit/Generate...", "nuke.tcl('animation_generate')")
m.addCommand("Edit/Move...", "nuke.tcl('animation_move')")
m.addCommand("Edit/Filter", "nuke.tcl('filter_multiple')")
m.addCommand("File/Create Curve", "nukescripts.create_curve()")
m.addCommand("Predefined/Loop", "nukescripts.animation_loop()")
m.addCommand("Predefined/Reverse", "nukescripts.animation_reverse()")
m.addCommand("Predefined/Negate", "nukescripts.animation_negate()")

m = nuke.menu("Axis")
n = m.addMenu("File")
n.addCommand("Import chan file", """nuke.tcl("import_chan_menu [node this]")""")
n.addCommand("Export chan file", """nuke.tcl("export_chan_menu [node this]")""")

n = m.addMenu("Snap")
n.addCommand("Match selection position", "nukescripts.snap3d.translateToPoints(nuke.selectedNode())")
n.addCommand("Match selection position, orientation", "nukescripts.snap3d.translateRotateToPoints(nuke.selectedNode())")
n.addCommand("Match selection position, orientation, size", "nukescripts.snap3d.translateRotateScaleToPoints(nuke.selectedNode())")

del m
del n
del isLinux

################################################################
# non-menu stuff:
#
# The stuff that lives here can't run in render mode or is
# pointless to run in render mode, so this way it only gets run
# if the GUI is starting up.

# Restore the default layout (number 1)
nuke.restoreWindowLayout(1)

# back-compatibility handling of autolabel. Load any autolabel.py we
# find and then register it so nuke.autolabel() calls it. User can
# override this by defining another version somewhere
# earlier in your NUKE_PATH, for instance $HOME/.nuke/menu.py.
from autolabel import autolabel
nuke.addAutolabel(autolabel)

