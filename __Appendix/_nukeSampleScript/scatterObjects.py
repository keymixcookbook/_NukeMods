import nuke
import nukescripts  
   
def scatterObjects():
    '''
    Places an object on each selected vertex. The new Scene node gets user knobs to control the new objects.
    args:
        obj  -  class of object to scatter (default = Card2)
    '''
    # pop up a panel to ask for the desired object type
    # the dictionary maps the name in the panel to the actual class used
    typeDict = dict( Axis='Axis', Card='Card2', Sphere='Sphere', Cylinder='Cylinder', Cube='Cube' )
    
    # create the initial panel and give it a title
    p = nuke.Panel( 'Pick object type to scatter' )
    
    # add a drop down list with the dictionary's keys as choices
    p.addEnumerationPulldown( 'object', ' '.join( typeDict.keys() ) )
    
    # adjust the panel's width a bit
    p.setWidth( 250 )
    
    # if the user confirms the dialogsave the choice for later, otherwise do nothing
    if p.show():
        objType = typeDict[ p.value( 'object' ) ]
    else:
        return
    
    
    vsel = nukescripts.snap3d.getSelection()
    sc = nuke.nodes.Scene()
    # add user knobs to control new nodes:
    offsetKnob = nuke.XYZ_Knob( 'offset' )
    sc.addKnob( offsetKnob )
    scaleKnob = nuke.Double_Knob( 'scale' )
    scaleKnob.setValue( 1 )
    sc.addKnob( scaleKnob )

    for i, v in enumerate( vsel ):
        obj = eval( 'nuke.nodes.%s()' % objType )
        # assign expressions to link to scene node's user knobs
        obj['translate'].setExpression( '%s + %s.offset' % ( v.position.x, sc.name() ), 0 )
        obj['translate'].setExpression( '%s + %s.offset' % ( v.position.y, sc.name() ), 1 ) 
        obj['translate'].setExpression( '%s + %s.offset' % ( v.position.z, sc.name() ), 2 ) 
        obj['uniform_scale'].setExpression( '%s.scale' % sc.name() ) 
        sc.setInput( i, obj)

    sc.setInput( i+1, nuke.thisNode() )
    nuke.connectViewer( 1, sc )



