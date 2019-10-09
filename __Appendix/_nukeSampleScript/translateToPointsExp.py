import nuke
import nukescripts.snap3d

def snapToPointsExp( node ):
    '''put expressions into node's translate knob to glue it to the average position of the current vertex selection over time'''
    expX = '[python nukescripts.snap3d.calcAveragePosition( nukescripts.snap3d.getSelection() ).x]'
    expY = '[python nukescripts.snap3d.calcAveragePosition( nukescripts.snap3d.getSelection() ).y]'
    expZ = '[python nukescripts.snap3d.calcAveragePosition( nukescripts.snap3d.getSelection() ).z]'
    
    knob = node['translate']
    knob.setExpression( expX, 0 )
    knob.setExpression( expY, 1 )
    knob.setExpression( expZ, 2 )