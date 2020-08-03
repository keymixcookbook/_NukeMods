kuDownloadPlugInPath=[
	'_icons/',
    'Cryptomatte/',
    'LineDrawer/',
	'ParticleRenderer'
]

for p in kuDownloadPlugInPath:
    nuke.pluginAddPath(p)
    print '--- %s' % p
