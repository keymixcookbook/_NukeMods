# Copyright (c) 2010 The Foundry Visionmongers Ltd.  All Rights Reserved.

import nuke

def setViewsForStereo():
  nuke.root().knob('views').fromScript( '\n'.join( ('left #ff0000', 'right #00ff00') ) )

