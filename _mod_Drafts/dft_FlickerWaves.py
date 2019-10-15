import nuke

n = nuke.nodes.NoOp(name='ku_FlickerWaves')

k_tab = nuke.Tab_Knob('tb_main', 'ku_FlickerWaves')

k_output = nuke.Double_Knob('wave', 'output wave')
k_fade = nuke.Double_Knob('fade','fade')

k_div1 = nuke.Text_Knob('','')

k_tx1 = nuke.Text_Knob('','Array Order',"[Base Wave, Mid Wave, High Wave]")
k_seed = nuke.Array_Knob('seed','seed',3)
k_freq_ratio = nuke.Array_Knob('freq_ratio','freq ratio',3)
k_timeoffset = nuke.Array_Knob('timeoffset','timeoffset',3)

k_div2 = nuke.Text_Knob('','')

k_amp = nuke.Array_Knob('amp','amp',3)
k_freq = nuke.Array_Knob('freq','freq',3)
k_shift = nuke.Array_Knob('shift','base shift',3)

k_div3 = nuke.Tab_Knob('','Output Waves')

k_b_out = nuke.Double_Knob('base_wave', 'base freq')
k_m_out = nuke.Double_Knob('mid_wave', 'mid freq')
k_h_out = nuke.Double_Knob('high_wave', 'high freq')

k_fade.setValue(1)
k_seed.setValue([666,888,686])
k_freq_ratio.setValue([1,0.5,0.25])
k_amp.setValue([1,1,1])
k_freq.setValue([1,1,1])

ls_knob = [
k_tab,k_output,k_fade,k_div1,
k_tx1,k_seed,k_freq_ratio,k_timeoffset,k_div2,
k_amp,k_freq,k_shift,k_div3,
k_b_out,k_m_out,k_h_out
]

for k in ls_knob:
    n.addKnob(k)
