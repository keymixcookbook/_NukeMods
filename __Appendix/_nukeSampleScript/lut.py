import nuke

def getLUT( size=1024 ):
    '''
    Get the current viewer process node and generate a simple lut from it
    args:
       size  -  size of resulting lut (default=1024)
    '''
    vpNode = nuke.ViewerProcess.node()
    vp = eval( 'nuke.nodes.%s()' % vpNode.Class() )
    _copyKnobsFromScriptToScript( vpNode, vp )

    ramp = nuke.nodes.Ramp()
    ramp['p0'].setValue( (0, 0) )
    ramp['p1'].setValue( (size, 0) )

    vp.setInput(0, ramp )

    saturation = nuke.nodes.Saturation( saturation = 0 )
    saturation.setInput(0, vp )   
    lut = [ saturation.sample("rgba.red", i+.5, 0.5) for i in xrange( 0, size )]

    nuke.delete( saturation )
    nuke.delete( ramp )
    nuke.delete( vp )

    return lut

def createLutNode( lut ):
    '''
    Create a ColorLookup node to hold lut. The values are normalised.
    args:
        lut  -  list of floating point numbers
    '''
    lutNode = nuke.createNode( 'ColorLookup' )
    lutKnob = lutNode['lut']
    for i, y in enumerate( lut ):
        x = float(i) / len(lut) 
        lutKnob.setValueAt( y, x )

def _copyKnobsFromScriptToScript( srcNode, trgNode):
    '''
    Copy knobs between nodes.
    This function can also be found in the default menu.py
    args:
       srcNode  -  node to copy values from
       trgNode  -  node to copy values to
    '''
    srcKnobs = srcNode.knobs()
    trgKnobs = trgNode.knobs()
    excludedKnobs = ["name", "xpos", "ypos"]
    intersection = dict([ (item, srcKnobs[ item ]) for item in srcKnobs.keys() if item not in excludedKnobs and trgKnobs.has_key( item ) ])
    for k in intersection.keys():
        trgNode[ k ].fromScript( srcNode[ k ].toScript() )