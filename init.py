'''

init.py for _NukeStudio
to used in a VFX Studio enviroment

'''




########## PLUGIN DIRECTORIES ##########




import os

print ">>>", "Start Install %s" % (os.path.basename(os.path.dirname(__file__))), "<<<"

nuke.pluginAddPath('./_pkg_KuFunc')
nuke.pluginAddPath('./_pkg_KuStudio')
nuke.pluginAddPath('./_mod_Download')
