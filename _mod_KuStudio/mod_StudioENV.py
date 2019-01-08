'''

- return enviroment variable in a VFX Studio enviroment

'''

import os


def StudioENV(studio="MPC"):

    if studio == "MPC":
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')

    elif studio == "Atomic":
        SHOW = os.getenv('JOB')
        SCENE = os.getenv('SCENE')
        SHOT = os.getenv('SHOTNAME')


    return SHOW, SCENE, SHOT
