import nuke
import nukescripts.snap3d

def snapToPointsAnim( node=None, mode='t'):
    '''
    Animated versions of the three default snapping funtions in the axis menu
    args:
       node  -  node to snap
       mode  -  which mode. Available modes are: 't' to match translation, 'tr', to match translation ans rotation, 'trs' to match translation, rotation and scale. default: 't'
    '''

    node = node or nuke.thisNode()
    if mode not in ( 't', 'tr', 'trs' ):
        raise ValueError, 'mode must be "t", "tr" or "trs"'
    
    # KNOB MAP
    knobs = dict( t=['translate'], tr=['translate', 'rotate'], trs=['translate', 'rotate','scaling'] )
    # SNAP FUNCTION MAP
    snapFn = dict( t=nukescripts.snap3d.translateToPoints,
                   tr=nukescripts.snap3d.translateRotateToPoints,
                   trs=nukescripts.snap3d.translateRotateScaleToPoints )

    # SET REQUIRED KNOBS TO BE ANIMATED
    for k in knobs[ mode ]:
        node[ k ].clearAnimated()
        node[ k ].setAnimated()
    
    # GET FRAME RANGE
    fRange = nuke.getInput( 'Frame Range', '%s-%s' % ( nuke.root().firstFrame(), nuke.root().lastFrame() ))
    if not fRange:
        return
    
    # DO THE WORK
    tmp = nuke.nodes.CurveTool() # HACK TO FORCE PROPER UPDATE. THIS SHOULD BE FIXED
    for f in nuke.FrameRange( fRange ):
        nuke.execute( tmp, f, f )
        snapFn[ mode ](node)
    nuke.delete( tmp ) # CLEAN UP THE HACKY BIT
