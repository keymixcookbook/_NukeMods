'''
!!! Replace 'TEMPLATE' to studio name (all lowercase) when setting up !!!
'''


'''

__init__.py for studio_TEMPLATE

'''

# Change this to package name
__STUDIO__='TEMPLATE'

import os

dir = os.path.dirname(__file__)
print "\n", "From Package: %s\n\nInstall:" % os.path.basename(dir)

mods = [os.path.splitext(n)[0] for n in os.listdir(dir) if __STUDIO__ in n and '.pyc' not in n]
__all__ = ['menu']

for m in mods:

    __all__.append(m)
    print '---', m

print "\n...DONE\n"
