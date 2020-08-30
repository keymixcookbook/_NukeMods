'''

Description of this module

'''


import platform


__VERSION__='0.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__COPYRIGHT__="copyright %s" % __AUTHOR__

__TITLE__=__file__.split('_')[1].split('.')[0]


def _version_():
	ver='''

	version 0.0
    - Features

	'''
	return ver




#------------------------------------------------------------------------------
#-Module Import
#------------------------------------------------------------------------------




import nuke, nukescripts 



#-------------------------------------------------------------------------------
#-Core Class
#-------------------------------------------------------------------------------




