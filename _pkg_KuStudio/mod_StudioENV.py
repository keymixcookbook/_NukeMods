'''

- return enviroment variable in a VFX Studio enviroment

'''

import os, nuke


def StudioENV():

    STUDIO = os.getenv("KU_STUDIO_ENV")

    if STUDIO == 'KUHQ': # Home Studio
        nuke.root()['format'].setValue('HD_1080')
        nuke.root()['first_frame'].setValue(1001)
        nuke.root()['last_frame'].setValue(1010)
        nuke.root()['lock_range'].setValue(True)
        print "Enviroment set to %s" % STUDIO

    elif STUDIO == "MPC": # Hub
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')
        print "Enviroment set to %s" % STUDIO

    elif STUDIO == "Atomic": # Shotgun
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')
        print "Enviroment set to %s" % STUDIO


    try:
        return {'SHOW': SHOW, 'SCENE': SCENE, 'SHOT': SHOT}
    except:
        return None
