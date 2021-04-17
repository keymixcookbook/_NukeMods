'''

init.py for _NukeStudio
to used in a VFX Studio enviroment

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os
from kplogger import log, col




#-------------------------------------------------------------------------------
#-Module Log
#-------------------------------------------------------------------------------



log.info("\033[036m\nfile: %s\033[0m" % os.path.relpath(__file__, os.getenv('KU_PKG_PATH')))

STUDIO = os.environ['KU_STUDIO_ENV']

log.info("\033[44m\n\n\n>>> Studio set to %s\033[0m" % STUDIO)

log.info("\033[44m\n\n\n>>> Start Install %s\n\n\n\033[0m" % (os.path.basename(os.path.dirname(__file__))))

kuPlugInPath=[
    './_pkg_KuFunc',
    './_pkg_Studios',
    './_mod_Download',
    './__icons',

    './_pkg_Studios/pkgStudio_%s' % STUDIO,
    './_mod_Download/'
    ]

log.info("\033[93m\nAdding kupipeline plugin path\033[0m")

for p in kuPlugInPath:
    nuke.pluginAddPath(p)
    log.info('--- %s' % p)

log.info("\033[32m\n...CONTINUE...\n\033[0m") # Continue to init.py file in _mod_Download
