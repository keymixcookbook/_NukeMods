import pickle
def getRotoData():
    rpNodes = nuke.allNodes( 'RotoPaint' )
    rpNodes.extend( nuke.allNodes( 'Roto' ) )
    
    rotoData = {}
    knobs = ['curves']
    for n in rpNodes:
        if not n['curves'].rootLayer:
            continue
        knobData = {}
        for k in knobs:
            knobData[ k ] = n[ k ].toScript()
        rotoData[ n.name() ] = knobData
    return rotoData

_firstFrame = True
def metaDatForFirstFrame():
    thisNode = nuke.thisNode()
    global mDatNode
    print nuke.frame()
    global _firstFrame
    if not _firstFrame:
        try:
            nuke.delete( mDatNode )
        except:
            pass
        return

    mDatNode = nuke.nodes.ModifyMetaData( inputs=[ thisNode.input(0) ] )
    thisNode.setInput( 0, mDatNode )
    _firstFrame = False

nuke.removeBeforeFrameRender( metaDatForFirstFrame )
nuke.addBeforeFrameRender( metaDatForFirstFrame )
