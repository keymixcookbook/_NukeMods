import nuke
import nukescripts
import os
from Qt import QtGui, QtWidgets, QtCore


mu = nuke.menu('Nuke').addMenu('KUHQ')
mu.addCommand('Sequence Loader', 'studio_kuhq.SequenceLoader()')
mu.addCommand('Write', 'studio_kuhq.kuWrite()','w')
mu.addCommand('Read from Write', 'studio_kuhq.readFromWrite()','alt+w')



def SequenceLoader():
    # source: https://community.foundry.com/discuss/topic/102647/how-can-i-import-all-sequence-images-from-one-folder-and-sub?mode=Post&postID=891904
    '''import aovs exrs as image group
    /<Render>_<Version>/<RenderLayer>/<RenderPasses>/<RenderPasses>_<Version>.%04d.exr
    /TIO_orbit_1k_v001/rs_rsl_car/albeto/albeto_1k_v001.0001.exr
    '''
    dir_renderVersion = nuke.getFilename("Select Render Version") # /Users/Tianlun/Desktop/_NukeTestScript/elems/image_group/TIO_orbit_1k_v001/
    name_renderVersion = os.path.basename(dir_renderVersion[:-1]) # TIO_orbit_1k_v001
    RGBA = 'beauty'


    def createRead(path):
        '''create read from path
        /.../<RenderVersion>/<RenderLayer>/<RenderPasses>/
        /.../TIO_orbit_1k_v001/rs_rsl_car/albeto/
        @path: full path for AOV, str
        return: aov read node, obj
        '''

        exrs = nuke.getFileNameList(path)[0] # ['albedo_1k_v001.####.exr 1-96']
        frames, range = exrs.split(' ')
        first, last = range.split('-')
        first = int(first)
        last = int(last)
        aov = nuke.nodes.Read(
            file=os.path.join(path, frames),
            name=os.path.basename(path),
            first=first,
            last=last,
            label=os.path.basename(path)
            )

        return aov



    def getAOVs(dir_renderVersion):
        '''get renderLayer, then passes
        @path: Render root path (ie. '/TIO_orbit_1k_v001'), str
        return: {<renderLayer>: [<renderPasses>]}
        '''
        ls_aov = {} # {RenderLayer: [RenderPasses, RenderPasses]}
        for l in nuke.getFileNameList(dir_renderVersion):
            thisLayer = [p for p in nuke.getFileNameList(os.path.join(dir_renderVersion, l))]
            ls_aov[l] = thisLayer

        return ls_aov



    def shuffling(node_B, aov_rest):
        '''create ShuffleCopy with changing nodes, then connects output'''
        curB = node_B
        for n in aov_rest:
            thisB = nuke.nodes.ShuffleCopy(
                        inputs=[curB, n],
                        name='in_%s' % n.name(),
                        out = n.name(),
                        red = 'red',
                        green = 'green',
                        blue = 'blue',
                        alpha = 'alpha2'
                        )
            curB = thisB
            print curB.name()
        nuke.nodes.Output(inputs=[curB])



    # Building Image Group
    ls_aov = getAOVs(dir_renderVersion)
    for p in ls_aov[ls_aov.keys()[0]]:
        nuke.Layer(p, ['%s.red' % p, '%s.green' % p, '%s.blue' % p, '%s.alpha' % p])
    nodeLabel = '%s\nv%s' % (name_renderVersion.split('_v')[0], name_renderVersion.split('_v')[1])
    for l in ls_aov.keys():
        imgGroup = nuke.nodes.Group(name=l, label=nodeLabel, postage_stamp=1)
        t_tab = nuke.Tab_Knob('tb_user', 'ku_ImageGroup')
        t_renderVersion = nuke.Text_Knob('tx_version','<b>render: </b>', name_renderVersion)
        t_renderLayer = nuke.Text_Knob('tx_layer','<b>layer: </b>', l)
        t_path = nuke.Text_Knob('tx_dir','<b>path: </b>', dir_renderVersion)
        t_aov = nuke.Text_Knob('tx_aov', '<b>aovs: </b>', '\n'.join(ls_aov[l]))
        for k in [t_tab, t_renderVersion, t_renderLayer, t_path, t_aov]:
            imgGroup.addKnob(k)

        with imgGroup:
            aov_beauty = None
            aov_rest = []
            for p in ls_aov[l]:
                path = os.path.join(dir_renderVersion, l, p)
                createRead(path)
            aov_beauty = nuke.toNode(RGBA)
            aov_rest = [n for n in nuke.allNodes('Read') if n != aov_beauty]
            shuffling(aov_beauty, aov_rest)



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
    out_path = os.path.join(projDir,'EXPORT', scene, out_file, '%s.%s.exr' % (out_file, PADDING_FRAME))
    node['file'].setValue(out_path)
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
        if os.path.exists(out_path):
            nuke.execute(node)
        else:
            os.makedirs(out_path)
            nuke.execute(node)
    else:
        print "user cancelled"


