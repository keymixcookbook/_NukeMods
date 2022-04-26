'''

Sets the default values for nodes

'''



#-------------------------------------------------------------------------------
#-Module Imports
#-------------------------------------------------------------------------------




import nuke
from _pkg_KuFunc import *
from _pkg_Studios import *
from _mod_Community import *

from _pkg_KuFunc.mod_KuUtility import *




#-------------------------------------------------------------------------------
#-Default Values
#-------------------------------------------------------------------------------




nuke.knobDefault('Blur.size', '12')
nuke.knobDefault('Blur.channels', 'alpha')

nuke.knobDefault('FilterErode.channels', 'alpha')
nuke.knobDefault('FilterErode.filter', 'gaussian')
nuke.knobDefault('Dilate.channels', 'alpha')
nuke.knobDefault('Defocus.channels', 'rgba')

nuke.knobDefault('OFXuk.co.thefoundry.keylight.keylight_v201.show', 'Intermediate Result')

nuke.knobDefault('Denoise.amount','.5')
nuke.knobDefault('Denoise.lumaAmount','4.5')

nuke.knobDefault('Remove.operation', 'keep')
nuke.knobDefault('Remove.channels', 'rgba')
nuke.knobDefault('Remove.label', '[value channels]')

nuke.knobDefault('Switch.which', '1')
nuke.knobDefault('Switch.label', '[value which]')

nuke.knobDefault('Log2Lin1.label', '[value operation]')
nuke.knobDefault('Log2Lin1.operation', 'lin2log')
nuke.knobDefault('OCIOLogConvert.label', '[value operation]')
nuke.knobDefault('OCIOLogConvert.operation', 'lin2log')

nuke.knobDefault('StickyNote.note_font', 'bold')
nuke.knobDefault('StickyNote.note_font_size', '24')

nuke.knobDefault('Multiply.label', '[value value]')
nuke.knobDefault('Expression.label', 'a::[value expr3]')
nuke.knobDefault('Invert.channels', 'alpha')
nuke.knobDefault('IBKColourV3.Size', '1')
nuke.knobDefault('Shuffle.label', '[value in]')
nuke.knobDefault('Roto.cliptype', 'no clip')
nuke.knobDefault('Rotopaint.cliptype', 'no clip')
nuke.knobDefault('Constant.channels', 'rgba')
nuke.knobDefault('Constant.color', '0.18 0.18 0.18 1.0')
nuke.knobDefault('Exposure.mode', 'Stops')

# Viewer Nodes
nuke.knobDefault('Viewer.frame_increment', '8')
nuke.knobDefault('Viewer.hide_input', 'True')




#-------------------------------------------------------------------------------
#-Nuke Startup
#-------------------------------------------------------------------------------




# nuke.addOnUserCreate(function, nodeClass='Class')
# nuke.addOnCreate(mod_StudioENV.StudioENV, nodeClass='Root')

def viewerSetting():
    for n in nuke.allNodes('Viewer'):
        n['frame_increment'].setValue(8)
        n['hide_input'].setValue(True)

nuke.addOnCreate(viewerSetting, nodeClass='Root')


def autolabel_Roto():
    n = nuke.thisNode()
    len_max = 3
    name = n.name()
    label = n['label'].value()
    c = n['curves']
    frame_format = ['all', '-{}', '{}', '{}-', '{}-{}']

    elem = [s for s in c.rootLayer]
    ls_elem_out = []

    for curve in elem:
        name = curve.name
        attr = curve.getAttributes()
        mode = int(attr.getValue(0, 'ltt'))
        fRange = [str(int(attr.getValue(0, 'ltn'))), str(int(attr.getValue(0, 'ltm')))]
        frames = frame_format[mode].format(*fRange)
        ls_elem_out.append('%s %s' % (name, frames))
    elem_out = '\n'.join(ls_elem_out[:len_max])
    if len(ls_elem_out) > len_max: elem_out += '\n...'

    if label == '' or elem_out != "":
        return name+'\n'+elem_out
    else:
        return None

nuke.addAutolabel(autolabel_Roto, nodeClass='Roto')