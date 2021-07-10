'''

Selective Modules to load from Community

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os
from kplogger import log, col




#-------------------------------------------------------------------------------
#-Selected Modules
#-------------------------------------------------------------------------------




mods = [
	'mod_autolife',
	'mod_AlignNodes',
	'mod_ScaleTree',
	# 'mod_Tabtabtab',
	'knob_scripter',
	# 'mod_TurboMerge'
]

__all__ = []




#-------------------------------------------------------------------------------
#-Logging Module Contents
#-------------------------------------------------------------------------------



log.info("\033[036m\nfile: %s\033[0m" % os.path.relpath(__file__, os.getenv('KU_PKG_PATH')))

dir = os.path.dirname(__file__)
log.info("\033[93m\nFrom Package: %s\n\nLoad:\033[0m" % os.path.basename(dir))

for m in mods:

    __all__.append(m)
    log.info('--- %s' % m)

log.info("\033[32m\n...DONE\n\033[0m")