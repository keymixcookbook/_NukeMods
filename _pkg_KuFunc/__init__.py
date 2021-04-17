'''

__init__.py for _pkg_KuFunc

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os
from kplogger import log, col




#-------------------------------------------------------------------------------
#-Logging Module Contents
#-------------------------------------------------------------------------------



log.info("\033[036m\nfile: %s\033[0m" % os.path.relpath(__file__, os.getenv('KU_PKG_PATH')))

dir = os.path.dirname(__file__)
log.info("\033[93m\nFrom Package: %s\n\nLoad:\033[0m" % os.path.basename(dir))

mods = [os.path.splitext(n)[0] for n in os.listdir(dir) if 'mod_' in n and '.pyc' not in n and 'upt_' not in n]
__all__ = []

for m in mods:

    __all__.append(m)
    log.info('--- %s' % m)

log.info("\033[32m\n...DONE\n\033[0m")
