def _version_():
    ver='''

    version 1.1
    - add more render types
    - fix precomp render directory problem (`render/` to `elements/`)
    - add render dialog UI with threading
    - fixing naming error in render file, avoid `..._comp_comp_...`
    - automatically check latest version

    version 1.0
    - auto set directory and type and versioning

    '''
    return ver

__VERSION__=1.1



#------------------------------------------------------------------------------
#-Import Modules
#------------------------------------------------------------------------------




import nuke, nukescripts, os
import slate
import shutil
import subprocess
from kputl import joinPath




#------------------------------------------------------------------------------
#-Global Variables
#------------------------------------------------------------------------------




RENDER_TYPE = ['comp', 'precomp', 'lookdev', 'backplate', 'lgtSlap', 'delivery']
NO_PASSNAME = ['comp', 'lookdev', 'backplate', 'lgtSlap', 'delivery']
TYPE_CONFIG = {
    'comp': {'DIR': slate.RENDER_DIR, 'CH': 'rgb', 'EXT': 'exr'},
    'precomp': {'DIR': slate.ELEMENTS_DIR, 'CH': 'all', 'EXT': 'exr'},
    'lookdev': {'DIR': slate.RENDER_DIR, 'CH': 'rgb', 'EXT': 'exr'},
    'backplate': {'DIR': slate.ELEMENTS_DIR, 'CH': 'rgba', 'EXT': 'jpg'},
    'lgtSlap': {'DIR': slate.RENDER_DIR, 'CH': 'rgb', 'EXT': 'exr'},
    'delivery': {'DIR': slate.DELIVERY_DIR, 'CH': 'rgb', 'EXT': 'exr'}
}

PADDING_VER, PADDING_FRAME = slate.SHOW_CONFIG['padding']
PADDING_FRAME = '%0{}d'.format(int(PADDING_FRAME))
VERSION_LABEL = {
    'delivery': "<font color='Gold'>(version matching latest comp version)</>",
    'new_version': "<font color='LimeGreen'>(new version)</>"
    }




#------------------------------------------------------------------------------
#-Supporting Function
#------------------------------------------------------------------------------




def image_group_path(verType, ver):
    '''create image group path, with scriptcopy
    @verType: verType of the file (str)
    @ver: file version (int)
    return: [out_exr, out_scriptcopy]  full file path (list)
    '''
    # Type without passname
    just_verType = verType.split('_')[0]

    versionName, versionDir, out_file, out_scriptcopy = None,None,None,None

    def _makeFile(versionName, subdir):
        '''sets out values
        @versionName: name of the version, format differs between delivery and non-delivery, ie. show_shot_type_pass_v###
        @subdir: sub-directory under version directory
        '''
        # Version directory
        versionDir = joinPath(TYPE_CONFIG[just_verType]['DIR'], versionName)
        out_file = joinPath(
            versionDir,
            subdir,
            '{versionName}.{frame}.{ext}'.format(versionName=versionName,frame=PADDING_FRAME,ext=TYPE_CONFIG[just_verType]['EXT'])
            )

        # Output file scriptcopy
        out_scriptcopy = joinPath(versionDir,'%s.scriptcopy.nk' % versionName)

        return out_file, out_scriptcopy

    # Set values
    if just_verType == 'delivery':
        # Delivery version
        versionName = '{show}_{shot}_comp_v{ver}.delivery'.format(
            show=slate.SHOW_CONFIG['kp_show'],
            shot=slate.SHOT_CONFIG['kp_shot'],
            ver=str(ver).zfill(int(PADDING_VER))
        )
        out_file, out_scriptcopy = _makeFile(versionName, TYPE_CONFIG[just_verType]['EXT'])
    else:
        # Non-Delivery version
        versionName = '{show}_{shot}_{verType}_v{ver}'.format(
            show=slate.SHOW_CONFIG['kp_show'],
            shot=slate.SHOT_CONFIG['kp_shot'],
            verType=verType,
            ver=str(ver).zfill(int(PADDING_VER))
        )
        out_file, out_scriptcopy = _makeFile(versionName, verType)

    print("\n==========\n- version:\n%s\n\n- file:\n%s\n\n- scriptcopy:\n%s\n==========" % (versionName, out_file, out_scriptcopy))

    return out_file, out_scriptcopy


