'''

menu.py for _NukeStudio
to used in a VFX Studio enviroment

'''




########## MODULE IMPORT ##########




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




########## KuFunc Menubar ##########




kuMu = nuke.menu('Nuke').addMenu('KU')

addMenuItem('f', kuMu, 'Connect Mask Input', "mask()", hotkey="ctrl+Y")
addMenuItem('f', kuMu, 'Change label',"labelChange()", hotkey="shift+N")
addMenuItem('m', kuMu, 'Linked Postage Stamp',"LinkedStamp()", hotkey="f4")
addMenuItem('f', kuMu, 'Group Connect A', "groupConnect()", hotkey="alt+ctrl+Y")
addMenuItem('f', kuMu, 'Set Operation', "mergeOp()", hotkey="alt+O")
addMenuItem('m', kuMu, 'Branching', "Branching()", hotkey="j", shortcutContext=2)
addMenuItem('f', kuMu, 'Cycle through Channels', "cycleChannels()", hotkey="c", shortcutContext=2)
kuMu.addSeparator()
addMenuItem('m', kuMu, 'Set Grain Channels', "GrainChannel()")
addMenuItem('m', kuMu, 'Link Clone', "LinkClone()")
addMenuItem('m', kuMu, 'Find Hidden Inputs', "RestoreHiddenInputs()")
addMenuItem('m', kuMu, 'Scale DAG', "ScaleTree()")
kuMu.addSeparator()
addMenuItem('m', kuMu, '$GUI Switch/switch', "GUISwitch(mode='switch')", hotkey="shift+D")
addMenuItem('m', kuMu, '$GUI Switch/reverse', "GUISwitch(mode='reverse')", hotkey="ctrl+shift+D")




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




########## DEFAULT NODE VALUE ##########




nuke.knobDefault('Blur.size', '12')
nuke.knobDefault('Blur.channels', 'alpha')

nuke.knobDefault('FilterErode.channels', 'alpha')
nuke.knobDefault('FilterErode.filter', 'gaussian')
nuke.knobDefault('Dilate.channels', 'alpha')

nuke.knobDefault('OFXuk.co.thefoundry.keylight.keylight_v201.show', 'Intermediate Result')

nuke.knobDefault('Denoise.amount','.5')
nuke.knobDefault('Denoise.lumaAmount','4.5')

nuke.knobDefault('Remove.operation', 'keep')
nuke.knobDefault('Remove.channels', 'rgba')
nuke.knobDefault('Remove.label', '[value channels]')

nuke.knobDefault('Switch.which', '1')
nuke.knobDefault('Switch.label', '[value which]')

nuke.knobDefault('log2lin2.label', '[value operation]')

nuke.knobDefault('StickyNote.note_font', 'bold')
nuke.knobDefault('StickyNote.note_font_size', '24')

nuke.knobDefault('Multiply.label', '[value value]')
nuke.knobDefault('Expression.label', 'a::[value expr3]')

### Viewer Node ###
nuke.knobDefault('Viewer.frame_increment', '8')
nuke.knobDefault('Viewer.hide_input', 'True')




########## Custom OnUserCreate ##########



# nuke.addOnUserCreate(function, nodeClass='Class')

nuke.addOnCreate(mod_StudioENV.StudioENV, nodeClass='Root')
