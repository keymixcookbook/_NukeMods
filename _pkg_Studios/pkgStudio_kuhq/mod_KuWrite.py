import nuke, nukescripts, os



#------------------------------------------------------------------------------
#-Supporting Function
#------------------------------------------------------------------------------



def set_settings(node):
    '''setting export element settings'''
    PADDING_VER = 3
    PADDING_FRAME = '%04d'
    projDir = node['fp_proj'].value()
    scene = node['tx_scene'].value()
    out_type = node['mu_type'].value()
    ver = int(node['nm_ver'].value())

    if out_type == 'comp':
        out_file = '%s_%s_v%s' % (scene, out_type, str(ver).zfill(PADDING_VER))
    elif out_type == 'precomp':
        out_file = '%s_%s_%s_v%s' % (scene, out_type, node['tx_precomp'].value(), str(ver).zfill(PADDING_VER))

    out_path = os.path.join(projDir,'render', out_file, '%s.%s.exr' % (out_file, PADDING_FRAME))

    node['file'].setValue(out_path.replace('\\', '/'))
    ch = 'rgb' if out_type == 'comp' else 'all'
    node['channels'].setValue(ch)

    print "==========\n\n%s\n\n%s-%s\n\n==========" % (
    out_file, nuke.Root()['first_frame'].value(), nuke.Root()['last_frame'].value()
    )



def render_node(node):
    '''launch render'''
    out_path = node['file'].value()
    askMessage = "Render Node: %s\nFile: %s\nFramerage: %s-%s\n" % (
    node.name(), os.path.basename(node['file'].value()), nuke.Root()['first_frame'].value(), nuke.Root()['last_frame'].value()
    )
    c = nuke.ask(askMessage)
    if c:
        if os.path.exists(os.path.dirname(out_path)):
            nuke.execute(node)
        else:
            os.makedirs(os.path.dirname(out_path))
            nuke.execute(node)
    else:
        print "user cancelled"



#------------------------------------------------------------------------------
#-Main Function
#------------------------------------------------------------------------------



def KuWrite():
    '''Adding inputs for auto generate output path'''

    RENDER_TYPE = ['comp', 'precomp', 'lookdev']

    node = nuke.createNode('Write')
    node.setName('KuWrite')
    node.knob('file').setEnabled(False)

    k_pipeline = nuke.Text_Knob('kupipeline', 'kuWrite', 'kuWrite') # Ku Pipeline Identifier

    k_tab = nuke.Tab_Knob('tb_KuWrite', 'KuWrite')
    k_projDir = nuke.File_Knob('fp_proj', 'proj dir')
    k_scene = nuke.String_Knob('tx_scene', 'scene', os.path.basename(nuke.scriptName()).split('_v')[0])
    k_type = nuke.Enumeration_Knob('mu_type', 'type', RENDER_TYPE)
    k_precomp = nuke.String_Knob('tx_precomp', '_', 'NewPass')
    k_ver = nuke.Int_Knob('nm_ver', 'version', 1)
    k_div = nuke.Text_Knob('divider','')
    k_set = nuke.PyScript_Knob('bt_set', '<b>Set Write</b>', 'mod_KuWrite.set_settings(nuke.thisNode())')
    k_render = nuke.PyScript_Knob('bt_render', '<b>Render</b>', 'mod_KuWrite.render_node(nuke.thisNode())')

    path_proj = os.path.dirname(os.path.dirname(nuke.script_directory()))
    k_projDir.setValue(path_proj)
    k_precomp.clearFlag(nuke.STARTLINE)
    k_precomp.setVisible(False)
    k_ver.setValue(1)
    k_render.clearFlag(nuke.STARTLINE)
    k_pipeline.setVisible(False)

    for k in [k_tab, k_pipeline, k_projDir, k_scene, k_type, k_precomp, k_ver, k_div, k_set, k_render]:
        node.addKnob(k)

    set_settings(node)




########### NUKE KNOB CHANGED ###########




def ku_knobChange():
    '''knob change function to call'''

    n = nuke.thisNode()
    k = nuke.thisKnob()

    if n['kupipeline'].value() == 'kuWrite':
        if k.name() in ['tb_kuWrite', 'fp_proj', 'tx_scene','mu_type', 'tx_precomp', 'nm_ver']:
            import mod_KuWrite
            mod_KuWrite.set_settings(n)

        if k.name() == 'mu_type':
            if n['mu_type'].value() == 'precomp':
                n['tx_precomp'].setVisible(True)
            else:
                n['tx_precomp'].setVisible(False)


nuke.addKnobChanged(ku_knobChange, nodeClass='Write')
