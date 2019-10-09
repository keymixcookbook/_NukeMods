import examples
import nuke

def shuffleLayer( node, layer ):
    '''
    Shuffle a given layer into rgba
    args:
       node  - node to attach a Shuffle node to
       layer - layer to shuffle into rgba
    '''
    shuffleNode = nuke.nodes.Shuffle( label=layer, inputs=[node] )
    shuffleNode['in'].setValue( layer )
    shuffleNode['postage_stamp'].setValue( True )
    return nuke.nodes.Dot( inputs=[ shuffleNode ] )

def autoComp( node ):
    channels = node.channels()
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    # CREATE SIMPLE PANEL TO MAP THE BUFFERS
    p = nuke.Panel( 'Map AOVs' )
    p.addEnumerationPulldown( 'texture', ' '.join( layers ) )
    p.addEnumerationPulldown( 'diffuse', ' '.join( layers ) )
    p.addEnumerationPulldown( 'specular', ' '.join( layers ) )
    p.addEnumerationPulldown( 'depth', ' '.join( channels ) )
    p.addBooleanCheckBox( 'normalise depth', True)
    p.addBooleanCheckBox( 'invert depth', False )
    if not p.show():
        return
    # STORE PANEL RESULt IN VARIABLES FOR EASE OF USE
    texture = p.value( 'texture' )
    diffuse = p.value( 'diffuse' )
    spec = p.value( 'specular' )
    depth = p.value( 'depth' )
    normZ = p.value( 'normalise depth' )
    invertZ = p.value( 'invert depth' )
    # CREATE SHUFFLE NODES
    texNode = shuffleLayer( node, texture )
    diffNode = shuffleLayer( node, diffuse )
    specNode = shuffleLayer( node, spec )
    
    mergeDiff = nuke.nodes.Merge2( operation='multiply', inputs=[ texNode, nuke.nodes.Multiply( inputs=[diffNode] ) ], output='rgb' )
    result = nuke.nodes.Merge2( operation='plus', inputs=[ mergeDiff, nuke.nodes.Multiply( inputs=[specNode] ) ], output='rgb' )
    
    if normZ:
        black, white = examples.getMinMax( node, depth )
        result = nuke.nodes.Grade( channels=depth, blackpoint=black, whitepoint=white, white_clamp=True, label='normalise depth', inputs=[result] )
    if invertZ:
        result = nuke.nodes.Invert( channels=depth, inputs=[result] )
    
    g = nuke.nodes.Grade( inputs=[result] ) 
    g['black'].setValue( 0.05 )
    g['mask'].setValue( depth )
    
