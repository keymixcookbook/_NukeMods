import nuke
from _pkg_KuFunc import *
from _pkg_KuStudio import *
from _mod_Download import *

from _pkg_KuFunc.mod_KuUtility import *
from _pkg_KuStudio.mod_KuStudio import *




########## AddMenuItem Func ##########




def addMenuItem(type, mu, name, mod, hotkey="", icon="", shortcutContext=1):

    '''
    type: 'm'= modules, 'f' = functions
    mu: menu variable
    mod: module/function name
    hotkey: ctl, alt, shift + letter
    icon: image file name + ext
    '''

    if type == 'm':
        mu.addCommand(name, "mod_{mod}.{func}".format(mod=mod.split('(')[0],func=mod), hotkey, icon=icon, shortcutContext=shortcutContext)
    elif type == 'f':
        mu.addCommand(name, "{func}".format(func=mod), hotkey, icon=icon, shortcutContext=shortcutContext)
    elif type == 'c':
        mu.addCommand(name, "mod_{cls}.{cls}.run()".format(cls=mod), hotkey, icon=icon, shortcutContext=shortcutContext)




########## KuFunc Menubar ##########




kuMu = nuke.menu('Nuke').addMenu('KU')

addMenuItem('f', kuMu, 'Connect Mask Input', "mask()", hotkey="ctrl+Y")
addMenuItem('c', kuMu, 'Change label',"SetLabel", hotkey="shift+N")
addMenuItem('m', kuMu, 'Linked Postage Stamp/set',"LinkedStamp()", hotkey="f4")
addMenuItem('m', kuMu, 'Linked Postage Stamp/reconnect',"LinkedStamp(mode='reconnect')", hotkey="shift+f4")
addMenuItem('f', kuMu, 'Group Connect A', "groupConnect()", hotkey="alt+ctrl+Y")
addMenuItem('f', kuMu, 'Set Operation', "mergeOp()", hotkey="alt+O")
addMenuItem('m', kuMu, 'Branching', "Branching()", hotkey="j", shortcutContext=2)
addMenuItem('m', kuMu, 'Cycling/regular', "Cycling(mode='regular')", hotkey="c", shortcutContext=2)
addMenuItem('m', kuMu, 'Cycling/all channels', "Cycling(mode='all')", hotkey="shift+c", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/>', "setSize(0.25)", hotkey="alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<', "setSize(-0.25)", hotkey="alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/>>', "setSize(0.5)", hotkey="shift+alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<<', "setSize(-0.5)", hotkey="shift+alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'Launch Selection in RV', "launchRV()", hotkey="f2")
addMenuItem('c', kuMu, 'Expression', "ExprPrompt", hotkey="e", shortcutContext=2)
addMenuItem('m', kuMu, 'Tracked Roto', "TrackedRoto()", hotkey="shift-t", shortcutContext=2)
addMenuItem('f', kuMu, 'Disable', "disable()", hotkey="d", shortcutContext=1)
kuMu.addSeparator()
addMenuItem('m', kuMu, 'Set Grain Channels', "GrainChannel()")
addMenuItem('m', kuMu, 'Link Clone', "LinkClone()")
addMenuItem('m', kuMu, 'Find Hidden Inputs', "RestoreHiddenInputs()")
addMenuItem('m', kuMu, 'Scale DAG', "ScaleTree()")
kuMu.addSeparator()
addMenuItem('m', kuMu, '$GUI Switch/switch', "GUISwitch(mode='switch')", hotkey="shift+D")
addMenuItem('m', kuMu, '$GUI Switch/reverse', "GUISwitch(mode='reverse')", hotkey="ctrl+shift+D")
kuMu.addSeparator()
kuMu.addCommand('Shuffle', "nuke.createNode('Shuffle')", "h", shortcutContext=2)




########## KuFunc Toolbar ##########




tBar = nuke.toolbar("T_Bar")

addMenuItem('f', tBar, 'Select Child Nodes',"selectChildNodes()", icon="Output.png")
tBar.addMenu('Align Nodes', icon="align_menu.png")
addMenuItem('m', tBar, 'Align Nodes/top', "AlignNodes('up')", icon="align_T.png")
addMenuItem('m', tBar, 'Align Nodes/bottom', "AlignNodes('down')", icon="align_B.png")
addMenuItem('m', tBar, 'Align Nodes/left', "AlignNodes('left')", icon="align_L.png")
addMenuItem('m', tBar, 'Align Nodes/right', "AlignNodes('right')", icon="align_R.png")
addMenuItem('f', tBar, 'Filter Selection', "filterSelection()", icon="NoOp.png")
addMenuItem('m', tBar, 'Backdrop Resize', "BackdropResize()", icon="BackdropResize.png")
addMenuItem('m', tBar, 'KuDrop', "ColorCode()", icon="Backdrop.png")
addMenuItem('m', tBar, 'Dot Cam Connect', "DotCamConnect()", icon="Camera.png")
addMenuItem('m', tBar, 'Roto AutoLife', "autolife()", icon="Roto.png")
addMenuItem('f', tBar, 'Stack IBK', "stackIBK()", icon="IBKColour.png")
tBar.addMenu('DeepCollect', icon="DeepMerge.png")
addMenuItem('m', tBar, 'DeepCollect/Collector', "DeepCollect()", icon="")
addMenuItem('m', tBar, 'DeepCollect/Set Markers', "DeepCollect(mode='markers')", icon="")
tBar.addSeparator()
tBar.addCommand('ClearAllCache', "nukescripts.clearAllCaches()", "shift+f12", icon="DiskCache.png", shortcutContext=1)
addMenuItem('f', tBar, 'Show IP', "showIPPanel()", icon="Viewer.png")




########## 3rd Party Menus ###########




# Nuke Tab alternative
#m_tab = nuke.menu("Nuke").findItem("Edit")
#m_tab.addCommand("Tabtabtab", mod_Tabtabtab.main, "Tab")

tN = nuke.menu('Nuke').findItem('KU')
tN.addCommand('Turbo/TurboCopy', 'mod_TurboMerge.turboCopy.open()', '', shortcutContext=2)
tN.addCommand('Turbo/TurboShuffle', 'mod_TurboMerge.turboShuffle.open()', '', shortcutContext=2)
tN.addCommand('Turbo/TurboMerge', 'mod_TurboMerge.turboMerge.open()', 'm', shortcutContext=2)
