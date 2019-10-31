import nuke

def FlickerWaves():
    n = nuke.nodes.NoOp()
    n.setName('ku_FlickerWaves')
    n['note_font'].setValue('Bold')

    # First Tab
    k_tab = nuke.Tab_Knob('tb_main', 'ku_FlickerWaves')

    k_output = nuke.Double_Knob('wave', 'output wave')
    k_global_amp = nuke.Double_Knob('g_amp', 'global amp')
    k_global_freq = nuke.Double_Knob('g_freq', 'global freq')
    k_fade = nuke.Double_Knob('fade','fade')

    k_div1 = nuke.Text_Knob('','')

    k_tx1 = nuke.Text_Knob('','Array Order',"[Base Wave, Mid Wave, High Wave]")
    k_seed = nuke.Array_Knob('seed','seed',3)
    k_amp_ratio = nuke.Array_Knob('amp_ratio','amp ratio',3)
    k_freq_ratio = nuke.Array_Knob('freq_ratio','freq ratio',3)
    k_shift = nuke.Double_Knob('shift','base shift')
    k_timeoffset = nuke.Array_Knob('timeoffset','timeoffset',3)

    k_div2 = nuke.Text_Knob('','')
    k_link = nuke.PyScript_Knob('bt_link','link to selected <b>Multiply</b> node','')
    k_curve = nuke.PyScript_Knob('bt_curve','Show in Curve Editor',"nuke.tcl('curve_editor')")
    k_curve.clearFlag(nuke.STARTLINE)

    # Second Tab
    k_secondary = nuke.Tab_Knob('tb_secondary','Output Waves')

    k_b_out = nuke.Double_Knob('base_freq', 'base freq')
    k_m_out = nuke.Double_Knob('mid_freq', 'mid freq')
    k_h_out = nuke.Double_Knob('high_freq', 'high freq')

    # Set default values
    k_fade.setValue(1)
    k_global_amp.setValue(1)
    k_global_amp.setRange(1,2)
    k_global_freq.setValue(1)
    k_global_freq.setRange(1,2)
    k_seed.setValue([666,888,686])
    k_amp_ratio.setValue([1,0.5,0.25])
    k_freq_ratio.setValue([1,0.5,0.25])
    k_shift.setRange(-1,1)

    ls_knob = [k for k in locals().keys() if k.startwith('k_')]
    for k in ls_knob:
        n.addKnob(k)


    str_expr = '((random({seed},(frame+{timeoffset})*{freq_ratio}*{g_freq}))*{amp_ratio}*{g_amp}+{shift})*{fade}'
    # order-len: seed-3, timeoffset-3, freq_ratio-3, g_freq-1, amp_ratio-3, g_amp-1, shift-3, fade-1

    def va(n,k,i):
        n[k].value()[i]
    def vs(n,k):
        n[k].value()

    n['base_freq'].setExpression(str_expr.format(
        seed=va(n,'seed',0), timeoffset=va(n,'timeoffset',0), freq_ratio=va(n,'freq_ratio',0),
        g_freq=vs(n,'g_freq'), amp_ratio=va(n,'amp_ratio',0),g_amp=vs(n,'freq_ratio',0),
        shift=va(n,'shift',0),fade=vs(n,'fade')
        ))
    n['mid_freq'].setExpression(str_expr.format(
        seed=va(n,'seed',1), timeoffset=va(n,'timeoffset',1), freq_ratio=va(n,'freq_ratio',1),
        g_freq=vs(n,'g_freq'), amp_ratio=va(n,'amp_ratio',1),g_amp=vs(n,'freq_ratio',1),
        shift=va(n,'shift',1),fade=vs(n,'fade')
        ))
    n['high_freq'].setExpression(str_expr.format(
        seed=va(n,'seed',2), timeoffset=va(n,'timeoffset',2), freq_ratio=va(n,'freq_ratio',2),
        g_freq=vs(n,'g_freq'), amp_ratio=va(n,'amp_ratio',2),g_amp=vs(n,'freq_ratio',2),
        shift=va(n,'shift',2),fade=vs(n,'fade')
        ))

    n['wave'].setExpression('base_freq*mid_freq*high_freq')

    py_link = "sel=nuke.selectedNodes('Multiply')\nif sel:\n\tsel['value'].setExpression('%s.wave' % nuke.thisNode().name())\n\tsel['tile_color'].setValue(nuke.thisNode()['tile_color'].value())\nelse:\n\tnuke.message('Select a Multiply node')"
    n['bt_link'].setCommand(py_link)
