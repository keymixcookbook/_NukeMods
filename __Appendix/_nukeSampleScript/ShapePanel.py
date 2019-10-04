import nuke
import nukescripts

class ShapePanel( nukescripts.PythonPanel ):
    def __init__( self, node ):
        '''List all roto paint nodes and the name of their respective shapes and strokes'''
        nukescripts.PythonPanel.__init__( self, 'RotoPaint Elements' )
        self.rpNode = node
        # CREATE KNOBS
        self.typeKnob = nuke.Enumeration_Knob( 'element', 'element / curve', ['Shapes', 'Strokes'] )
        self.elementKnob = nuke.Enumeration_Knob( 'curve', '', [] )
        self.elementKnob.clearFlag( nuke.STARTLINE )
        # ADD KNOBS
        for k in ( self.typeKnob, self.elementKnob ):
            self.addKnob( k )

        # STORE DICTIONARY OF ELEMENTS PER TYPE
        self.curveDict = {}
        # FILL DICTIONARY
        self.getData()

    def getData( self ):
        '''return a nested dictionary of all shapes and strokes per node'''
        self.curveDict={ 'Shapes':[], 'Strokes':[] }
        rootLayer = self.rpNode['curves'].rootLayer
        for e in rootLayer:
            if isinstance( e, nuke.rotopaint.Shape ):
                self.curveDict[ 'Shapes' ].append( e.name )
            elif isinstance( e, nuke.rotopaint.Stroke ):
                self.curveDict[ 'Strokes' ].append( e.name )


    def knobChanged( self, knob ):
        if knob is self.typeKnob or knob.name()=='showPanel':
            self.elementKnob.setValues( self.curveDict[ self.typeKnob.value() ] )
