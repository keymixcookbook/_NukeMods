import nuke

n = nuke.nodes.NoOp(name='ku_FlickerWaves')

k_tab = nuke.Tab_Knob('tb_main', 'ku_FlickerWaves')

k_output = nuke.Double_Knob('wave', 'wave')
k_fade = nuke.Double_Knob('fade','fade')

k_div1 = nuke.Text_Knob('','')

k_seed = nuke.Array_Knob('seed','seed',3)
k_freq_ratio = nuke.Array_Knob('freq_ratio','frequency ratio',3)
k_timeoffset = nuke.Array_Knob('timeoffset','timeoffset',3)

k_div2 = nuke.Text_Knob('','')

k_b_amp = nuke.Double_Knob('base_amp','base amplitude')
k_m_amp = nuke.Double_Knob('mid_amp','mid amplitude')
k_h_amp = nuke.Double_Knob('high_amp','high amplitude')

k_b_freq = nuke.Double_Knob('base_freq','base freq')
k_m_freq = nuke.Double_Knob('mid_freq','mid freq')
k_h_freq = nuke.Double_Knob('high_freq','high freq')

k_b_shift = nuke.Double_Knob('base_shift','base amp shift')
k_m_shift = nuke.Double_Knob('mid_shift','mid amp shift')
k_h_shift = nuke.Double_Knob('high_shift','high amp shift')

k_div3 = nuke.Text_Knob('','')

k_b_out = nuke.Double_Knob('base_wave', 'base freq wave')
k_m_out = nuke.Double_Knob('mid_wave', 'mid freq wave')
k_h_out = nuke.Double_Knob('high_wave' 'high freq wave')


ls_knob = [
k_tab,k_output,k_fade,k_div1,
k_seed,k_freq_ratio,k_timeoffset,
k_b_amp,k_m_amp,k_h_amp,
k_b_freq,k_m_freq,k_h_freq,
k_b_shift,k_m_shift,k_h_shift
]

for k in ls_knob:
    n.addKnob(k)
