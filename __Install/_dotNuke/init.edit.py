'''

init.py for './nuke' with external Package
Remove '.edit' in filename when installed

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os




#-------------------------------------------------------------------------------
#-Functions
#-------------------------------------------------------------------------------




# Set ENV Variables, to change when installed
os.environ['KU_PKG_PATH'] = "URL/TO/PACKAGE/"
os.environ['KU_STUDIO_ENV'] = "STUDIONAME"

print("\n")
print("Comfirm Package location: %s" % os.getenv('KU_PKG_PATH'))
print("\n")

# Install Package
nuke.pluginAddPath(os.getenv('KU_PKG_PATH'))
