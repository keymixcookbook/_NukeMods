import nuke
import nukescripts
import nuke.rotopaint as rp

class ShapeAndCVPanel( nukescripts.PythonPanel ):
    def __init__( self, node ):
        nukescripts.PythonPanel.__init__( self, 'Get Shape and CV index' )
        self.rpNode  = node
        # GET THE NODES ROOT LAYER AND COLLECT ALL SHAPES IN IT
        root = node['curves'].rootLayer
        shapeNames = [ c.name for c in root if isinstance( c, rp.Shape ) ]
        if not shapeNames:
            nuke.message( 'No Shapes found in %s' % node.name() )
            return
        # CREATE KOBS
        self.fRange = nuke.String_Knob( 'fRange', 'Track Range', '%s-%s' % ( nuke.root().firstFrame(), nuke.root().lastFrame() ) )        
        self.shape = nuke.Enumeration_Knob( 'shape', 'Shape', shapeNames )
        self.cv = nuke.Int_Knob( 'pointNumber', 'Point Number' )
        self.warning = nuke.Text_Knob( 'warning', '<span style="color:red">invalid index</span>' )
        self.warning.clearFlag( nuke.STARTLINE )
        self.warning.setVisible( False )

        # ADD KOBS
        for k in ( self.fRange, self.shape, self.cv, self.warning ):
            self.addKnob( k )

    def knobChanged( self, knob ):
        # IF AN INVALID INDEX IS SHOWN DISPLAY THE WARNING TEXT
        if knob in( self.cv, self.shape ):
            currentShape = self.rpNode['curves'].toElement( self.shape.value() )
            size = len( [pt for pt in currentShape] )
            validNumber = -1 < knob.value() < size
            self.warning.setVisible( not validNumber )
