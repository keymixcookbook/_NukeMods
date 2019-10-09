

def nodesFromLayers( node, layer ):
    '''
    Create a RotoPaint node from all elements in a roto paint layer.
    '''
    newNode = nuke.nodes.RotoPaint( label='%s\n%s' % ( node.name(), layer.name ) )
    newRoot = newNode['curves'].rootLayer
    for element in layer:
        if isinstance( element, nuke.rotopaint.Layer ):
            nodesFromLayers( node, element )
        else:
            newCurve = type( element )( newNode['curves'] )
            newCurve
            newRoot.append( newCurve )
            for p in element:
                newCurve.append( p )


#node = nuke.toNode( 'RotoPaint1' )
#root = node['curves'].rootLayer
#nodesFromLayers( node, root )

