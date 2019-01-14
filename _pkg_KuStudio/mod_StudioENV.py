'''

- return enviroment variable in a VFX Studio enviroment

'''

import os


def StudioENV():

    STUDIO = os.getenv("KU_STUDIO_ENV")

    if STUDIO == "MPC": # Hub
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')

    elif STUDIO == "Atomic": # Shotgun
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')


    return {'SHOW': SHOW, 'SCENE': SCENE, 'SHOT': SHOT}
