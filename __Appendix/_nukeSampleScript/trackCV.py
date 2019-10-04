import examples
import nuke
import nukescripts
import threading

def _cvTracker( node, shapeName, cvID, fRange ):
    shape = node['curves'].toElement( shapeName )
   
    # SHAPE CONTROL POINT
    try:
        shapePoint = shape[cvID]
    except IndexError:
        nuke.message( 'Index %s not found in %s.%s' % (  ) )
        return

    # ANIM CONTROL POINT
    animPoint = shapePoint.center   
        
    # CREATE A TRACKER NODE TO HOLD THE DATA
    tracker = nuke.createNode( 'Tracker3' )
    tracker['label'].setValue( 'tracking cv#%s in %s.%s' % ( cvID, node.name(), shape.name ) )
    trackerKnob = tracker['track1']
    trackerKnob.setAnimated()    
    
    # SET UP PROGRESS BAR
    task = nuke.ProgressTask( 'CV Tracker' )
    task.setMessage( 'tracking CV' )
    
    # DO THE WORK
    for f in fRange:
        if task.isCancelled():
            nuke.executeInMainThread( nuke.message, args=( "CV Track Cancelled" ) )
            break
        task.setProgress( int( float(f)/fRange.last() * 100 ) )
        
        # GET POSITION
        pos = animPoint.getPosition( f )
        nuke.executeInMainThreadWithResult( trackerKnob.setValueAt, args=( pos.x, f, 0 ) ) # SET X VALUE
        nuke.executeInMainThreadWithResult( trackerKnob.setValueAt, args=( pos.y, f, 1 ) ) # SET Y VALUE

def trackCV():
    # GET THE SELECTED NODE. SINCE WE PLAN ON CALLING THIS FROM THE PROPERTIES MENU
    # WE CAN BE SURE THAT THE SELECTED NODE IS ALWAYS THE ONE THE USER CLICKED IN
    node = nuke.selectedNode()
    
    # BAIL OUT IF THE NODE IS NOT WHAT WE NEED
    if node.Class() not in ('Roto', 'RotoPaint'):
        nuke.message( 'Unsupported node type. Node must be of class Roto or RotoPaint' )
        return
   
    p = examples.ShapeAndCVPanel( node )
    if p.showModalDialog():
        fRange = nuke.FrameRange( p.fRange.value() )
        shapeName = p.shape.value()
        cv = p.cv.value()
        threading.Thread( None, _cvTracker, args=(node, shapeName, cv, fRange) ).start()
