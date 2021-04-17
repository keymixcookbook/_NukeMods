'''

- return enviroment variable in a VFX Studio enviroment
- Slate variables: SHOW, SCENE, SHOT

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os




#-------------------------------------------------------------------------------
#-Slates
#-------------------------------------------------------------------------------




SLATE = {
	'kuhq':         ['WSLENV','KP_SHOW', 'KP_SCENE', 'KP_SHOT'],
	'mpc':          ['JOB', 'SCENE', 'SHOTNAME'],
	'atomic':       ['JOB', 'SCENE', 'SHOTNAME'],
	'framestore':   ['PL_SHOW', 'PL_SEQ', 'PL_SHOT']
}



#-------------------------------------------------------------------------------
#-Slate
#-------------------------------------------------------------------------------




def LoadSlate():
	'''load slate variables per studio'''

	STUDIO = os.getenv("KU_STUDIO_ENV")

	if STUDIO=='kuhq':
		shell = os.getenv('KP_SHELL')
		if shell=="CMD":
			SHOW    = os.getenv(SLATE[STUDIO][1])
			SCENE   = os.getenv(SLATE[STUDIO][2])
			SHOT    = os.getenv(SLATE[STUDIO][3])
		elif shell==None:
			SHOW, SCENE, SHOT = 'SHOW', 'SCENE', 'SHOT'
		else:
			# Transfer enviroment variable from WSL to Win
			SHOW, SCENE, SHOT = os.getenv(SLATE[STUDIO][0]).split(':')
	else:
		SHOW    = os.getenv(SLATE[STUDIO][0])
		SCENE   = os.getenv(SLATE[STUDIO][1])
		SHOT    = os.getenv(SLATE[STUDIO][2])

	try:
		return {'SHOW': SHOW, 'SCENE': SCENE, 'SHOT': SHOT}
	except:
		return None
