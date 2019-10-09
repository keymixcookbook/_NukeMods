import nuke

def createMetaDatCam( node ):
    '''
    create a camera node from meta data.
    This assumes the following keys in the given nodes meta data stream: 'focal', 'haperture', 'vaperture' and 'matrix',
    where 'matrix' carries the result of "[python nuke.toNode( 'Camera1' ).knob('world_matrix').valueAt( nuke.frame() )]"
    args:
       node  -  node to check for meta data
       ask   -  prompt before creating camera
    '''  
    mDat = node.metadata()
    reqFields = ['exr/nuke/camera/%s' % i for i in ('focal', 'haperture', 'vaperture', 'matrix')]
    if not set( reqFields ).issubset( mDat ):
        print 'no metdata for camera found'
        return

    first = node.firstFrame()
    last = node.lastFrame()
    ret = nuke.getFramesAndViews( 'Create Camera from Metadata', '%s-%s' %( first, last )  )
    fRange = nuke.FrameRange( ret[0] )

    cam = nuke.createNode( 'Camera2' )
    cam['useMatrix'].setValue( True )

    for k in ( 'focal', 'haperture', 'vaperture', 'matrix'):
        cam[k].setAnimated()

    task = nuke.ProgressTask( 'Baking camera from meta data in %s' % node.name() )

    for curTask, frame in enumerate( fRange ):
        if task.isCancelled():
            break
        task.setMessage( 'processing frame %s' % frame )

        # GET ALL FRAMES
        for k in ( 'focal', 'haperture', 'vaperture' ):
            val = float( node.metadata( 'exr/nuke/camera/%s' % k, frame ) )
            cam[ k ].setValueAt(  float( val ), frame )

        # CONVERT STRING BACK TO LIST OBJECT AND ASSIGN
        matrixList = eval( node.metadata('exr/nuke/camera/matrix') )
        for i, v in enumerate( matrixList ):
            cam[ 'matrix' ].setValueAt( v, frame, i)
        # UPDATE PROGRESS BAR
        task.setProgress( int( float(curTask) / fRange.frames() *100) )

