import nuke
import nukescripts
import os
from Qt import QtGui, QtWidgets, QtCore
from pkgStudio_kuhq import *


mu = nuke.menu('Nuke').addMenu('KUHQ')
mu.addCommand('Sequence Loader', 'mod_SequenceLoader.SequenceLoader()')
mu.addCommand('Write', 'mod_KuWrite.KuWrite()','w')
mu.addCommand('Read from Write', 'menu.readFromWrite()','alt+w')



def readFromWrite():
    '''create read from write'''
    for n in nuke.selectedNodes('Read'):
        path = os.path.dirname(n['file'].value())
        exrs = nuke.getFileNameList(path)[0] # ['albedo_1k_v001.####.exr 1-96']
        frames, range = exrs.split(' ')
        first, last = range.split('-')
        first = int(first)
        last = int(last)
        nuke.nodes.Read(
            file=os.path.join(path, frames),
            name=os.path.basename(path),
            first=first,
            last=last,
            label=os.path.basename(path)
            )
