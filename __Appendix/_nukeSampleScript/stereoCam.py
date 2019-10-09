import nuke

def stereoCam( node=None, interoc=.6 ):
    '''
    Create a simple stereo camera or convert an existing one.
    args:
       node - camera node to convert to stereo. if None a camera will be created
       interoc  -  distance between right and left view
    '''
    try:
        node = node or nuke.selectedNode()
    except ValueError:
        # IF NO NODE IS GIVEN AND NOTHING IS SELECTED, CREATE A NEW NODE
        node = nuke.createNode( 'Camera2' )

    # GET SCRIPT SETTIONGS' VIEWS
    views = nuke.views()
    leftView = views[0]
    rightView = views[1]

    # THE OFFSET AS REQUESTED
    rightOffset = float(interoc)/2
    leftOffset = -rightOffset
      
    # THE KNOB TO SPLIT
    if node['useMatrix'].value():
        knob = node['matrix']
        leftEyeMatrix = node['transform'].value() # GETS MATRIX BUT IN REVERSE ORDER
        rightEyeMatrix = nuke.math.Matrix4( leftEyeMatrix ) # COPY MATRIX

        # GET THE NEW VALUES FOR LEFT AND RIGHT EYE
        leftEyeMatrix.translate( leftOffset, 0, 0 ) 
        rightEyeMatrix.translate( rightOffset, 0, 0 )

        # REVERSE FOR ASSIGNMENT
        leftEyeMatrix.transpose()
        rightEyeMatrix.transpose()

        # IF THERE ARE MORE THAN 2 VIEWS MAKE SURE TO SPLIT OFF LEFT VIEW AS WELL
        if len( views ) > 2:
            knob.splitView( leftView )
        knob.splitView( rightView )

        # ASSIGN VALUES
        for i in range(16):
            knob.setValueAt( leftEyeMatrix[i], nuke.frame(), i, leftView )
            knob.setValueAt( rightEyeMatrix[i], nuke.frame(), i, rightView )
    else:
        knob = node['translate']
        # GET THE NEW VALUES FOR LEFT AND RIGHT EYE
        leftEye = knob.value(0) + leftOffset
        rightEye = knob.value(0) + rightOffset

        # IF THERE ARE MORE THAN 2 VIEWS MAKE SURE TO SPLIT OFF LEFT VIEW AS WELL
        if len( views ) > 2:
            knob.splitView( leftView )
        knob.splitView( rightView )
        
        # ASSIGN NEW VALUE
        knob.setValue( leftEye, 0, view=leftView )
        knob.setValue( rightEye, 0, view=rightView )

