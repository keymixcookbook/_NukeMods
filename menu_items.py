'''

Master Menu items

'''




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke
from _pkg_KuFunc import *
from _pkg_Studios import *
from _mod_Community import *

from _pkg_KuFunc.mod_KuUtility import *




#------------------------------------------------------------------------------
#-Header
#------------------------------------------------------------------------------




__OS__			= platform.system()
__AUTHOR__		= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)




#-------------------------------------------------------------------------------
#-Menu Item Functions for KuPipeline
#-------------------------------------------------------------------------------




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




#-------------------------------------------------------------------------------
#-KuFunc Menubar
#-------------------------------------------------------------------------------




kuMu = nuke.menu('Nuke').addMenu('KU')

addMenuItem('c', kuMu, 'Change label',"SetLabel", hotkey="shift+N", shortcutContext=2)
addMenuItem('c', kuMu, 'Expression', "ExprPrompt", hotkey="e", shortcutContext=2)
addMenuItem('c', kuMu, 'HoverValue', "HoverValue", hotkey="alt+v", shortcutContext=0)
addMenuItem('c', kuMu, 'QuickNode', "QuickNode", hotkey="alt+q", shortcutContext=2)
kuMu.addSeparator()
addMenuItem('m', kuMu, 'Linked Postage Stamp/set',"LinkedStamp()", hotkey="f4")
addMenuItem('m', kuMu, 'Linked Postage Stamp/reconnect',"LinkedStamp(mode='reconnect')", hotkey="meta+f4")
addMenuItem('m', kuMu, 'Linked Postage Stamp/marking (manually)',"LinkedStamp(mode='marking')", hotkey="")
# addMenuItem('f', kuMu, 'Set Operation', "mergeOp()", hotkey="alt+O")
addMenuItem('m', kuMu, 'Branching', "Branching()", hotkey="j", shortcutContext=2)
addMenuItem('m', kuMu, 'Cycling/regular', "Cycling(mode='regular')", hotkey="c", shortcutContext=2)
addMenuItem('m', kuMu, 'Cycling/all channels', "Cycling(mode='all')", hotkey="shift+c", shortcutContext=2)
addMenuItem('m', kuMu, 'Tracked Roto', "TrackedRoto()", hotkey="shift+t", shortcutContext=2)
addMenuItem('m', kuMu, 'Set Grain Channels', "GrainChannel()")
addMenuItem('m', kuMu, 'Link Clone', "LinkClone()")
addMenuItem('m', kuMu, 'Find Hidden Inputs', "RestoreHiddenInputs()")
addMenuItem('m', kuMu, 'Scale DAG', "ScaleTree()")
addMenuItem('m', kuMu, 'Create IP', "IP()", hotkey="")
kuMu.addSeparator()
addMenuItem('f', kuMu, '$GUI Switch/switch', "guiSwitch(mode='switch')", hotkey="shift+D")
addMenuItem('f', kuMu, '$GUI Switch/reverse', "guiSwitch(mode='reverse')", hotkey="ctrl+shift+D")
addMenuItem('f', kuMu, 'Connect Mask Input', "mask()", hotkey="ctrl+Y")
addMenuItem('f', kuMu, 'Group Connect A', "groupConnect()", hotkey="alt+ctrl+Y")
addMenuItem('f', kuMu, 'SetVal/>', "setSize(0.25)", hotkey="alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<', "setSize(-0.25)", hotkey="alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/>>', "setSize(0.5)", hotkey="shift+alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<<', "setSize(-0.5)", hotkey="shift+alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'Launch Selection in RV', "launchRV()", hotkey="f2")
addMenuItem('f', kuMu, 'Disable', "disable()", hotkey="d", shortcutContext=1)
kuMu.addSeparator()
kuMu.addCommand('Shuffle', "nuke.createNode('Shuffle')", "h", shortcutContext=2)




#-------------------------------------------------------------------------------
#-KuFunc Toolbar
#-------------------------------------------------------------------------------




tBar = nuke.toolbar("T_Bar")

addMenuItem('f', tBar, 'Select Child Nodes',"selectChildNodes()", icon="Output.png")
addMenuItem('m', tBar, 'AOVContactSheet',"AOVContactSheet()", icon="ContactSheet.png")
tBar.addMenu('Align Nodes', icon="align_menu.png")
addMenuItem('m', tBar, 'Align Nodes/top', "AlignNodes('up')", icon="align_T.png")
addMenuItem('m', tBar, 'Align Nodes/bottom', "AlignNodes('down')", icon="align_B.png")
addMenuItem('m', tBar, 'Align Nodes/left', "AlignNodes('left')", icon="align_L.png")
addMenuItem('m', tBar, 'Align Nodes/right', "AlignNodes('right')", icon="align_R.png")
addMenuItem('f', tBar, 'Filter Selection', "filterSelection()", icon="NoOp.png")
addMenuItem('m', tBar, 'Backdrop Resize', "BackdropResize()", icon="BackdropResize.png")
addMenuItem('c', tBar, 'Keyframing', "Keyframing", icon="Paint.png")
addMenuItem('c', tBar, 'KuDrop', "ColorCode", icon="Backdrop.png")
addMenuItem('m', tBar, 'Dot Cam Connect', "DotCamConnect()", icon="Camera.png")
addMenuItem('m', tBar, 'Roto AutoLife', "autolife()", icon="Roto.png")
addMenuItem('f', tBar, 'Stack IBK', "stackIBK()", icon="IBKColour.png")
tBar.addMenu('DeepCollect', icon="DeepMerge.png")
addMenuItem('m', tBar, 'DeepCollect/Collector', "DeepCollect()", icon="")
addMenuItem('m', tBar, 'DeepCollect/Set Markers', "DeepCollect(mode='markers')", icon="")
tBar.addSeparator()
tBar.addCommand('ClearAllCache', "nukescripts.clearAllCaches()", "shift+f12", icon="DiskCache.png", shortcutContext=1)
addMenuItem('f', tBar, 'Show IP', "showIPPanel()", icon="Viewer.png")




#-------------------------------------------------------------------------------
#-Context Menus
#-------------------------------------------------------------------------------




nuke.menu('Viewer').addCommand('Viewer Restore', "mod_KuUtility.setViewer(mode='restore')", "alt+v", index=0, shortcutContext=0)
nuke.menu('Viewer').addCommand('Viewer Set', "mod_KuUtility.setViewer(mode='set')", index=1, shortcutContext=0)




#-------------------------------------------------------------------------------
#-Community Module Menus
#-------------------------------------------------------------------------------




# Nuke Tab alternative
#m_tab = nuke.menu("Nuke").findItem("Edit")
#m_tab.addCommand("Tabtabtab", mod_Tabtabtab.main, "Tab")

tN = nuke.menu('Nuke').findItem('KU')
tN.addCommand('Turbo/TurboCopy', 'mod_TurboMerge.turboCopy.open()', '', shortcutContext=2)
tN.addCommand('Turbo/TurboShuffle', 'mod_TurboMerge.turboShuffle.open()', '', shortcutContext=2)
tN.addCommand('Turbo/TurboMerge', 'mod_TurboMerge.turboMerge.open()', 'alt+m', shortcutContext=2)


mvs = nuke.menu('Viewer').addMenu("QuickCreate", icon="ROI.png") # <--- BUG HERE FOUNDRY!, this icon will be replaced by the first in the sub menu
mvs.addCommand( '-> ROI', 'mod_ViewerShortcuts.CreateOnSelection("ROI")',icon='ROI.png') #Luckily we have added the same icon for the first item =)
# mvs.addCommand( '-> Cornerpin (From)', 'mod_ViewerShortcuts.CreateOnSelection("CornerpinFrom")',icon='CornerPin.png')
# mvs.addCommand( '-> Cornerpin (To)', 'mod_ViewerShortcuts.CreateOnSelection("CornerpinTo")',icon='CornerPin.png')
# mvs.addCommand( '-> Cornerpin (From and To)', 'mod_ViewerShortcuts.CreateOnSelection("CornerpinFromTo")',icon='CornerPin.png')
# mvs.addCommand( '-> Crop', 'mod_ViewerShortcuts.CreateOnSelection("Crop")',icon='Crop.png')
# mvs.addCommand( '-> GridWarp', 'mod_ViewerShortcuts.CreateOnSelection("GridWarp")',icon='GridWarp.png')
# mvs.addCommand( '-> Keylight', 'mod_ViewerShortcuts.CreateOnSelection("Keylight")',icon='Keylight.png')
# mvs.addCommand( '-> Radial', 'mod_ViewerShortcuts.CreateOnSelection("Radial")',icon='Radial.png')
# mvs.addCommand( '-> Text', 'mod_ViewerShortcuts.CreateOnSelection("Text")',icon='Text.png')
mvs.addCommand( '-> Tracker', 'mod_ViewerShortcuts.CreateOnSelection("Tracker")',icon='Tracker.png')
# mvs.addCommand( '-> Transform', 'mod_ViewerShortcuts.CreateOnSelection("Transform")',icon='2D.png')
mvs.addCommand( '-> Constent', 'mod_ViewerShortcuts.CreateOnSelection("Constant")',icon='Sampler.png')
