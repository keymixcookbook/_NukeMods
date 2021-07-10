'''

alias file for importing Workbench Manger Package
for nuke environment use

url: D:/Dropbox/REPOSITORIES/_kptools/pkgMod_WorkbenchManager/

'''



#------------------------------------------------------------------------------
#-Import Modules
#------------------------------------------------------------------------------




import os
import sys
import nuke, nukescripts



#------------------------------------------------------------------------------
#-Setup modules
#------------------------------------------------------------------------------



nuke.pluginAddPath(r'D:/Dropbox/REPOSITORIES/_kptools/')
os.environ['KP_GUI'] = 'nuke'
from pkgMod_WorkbenchManager import mod_PanelSave

# PanelSave = mod_PanelSave.Core_PanelSave()
# PanelSave.run()
