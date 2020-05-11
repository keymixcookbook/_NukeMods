'''
# source: https://community.foundry.com/discuss/topic/102647/how-can-i-import-all-sequence-images-from-one-folder-and-sub?mode=Post&postID=891904
import aovs exrs as image group
/<Render>_<Version>/<RenderLayer>/<RenderPasses>/<RenderPasses>_<Version>.%04d.exr
/TIO_orbit_1k_v001/rs_rsl_car/albeto/albeto_1k_v001.0001.exr
'''



import nuke, os




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
        file=os.path.join(path, frames).replace('\\','/'),
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




def getLightingPath():
    '''get lighting render dir from kupipeline'''
    import mod_StudioLoad

    SHOW=mod_StudioLoad.LoadSlate()['SHOW']
    SHOT=mod_StudioLoad.LoadSlate()['SHOT']
    path=os.path.join('K:/PROJECTS/Personal/', SHOW, SHOT, 'assets', 'lighting')

    return path



#------------------------------------------------------------------------------
#-Main function
#-----------------------------------------------------------------------------



def SequenceLoader():
    '''main function'''

    dir_renderVersion = nuke.getFilename("Select Render Version", pattern='*/', default=getLightingPath()) # /Users/Tianlun/Desktop/_NukeTestScript/elems/image_group/TIO_orbit_1k_v001/
    if dir_renderVersion == None:
        nuke.message("Import Canceled")
    else:
        name_renderVersion = os.path.basename(dir_renderVersion[:-1]) # TIO_orbit_1k_v001
        RGBA = 'beauty'

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
                    createRead(path.replace('\\', '/'))
                aov_beauty = nuke.toNode(RGBA)
                aov_rest = [n for n in nuke.allNodes('Read') if n != aov_beauty]
                shuffling(aov_beauty, aov_rest)
