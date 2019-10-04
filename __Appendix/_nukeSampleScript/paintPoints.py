import nuke
import nukescripts

def paintPoints():
    '''
    Rather experimental but kinda fun. This projects sleected 3D points through a camera ito screen space
    and draws a dot for each using a paint stroke.
    '''
    # GET THE GEO NODE FROM THE CURRENTLY ACTIVE VIEWER
    geoNode = nuke.activeViewer().node()   

    # WE EXPECT A CAMERA TO BE SELECTED
    camera = nuke.selectedNode()
    if not camera.Class() in ( 'Camera', 'Camera2' ):
        nuke.message( 'Please select a camera node first')
        return

    # COLLECT ALL OBJECTS IN THE CURRENT GEO KNOB. QUIT IFNONE WERE FOUND
    geoKnob = geoNode['geo']
    objs = geoKnob.getGeometry()
    if not objs:
        nuke.message( 'No geometry found in %s' % geoNode.name() )

    pts = []
    for o in objs:
        # CYCLE THROUGH ALL OBJECTS
        objTransform = o.transform()
        for p in o.points():
            # CYCLE THROUGH ALL POINTS OF CURRENT OBJECT
            worldP = objTransform * nuke.math.Vector4(p.x, p.y, p.z, 1)
            pts.append( [worldP.x, worldP.y, worldP.z] )

    # CREATE THE NODE THAT WILL HOLD THE PAINT STROKES
    curvesKnob = nuke.createNode( 'RotoPaint' )['curves']
    # PREP THE TASK BAR
    task  = nuke.ProgressTask( 'painting points' )
    
    for i, pt in enumerate( pts ):
        if task.isCancelled():
            break
        task.setMessage( 'painting point %s' % i )
        # CREATE A NEW STROKE
        stroke = nuke.rotopaint.Stroke( curvesKnob )
        # PROJECT THE POINT TO SCREEN SPACE
        pos = nukescripts.snap3d.projectPoint( camera, pt )
        # CREATE ANE CONTROL POINT FOR
        ctrlPoint = nuke.rotopaint.AnimControlPoint( pos )
        # ASSIGN IT TO THE STROKE
        stroke.append( ctrlPoint )
        # ASSIGN TH E STROKE TO THE ROOT LAYER
        curvesKnob.rootLayer.append( stroke )
        # UPDARE PROGRESS BAR
        task.setProgress( int( float(i)/len(pts)*100 ) )
