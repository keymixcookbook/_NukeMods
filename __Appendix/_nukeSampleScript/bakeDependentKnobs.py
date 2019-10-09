import nuke

def bakeCurve( curve, first, last, inc ):
    '''bake an expresison curve into a keyframes curve'''
    for f in xrange( first, last, inc ):
        curve.setKey( f, curve.evaluate( f ) )
    curve.setExpression( 'curve' )

####################################################
def getCurves( knob, views ):
    '''return a list of all animation curves found in the given knob'''
    curves = []
    for v in views:
        curves.extend( knob.animations( v ) )
    return curves

####################################################
def bakeExpressionKnobs( node, first, last, inc, views ):  
    '''bake all knobs in node that carry expressions'''
    # GET ALL KNOBS WITH EXPRESSIONS IN THEM
    expKnobs = [ k for k in node.knobs().values() if k.hasExpression() ]

    # GET ALL CURVES INSIDE THAT KNOB INCLUDING SPLIT FIELDS AND VIEWS
    allCurves = []
    for k in expKnobs:
        allCurves += getCurves( k, views )

    # BAKE ALL CURVES
    for c in allCurves:
        bakeCurve( c, first, last, inc )

####################################################
def bakeDependentNodes():
    '''Add this to onUserDestroy callback - not yet implemented'''
    parentNode = nuke.thisNode() # THIS IS GIVEN TO US BY THE CALLBACK, i.e. WHEN A NODE IS DELETED - WELL, NOT YET
    depNodes  = parentNode.dependent( nuke.EXPRESSIONS )
    
    ret = nuke.getFramesAndViews( 'bake curves in dependent nodes?', '%s-%s' % (parentNode.firstFrame(), parentNode.lastFrame()) )
    if not ret:
        return
    fRange = nuke.FrameRange( ret[0] )
    views = ret[1]

    for n in depNodes:
        bakeExpressionKnobs( n, fRange.first(), fRange.last(), fRange.increment(), views )
        

####################################################
def bakeSelectedNodes():
    '''bake selected nodes' knobs that carry expressions'''
    ret = nuke.getFramesAndViews( 'bake curves in selected nodes?', '%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()) )
    if not ret:
        return
    fRange = nuke.FrameRange( ret[0] )
    views = ret[1]

    for n in nuke.selectedNodes():
        bakeExpressionKnobs( n, fRange.first(), fRange.last(), fRange.increment(), views )
