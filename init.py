'''

init.py for _NukeStudio
to used in a VFX Studio enviroment

'''





import os

STUDIO = os.environ['KU_STUDIO_ENV']
print "\n\n\n==========\nStudio set to %s\n==========" % STUDIO

print "\n\n\n>>>", "Start Install %s" % (os.path.basename(os.path.dirname(__file__))), "<<<\n\n\n"

kuPlugInPath=[
    './_pkg_KuFunc',
    './_pkg_Studios',
    './_mod_Download',
    './__icons',

    './_pkg_Studios/pkgStudio_%s' % STUDIO,
    './_mod_Download/'
    ]

print "Adding kupipeline plugin path"
for p in kuPlugInPath:
    nuke.pluginAddPath(p)
    print '--- %s' % p
