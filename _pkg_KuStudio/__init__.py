'''

__init__.py for _pkg_KuStudio

'''


import os

dir = os.path.dirname(__file__)
print "\n", "From Package: %s\n\nInstall:" % os.path.basename(dir)

mods = [os.path.splitext(n)[0] for n in os.listdir(dir) if "mod_" in n]
for m in mods:
    
    try:
        pycmd = "from %s import *" % (m)
        eval(pycmd)
        
        print '---', m
    except:
        print 'xxx', m

print "\n...DONE\n"