def get_versions(verType):
    '''get the latest version of selected version type
    @verType: version type (str)
    return: verLatest (int)
    '''

    just_verType = verType.split('_')[0]
    if just_verType == 'delivery':
        _dir2list = TYPE_CONFIG['comp']['DIR']
        _type2look = '_comp_'
    else:
        _dir2list = TYPE_CONFIG[just_verType]['DIR']
        _type2look = '_'+verType+'_'

    ls_ver = [int(v.split('_v')[1]) for v in os.listdir(_dir2list) if _type2look in v]
    ls_ver = [0] if len(ls_ver)==0 else ls_ver

    return ls_ver


def get_type(node):
    ''' get the type of the node'''
    out_type = node['mu_type'].value()
    out_type = out_type+'_'+node['tx_passname'].value() if out_type not in NO_PASSNAME else out_type

    return out_type


def set_versions(node, out_type):
    '''sets the list of version and labels
    @node: node (obj)
    @out_type: ouput type (str)
    '''

    if out_type == 'delivery':
        verNew = max(get_versions(out_type))
        node['mu_ver'].setEnabled(False)
        node['tx_versionLabel'].setValue(VERSION_LABEL['delivery'])
    else:
        verNew = max(get_versions(out_type))+1
        node['mu_ver'].setEnabled(True)
        node['tx_versionLabel'].setValue(VERSION_LABEL['new_version'])

    ls_ver = [str(v) for v in range(1, verNew+1)]
    node['mu_ver'].setValues(ls_ver)
    # node['mu_ver'].setValue(max(ls_ver))


def set_file(node, out_type, ver):
    '''set output file and settings
    @node: node (obj)
    @out_type: output type (str)
    @ver: version to set (int)
    '''

    out_file, out_scriptcopy = image_group_path(out_type, ver)
    node['file'].setValue(out_file)
    node['tx_scriptcopy'].setValue(out_scriptcopy)
    node['channels'].setValue(TYPE_CONFIG[out_type.split('_')[0]]['CH'])

    # print "==========\n\n%s\n\n%s-%s\n\n==========" % (
    # file, nuke.Root()['first_frame'].value(), nuke.Root()['last_frame'].value()
    # )




#------------------------------------------------------------------------------
#-Main Function
#------------------------------------------------------------------------------




def KuWrite():
    '''Adding inputs for auto generate output path'''

    node = nuke.createNode('Write')
    node.setName('KuWrite')
    node.knob('file').setEnabled(False)

    k_pipeline = nuke.Text_Knob('kupipeline', 'kuWrite', 'kuWrite') # Ku Pipeline Identifier

    k_tab = nuke.Tab_Knob('tb_KuWrite', 'KuWrite')
    k_title = nuke.Text_Knob('tx_title', '', '<h1><br>KuWrite</h1>')
    k_show = nuke.Text_Knob('tx_show', '<h3>show</h3>', slate.SHOW_CONFIG['kp_show'])
    k_shot = nuke.Text_Knob('tx_shot', '<h3>shot</h3>', slate.SHOT_CONFIG['kp_shot'])
    k_type = nuke.Enumeration_Knob('mu_type', '<h3>type</h3>', RENDER_TYPE)
    k_elements = nuke.String_Knob('tx_passname', '_', 'NewPass')
    k_ver = nuke.Enumeration_Knob('mu_ver', '<h3>version</h3>', [' '])
    k_latest = nuke.Text_Knob('tx_versionLabel', '', VERSION_LABEL['new_version'])
    k_div_title = nuke.Text_Knob('divider','')
    k_div = nuke.Text_Knob('divider',' ')
    k_set = nuke.PyScript_Knob('bt_set', '<b>Set Write</b>', 'mod_KuWrite.set_settings(nuke.thisNode())')
    k_render = nuke.PyScript_Knob('bt_render', '<b>Render</b>', 'mod_KuWrite.render_node(nuke.thisNode())')
    k_scriptcopy = nuke.String_Knob('tx_scriptcopy', 'scriptcopy dir', '')

    k_elements.clearFlag(nuke.STARTLINE)
    k_elements.setVisible(False)
    k_set.setFlag(nuke.STARTLINE)
    k_latest.clearFlag(nuke.STARTLINE)
    k_render.clearFlag(nuke.STARTLINE)
    k_pipeline.setVisible(False)
    k_scriptcopy.setVisible(False)

    for k in [k_tab, k_pipeline, k_title, k_div_title, k_show, k_shot, k_type, k_elements, k_ver, k_latest, k_div, k_set, k_render, k_scriptcopy]:
        node.addKnob(k)

    mod = os.path.basename(__file__).split('.')[0]
    node['knobChanged'].setValue('%s.onChange()' % mod)

    out_type = get_type(node)
    set_versions(node, out_type)
    verLatest = max(get_versions(node['mu_type'].value()))+1
    node['mu_ver'].setValue(verLatest)
    set_file(node, out_type, verLatest)




