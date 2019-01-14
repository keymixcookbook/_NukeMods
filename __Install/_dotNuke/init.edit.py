'''

init.py for './nuke' with external Package
Remove '.edit' in filename when installed

'''




########## PLUGIN DIRECTORIES ##########


import os

# Set ENV Variables, to change when installed
os.environ['KU_PKG_PATH'] = "/Users/Tianlun/Documents/GitHub/_NukeStudio"
os.environ['KU_STUDIO_ENV'] = "MPC"

# Install Package
nuke.pluginAddPath(os.getenv('KU_PKG_PATH'))
