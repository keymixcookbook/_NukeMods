'''

file to parse slate variables

'''



from mod_StudioLoad import LoadSlate
import json, os
from kputl import *




slate = LoadSlate()
SHOW = slate['SHOW']
SCENE = slate['SCENE']
SHOT = slate['SHOT']
print('%s:%s:%s' % (SHOW, SCENE, SHOT))


SHOW_ROOT_DIR = r'k:/PROJECTS/Personal/'
SHOW_DIR = joinPath(SHOW_ROOT_DIR, SHOW)
SHOT_DIR = joinPath(SHOW_DIR, SHOT)
SHOW_CONFIG_FILE = joinPath(SHOW_DIR, '_configShow.json')
SHOT_CONFIG_FILE = joinPath(SHOT_DIR, '_configShot.json')

RENDER_DIR = joinPath(SHOT_DIR, 'render/')
ELEMENTS_DIR = joinPath(SHOT_DIR, 'assets', 'elements/')
DELIVERY_DIR = joinPath(SHOW_DIR, '_delivery/')
SHOW_TOOL_DIR = joinPath(SHOW_DIR, 'showtools/')

NUKE_DIR = joinPath(SHOW_DIR, 'workbench', 'nuke/')
MAYA_DIR = joinPath(SHOW_DIR, 'workbench', 'maya/scenes/')
BLENDER_DIR = joinPath(SHOW_DIR, 'workbench', 'blender/')
PS_DIR = joinPath(SHOW_DIR, 'workbench', 'ps/')
AE_DIR = joinPath(SHOW_DIR, 'workbench', 'ae/')

SHOW_CONFIG, SHOT_CONFIG = None, None
try:
    with open(SHOW_CONFIG_FILE, 'r') as f:
        SHOW_CONFIG = json.load(f)
    with open(SHOT_CONFIG_FILE, 'r') as f:
        SHOT_CONFIG = json.load(f)
except:
    print("No show/shot config file found ")
