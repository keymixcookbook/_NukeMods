pathDict = {}

shape = nuke.toNode('Roto1')['curves'].toElement( 'Bezier1' )
shapeDict = dict( label=shape.name )
for cp in shape:
    # SHAPE CONTROL POINT LEVEL
    print '\n%s' % cp
    centre = cp.center
    leftTan = cp.leftTangent
    rightTan = cp.rightTangent
    pathDict = dict( closed=True, interp='linear' )
    keyDict = {}
    posList = []
    for p in ( centre, leftTan, rightTan ): # MATCH ORDER IN SILHOUETTE!
        # ANIM CONTROL POINT LEVEL
        print '\t%s' % p
        for k in p.getControlPointKeyTimes():
            # KEYFRAME LEVEL
            pos = p.getPosition( k )
            posList.append( ( pos.x, pos.y ) )
            keyDict['frame'] = k
            try:
                keyDict['pathData'].append( (pos.x, pos.y) )            
            except KeyError:
                keyDict['pathData'] = [ (pos.x, pos.y) ]
            print '\t\t%s:  %s' % ( k, pos )
    print '>>> %s\n\n' % posList
