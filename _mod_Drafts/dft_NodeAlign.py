'''

version 0
- Align Nodes with better controls

'''


import nuke, nukescripts




########## Supporting Function ##########








########## Main Function ##########




def alignNodes():

    nodes = nuke.selectedNodes()

    p = nuke.Panel("Align")
    p.addEnumerationPulldown('IN','X-Vertical Y-Horizontal')

    if len( nodes ) < 2:
        return

    if p.show():
        direction = p.value("IN")

        positions = [ float( n[ direction[0].lower()+'pos' ].value() ) for n in nodes]
        avrg = sum( positions ) / len( positions )

        for n in nodes:
            if direction == 'X-Vertical':
                for n in nodes:
                    n.setXpos( int(avrg) )
            else:
                for n in nodes:
                    n.setYpos( int(avrg) )