#------------------------------------------------------------------------------
#-Knob Changed
#------------------------------------------------------------------------------




def onChange():
    '''knob change function to call'''

    n = nuke.thisNode()
    k = nuke.thisKnob()

    if k.name() in ['mu_type','tx_passname']:
        verType = get_type(n)
        set_versions(n, verType)

        if n['mu_type'].value() not in NO_PASSNAME:
            n['tx_passname'].setVisible(True)
        else:
            n['tx_passname'].setVisible(False)

        n['mu_ver'].setValue(max(n['mu_ver'].values()))
        set_file(n, verType, n['mu_ver'].value())

    if k.name() in ['mu_ver']:
        verType = get_type(n)

        if n['mu_ver'].value() == max(n['mu_ver'].values()):
            n['tx_versionLabel'].setVisible(True)
        else:
            n['tx_versionLabel'].setVisible(False)

        set_file(n, verType, n['mu_ver'].value())

    if k.name() == 'mu_type' and k.value() == 'delivery':
        n['tile_color'].setValue(12533759)
    else:
        n['tile_color'].setValue(0)




#------------------------------------------------------------------------------
#-Rendering Node
#------------------------------------------------------------------------------




def render_node(node):
    '''launch render'''
    out_path = node['file'].value()
    out_scriptcopy = node['tx_scriptcopy'].value()
    startFrame = int(nuke.Root()['first_frame'].value())
    endFrame = int(nuke.Root()['last_frame'].value())

    def _soloWrite(sel_node, all_enabled_write, mode='solo'):
        if mode == 'solo':
            for s in all_enabled_write:
                if s != sel_node.name():
                    print('node disabled---' + s )
                    nuke.toNode(s)['disable'].setValue(True)
        elif mode == 'reverse':
            for s in all_enabled_write:
                nuke.toNode(s)['disable'].setValue(False)
                print('node enabled---' + s )

    askMessage = "Render Node: %s\nFile: %s\nFramerage: %s-%s\n" % (
    node.name(), os.path.basename(node['file'].value()), startFrame, endFrame)
    c = nuke.ask(askMessage)
    if c:
        if not os.path.exists(os.path.dirname(out_path)):
            p = os.path.dirname(out_path)
            os.makedirs(p)
            print("out path created --- %s" % p)
        if not os.path.exists(os.path.dirname(out_scriptcopy)):
            s = os.path.dirname(out_scriptcopy)
            os.makedirs(s)
            print("out scriptcopy created --- %s" % s)

        all_enabled_write = [n.name() for n in nuke.allNodes('Write') if n['disable'].value() == False]
        _soloWrite(node, all_enabled_write, mode='solo')
        nuke.scriptSave()
        thisScript_path = nuke.scriptName()
        shutil.copy2(thisScript_path, out_scriptcopy)

        # nuke.render(node, startFrame, endFrame)

        exe = joinPath(nuke.EXE_PATH).replace('/', '\\')

        cmd_str = """start cmd /k "{exe}" -t -m 22 -xi {script} {start}-{end}""".format(
            exe=exe,
            node=node.name(),
            script=thisScript_path,
            start=startFrame,
            end=endFrame
        )

        # subprocess.Popen(cmd_str, shell=True)
        _soloWrite(node, all_enabled_write, mode='reverse')
    else:
        print("user cancelled")


KuWrite()
# render_node(nuke.toNode('KuWrite1'))
