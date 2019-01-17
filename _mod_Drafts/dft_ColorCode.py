'''

- Adding Color Scheme selection buttons for groups:
- Groups include: CG, Plate, Grade, Key, Despill, Output, 2D Elem, Ref, End Comp, Lens FX

'''



import nuke, nukescripts

def ColorCode(mode='create'):

    '''
    mode: create, build
    '''

    # Symbols and Color
    blk = '&#9608;'
    #hex_group = {'CG': ['CCC0C0','5C3737','7D5F5F'], 'Plate', 'Grade', 'Key', 'Despill', 'Output', 'Elem', 'Ref', 'EndComp', 'LensFX'}
    hex_group = {'CG': ['CCC0C0','5C3737','7D5F5F'], 'Plate': ['BFC5CC', '2E405C', '58667d'], 'Grade': ['C0CCCC' ,'2E5C5C' ,'587d7d']}

    # Main Functions
    if mode == 'create':
        nodes = nuke.selectedNodes()
    if mode == 'build':
        nodes = nuke.selectedNodes('BackdropNode')

    if not nodes:
        nuke.message("Select Nodes to")
    elif mode == 'create':

        bd = nukescripts.autoBackdrop()

        ## Inherit from:
        ## (https://github.com/mb0rt/Nuke-NodeHelpers/blob/master/mbort/backdrop_palette/backdrop.py)

        # Create Knobs

        # Tab
        tab = nuke.Tab_Knob( 'Backdrop+ColorCode' )

        # Label
        label_link = nuke.Link_Knob( 'label_link', 'label' )
        label_link.makeLink( bd.name(), 'label' )

        # Font
        font_link = nuke.Link_Knob( 'note_font_link', 'font' )
        font_link.makeLink( bd.name(), 'note_font' )

        # Font Size
        font_size_link = nuke.Link_Knob( 'note_font_size_link', '' )
        font_size_link.makeLink( bd.name(), 'note_font_size' )
        font_size_link.clearFlag( nuke.STARTLINE )
        
        # font Color
        font_color_link = nuke.Link_Knob( 'note_font_color_link', '' )
        font_color_link.makeLink( bd.name(), 'note_font_color' )
        font_color_link.clearFlag( nuke.STARTLINE )

        # Divider
        k_div = nuke.Text_Knob('')

        # add Tab
        bd.addKnob( tab )

        # Color Code
        counter = 0

        for t in hex_group.keys():

            name = "bt_%s" % (t)
            label = "<font size='+1' color='#%s'>%s</font> <b>%s" % (hex_group[t][2], blk, t)
            cmd = "n=nuke.thisNode();\
                    n['tile_color'].setValue(int('%sFF',16));\
                    n['note_font_color'].setValue(int('%sFF', 16));\
                    n['note_font'].setValue('bold')" % (hex_group[t][1], hex_group[t][0])


            cc_knob = nuke.PyScript_Knob(name,label,cmd)
            cc_knob.setTooltip(t)

            # If First Item
            if counter == 0:
                cc_knob.clearFlag(nuke.STARTLINE)

            bd.addKnob(cc_knob)

            counter += 1


        # Add Knobs
        bd.addKnob( k_div )
        bd.addKnob( label_link )
        bd.addKnob( font_link )
        bd.addKnob( font_size_link )
