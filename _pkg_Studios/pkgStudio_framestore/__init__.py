'''

__init__.py for studio_framestore # <- change to package name

'''


import os
# Change this to package name
__STUDIO__='framestore'

dir = os.path.dirname(__file__)
print "\n", "From Package: %s\n\nInstall:" % os.path.basename(dir)

mods = [os.path.splitext(n)[0] for n in os.listdir(dir) if __STUDIO__ in n and '.pyc' not in n]
__all__ = ['menu']

for m in mods:

    __all__.append(m)
    print '---', m

print "\n...DONE\n"
