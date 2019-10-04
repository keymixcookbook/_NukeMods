import examples
import nuke.rotopaint as rp
import nuke
import threading

def _pointsToKeys( curve, knob, fRange ):
    '''
    Set keys along a shape.
    args:
        shape - CubicCurve to define animation path
        knob - knob to set keys on. This needs to be an Array_Knob
        fRange  - frame range across which to set keys (first frame = start of shape, last frame = end of shape)
    '''
    task = nuke.ProgressTask( 'Shape Tracker' )
    task.setMessage( 'tracking shape' )
    for f in fRange:
        # TAKE CARE OF PROGRESS BAR
        if task.isCancelled():
            nuke.executeInMainThread( nuke.message, args=( "Shape Track Cancelled" ) )
            break
        task.setProgress( int( float(f)/fRange.last() * 100 ) )
        # DO THE WORK
        curPoint = curve.getPoint( float( f )/fRange.last() )
        nuke.executeInMainThreadWithResult( knob.setValueAt, args=(curPoint.x, f, 0) )
        nuke.executeInMainThreadWithResult( knob.setValueAt, args=(curPoint.y, f, 1) )

def trackShape( node=None ):
    '''
    Turn a paint stroke or roto shape into an animation path.
    args:
       node  -  Roto or RotoPaint node that holds the required shape
    '''
    # IF NO NODE IS GIVEN, USE THE CURRENTLY SELECTED NODE
    node = node or nuke.selectedNode()
    
    # BAIL OUT IF THE NODE IS NOT WHAT WE NEED
    if node.Class() not in ('Roto', 'RotoPaint'):
        if nuke.GUI:
            nuke.message( 'Unsupported node type. Node must be of class Roto or RotoPaint' )
        raise TypeError, 'Unsupported node type. Node must be of class Roto or RotoPaint'
    
    # GET  THE KNOB THAT HOLDS ALL THE SHAPES AND POP UP A PANEL THAT LISTS STROKES AND SHAPES (NO LAYERS)
    shPanel = examples.ShapePanel( nuke.selectedNode() )
    if not shPanel.showModalDialog():
        return
    # GET SHAPE OBJECT BY NAME
    shapeName = shPanel.elementKnob.value()
    curveKnob = node['curves']
    shape = curveKnob.toElement( shapeName )
    if isinstance( shape, rp.Stroke ):
        # FOR PAINT STROKES WE JUST EVALUATE AS IS TO GET THE CURVE
        cubicCurve = shape.evaluate( nuke.frame() )
    elif isinstance( shape, rp.Shape ):
        # FOR SHAPES WE EVALUATE INDEX "0" WHICH IS THE MAIN CURVE ("1" WOULD BE THE FEATHER CURVE)
        cubicCurve = shape.evaluate( 0, nuke.frame() )

    # ASK FOR THE DESIRED FRAME RANGE TO DISTRIBUTE THE RESULTING KEYFRAMES OVER
    fRange = nuke.FrameRange( nuke.getInput( 'Track Range', '%s-%s' % ( nuke.root().firstFrame(), nuke.root().lastFrame() ) ) )   
    
    # CREATE A TRACKER NODE TO HOLD THE DATA
    tracker = nuke.createNode( 'Tracker3' )
    tracker['label'].setValue( 'tracking %s in %s' % ( shape.name, node.name() ) )
    t = tracker['track1']
    t.setAnimated()
    threading.Thread( None, _pointsToKeys, args=(cubicCurve, t, fRange) ).start()