def kuWrite():
    '''Adding inputs for auto generate output path'''

    RENDER_TYPE = ['comp', 'precomp']

    node = nuke.createNode('Write')
    node.setName('KuWrite')
    node.knob('file').setEnabled(False)

    k_pipline = nuke.Text_Knob('kupipline', 'kuWrite', 'kuWrite') # Ku Pipline Identifier

    k_tab = nuke.Tab_Knob('tb_kuWrite', 'kuWrite')
    k_projDir = nuke.File_Knob('fp_proj', 'proj dir')
    k_scene = nuke.String_Knob('tx_scene', 'scene', os.path.basename(nuke.scriptName()).split('_v')[0])
    k_type = nuke.Enumeration_Knob('mu_type', 'type', RENDER_TYPE)
    k_precomp = nuke.String_Knob('tx_precomp', '_', 'NewPass')
    k_ver = nuke.Int_Knob('nm_ver', 'version', 1)
    k_div = nuke.Text_Knob('divider','')
    k_set = nuke.PyScript_Knob('bt_set', '<b>Set Write</b>', 'studio_kuhq.set_settings(nuke.thisNode())')
    k_render = nuke.PyScript_Knob('bt_render', '<b>Render</b>', 'studio_kuhq.render_node(nuke.thisNode())')

    path_proj = os.path.dirname(nuke.script_directory())
    k_projDir.setValue(path_proj)
    k_precomp.clearFlag(nuke.STARTLINE)
    k_precomp.setVisible(False)
    k_ver.setValue(1)
    k_render.clearFlag(nuke.STARTLINE)
    k_pipline.setVisible(False)

    for k in [k_tab, k_pipline, k_projDir, k_scene, k_type, k_precomp, k_ver, k_div, k_set, k_render]:
        node.addKnob(k)

    set_settings(node)



def readFromWrite():
    '''create read from write'''
    for n in nuke.selectedNodes('Read'):
        path = os.path.dirname(n['file'].value())
        exrs = nuke.getFileNameList(path)[0] # ['albedo_1k_v001.####.exr 1-96']
        frames, range = exrs.split(' ')
        first, last = range.split('-')
        first = int(first)
        last = int(last)
        nuke.nodes.Read(
            file=os.path.join(path, frames),
            name=os.path.basename(path),
            first=first,
            last=last,
            label=os.path.basename(path)
            )






########### NUKE KNOB CHANGED ###########




def ku_knobChange():
    '''knob change function to call'''

    n = nuke.thisNode()
    k = nuke.thisKnob()

    if n['kupipline'].value() == 'kuWrite':
        if k.name() in ['tb_kuWrite', 'fp_proj', 'tx_scene','mu_type', 'tx_precomp', 'nm_ver']:
            import studio_kuhq
            studio_kuhq.set_settings(n)

        if k.name() == 'mu_type':
            if n['mu_type'].value() == 'precomp':
                n['tx_precomp'].setVisible(True)
            else:
                n['tx_precomp'].setVisible(False)


nuke.addKnobChanged(ku_knobChange, nodeClass='Write')
