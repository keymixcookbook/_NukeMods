import nuke
import nukescripts

class AdjustScatterObjects( nukescripts.PythonPanel ):
    def __init__( self, nodes ):
        '''
        Adjust nodes' position and scale
        args:
            nodes -  list of nodes to control. nodes in thi list have to have a 3D transform knob
        '''
        nukescripts.PythonPanel.__init__( self, 'Adjust Scattered Objects' )
        self.nodes = nodes
        self.origPos = dict( [ ( n, n['translate'].value() ) for n in nodes ] )
        self.offset = nuke.XYZ_Knob( 'offset', 'offset' )
        self.scale = nuke.Double_Knob( 'uniform_scale', 'uniform scale' )
        self.scale.setValue( 1 )
        self.addKnob( self.offset )
        self.addKnob( self.scale )

    def knobChanged( self, knob ):
        if knob == self.scale:
            for n in self.nodes:
                n['uniform_scale'].setValue( knob.value() )
        else:
            for n in self.nodes:
                n['translate'].setValue( [sum(value) for value in zip( self.origPos[n], self.offset.value() )] )