'''

menu.py for _NukeStudio
to used in a VFX Studio enviroment

'''


########## MODULE IMPORT ##########




from KuFunc import *
from KuStudio import *
from _pkg_KuFunc import *
from _pkg_KuStudio import *




########## KUFUNC Menubar ##########




kuMu = nuke.menu('Nuke').addMenu('KU')

kuMu.addCommand('Connect Mask Input', "mask()", 'ctrl+Y')
kuMu.addCommand('Change Label', "labelChange()", 'shift+N')
kuMu.addCommand('Linked Postage Stamp', "linkedStamp()", 'F4')
kuMu.addCommand('Group Connect A', "groupConnect()", 'alt+ctrl+Y')
kuMu.addCommand('Set Operation', "mergeOp()", 'alt+o')
kuMu.addCommand('Change Channels', "quickChannel()")
kuMu.addSeparator()
kuMu.addCommand('Reload All Read Nodes', "reloadRead()")
kuMu.addCommand('Reset Node Color', "resetNodeCol()")




########## KUFUNC Toolbar ##########




tBar = nuke.toolbar("T_Bar")

tBar.addCommand('Select Child Nodes', "selectChildNodes()", icon="Output.png")
tBar.addCommand('Align Nodes', "alignNodes()", icon="Posterize.png")
tBar.addCommand('Filter Selection', "filterSelection()", icon="NoOp.png")
tBar.addCommand('Backdrop Resize', "backdropResize()", icon="Distort.png")
tBar.addCommand('KuDrop', "kuDrop()", icon="Backdrop.png")
tBar.addCommand('Dot Cam Connect', "dotCamConnect()", icon="Camera.png")




########## DEFAULT NODE VALUE ##########




nuke.knobDefault('Blur.size', '12')
nuke.knobDefault('Blur.channels', 'alpha')

nuke.knobDefault('FilterErode.channels', 'alpha')
nuke.knobDefault('FilterErode.filter', 'gaussian')

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

### Viewer Node ###
nuke.knobDefault('Viewer.frame_increment', '8')
nuke.knobDefault('Viewer.hide_input', 'True')




########## Custom OnUserCreate ##########




nuke.addOnUserCreate(lambda n=nuke.thisNode(): n['first_frame'].setValue(nuke.frame()), nodeClass='FrameHold')
nuke.addOnUserCreate(lambda n=nuke.thisNode(): n['reference_frame'].setValue(nuke.root()['first_frame'].value()), nodeClass='Tracker4')
