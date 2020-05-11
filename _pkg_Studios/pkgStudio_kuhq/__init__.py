'''

__init__.py for pkgStudio_kuhq

'''


import os
# Change this to package name

dir = os.path.dirname(__file__)
print "\n", "From Package: %s\n\nInstall:" % os.path.basename(dir)

mods = [os.path.splitext(n)[0] for n in os.listdir(dir) if 'mod_' in n and '.pyc' not in n]
__all__ = []

for m in mods:

    __all__.append(m)
    print '---', m

print "\n...DONE\n"
