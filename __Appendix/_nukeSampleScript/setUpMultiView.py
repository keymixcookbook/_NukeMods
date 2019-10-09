import nuke

def setUpMultiView( views=[ ('left',(0,1,0)), ('right',(1,0,0) ) ] ):
    '''
    set up the nuke project with an arbitrary amount of colour coded views
    args:
       views  -  nested list with view names and rgb tuples for each view. rgb values are assumed to be normalise, eg red = (1,0,0)
    '''
    newViews = []
    for v in views:   # CYCLE THROUGH EACH REQUESTED VIEW
        name = v[0]   # GRAB THE CURRENT VIEWS NAME
        col = v[1]    # GRAB THE CURRENT VIEWS COLOUR
        rgb = tuple( [ int(v*255) for v in col ] ) #CONVERT FLOAT TO 8BIT INT AND RETURN A TUPLE
        hexCol = '#%02x%02x%02x' % rgb             #CONVERT INTEGER NUMBERS TO HEX CODE
        curView = '%s %s' % ( name, hexCol )       #COMBINE NAME AND HEX COLOUR TO SCRIPT SYNTAX
        newViews.append( curView )      # COLLECT ALL REQUESTED VIEWS

    # COMBINE ALL VIEWS WITH LINE BREAK AND INITIALISE THE VIEWS KNOB WITH THE RESULTING SCRIPT SYNTAX
    nuke.root().knob('views').fromScript( '\n'.join( newViews ) )
