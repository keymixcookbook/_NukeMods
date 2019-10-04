import nuke
import nuke.rotopaint as rp

def getKnobRange( knob ):
    '''
    Return a frame range object of the knob's animation range.
    If the knob has no keyframes the script range is returned
    args:
       knob - animated knob
    '''
    allRanges = nuke.FrameRanges()
    for anim in knob.animations():
        if not anim.keys():
            #KNOB ONLY HAS EXPRESSION WITHOUT KEYS SO USE SCRIPT RANGE
            first = nuke.root().firstFrame()
            last = nuke.root().lastFrame()
            allRanges.add( nuke.FrameRange( first, last ) )
        else:
            # GET FIRST FRAME
            allKeys = anim.keys()
            allRanges.add( nuke.FrameRange(  allKeys[0].x, allKeys[-1].x, 1 ) )

    return nuke.FrameRange( allRanges.minFrame(), allRanges.maxFrame(), 1 )


def paintTrajectory( knob, frameRange ):
    '''
    Create a paint stroke that visualises a knob's animation path
    args:
        knob - Array knob with 2 fields. Presumably this is a XY_Knob but can be any
        frameRange - Range for which to draw the trajectory.
                     This is an iterable object containing the requested frames.
                     Default is current script range
    '''
    if knob.arraySize() != 2:
        raise TypeError, 'knob must have array size of 2'

    parentNode = knob.node()
    paintNode = nuke.createNode('RotoPaint')
    curvesKnob = paintNode['curves']

    stroke = rp.Stroke( curvesKnob )
    ctrlPoints = []
    for f in frameRange:
        pos = knob.valueAt( f )
        try :
            # IF PARENT NODE HAS "CENTER" KNOB ADD THE OFFSET TO LINE UP STROKE PROPERLY
            offset = parentNode['center'].valueAt( f )
        except NameError:
            # OTHERWISE NO OFFSET IS APPLIED
            offset = ( 0, 0 )
        finalPos = [ sum(p) for p in zip( pos, offset ) ]
        stroke.append( rp.AnimControlPoint( *finalPos ) )

    stroke.name = 'trajectory for %s.%s' % ( parentNode.name(), knob.name() )
    curvesKnob.rootLayer.append( stroke )
