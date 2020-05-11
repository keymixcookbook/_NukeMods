'''

- return enviroment variable in a VFX Studio enviroment
- Slate variables: SHOW, SCENE, SHOT

'''




import os, nuke

# Load pkgStudio modules
#STUDIO = os.getenv("KU_STUDIO_ENV")
#__import__('pkgStudio_%s' % STUDIO, globals=globals())

def LoadSlate():
    '''load slate variables per studio'''

    SLATE = {
        'kuhq':         ['WSLENV','KP_SHOW', 'KP_SCENE', 'KP_SHOT'],
        'mpc':          ['JOB', 'SCENE', 'SHOTNAME'],
        'atomic':       ['JOB', 'SCENE', 'SHOTNAME'],
        'framestore':   ['PL_SHOW', 'PL_SEQ', 'PL_SHOT']
    }

    STUDIO = os.getenv("KU_STUDIO_ENV")

    if STUDIO=='kuhq':
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
