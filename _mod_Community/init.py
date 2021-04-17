'''

Append plugin path from community

'''



#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os
from kplogger import log, col




#-------------------------------------------------------------------------------
#-Selected Modules
#-------------------------------------------------------------------------------




log.info("\033[036m\nfile: %s\033[0m" % os.path.relpath(__file__, os.getenv('KU_PKG_PATH')))

log.info("\033[93m\nInitialize plugins for nuke:\033[0m")

kuDownloadPlugInPath=[
	'_icons/',
    'Cryptomatte/',
    'LineDrawer/',
	'ParticleRenderer'
]

for p in kuDownloadPlugInPath:
    nuke.pluginAddPath(p)
    log.info('--- %s' % p)

log.info("\033[32m\n...DONE\n\033[0m")

