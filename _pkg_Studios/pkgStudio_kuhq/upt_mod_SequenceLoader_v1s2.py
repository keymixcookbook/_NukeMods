'''
# source: https://community.foundry.com/discuss/topic/102647/how-can-i-import-all-sequence-images-from-one-folder-and-sub?mode=Post&postID=891904
import aovs exrs as image group

filename structure:

<show>_<shot####>_lgt_v<###>/<RenderLayer>/<RenderPass>/<RenderPass>.%04d.exr
bpp_ism0010_lgt_v011/masterLayer/albeto/albeto.1001.exr

'''



def _version_():
    '''

    version 1.1
    - qt UI for selecting render versions
    - version updates in group node tab

    version 1.0
    - Select version folder and loads render layer inside
    - import aovs exrs as image group

    '''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import nuke, os
from Qt import QtWidgets, QtGui, QtCore





#-------------------------------------------------------------------------------
#-Supporting Function
#-------------------------------------------------------------------------------




def createRead(path):
    '''create read from path
    @path: full path for AOV, str
    return: aov read node, obj
    '''

    exrs = nuke.getFileNameList(path)[0] # ['albedo.####.exr 1-96']
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
    path.replace('\\', '/')
    return path



#------------------------------------------------------------------------------
#-Main function
#------------------------------------------------------------------------------




class Core_SequenceLoader(QtWidgets.QDialog):
    def __init__(self):
        super(Core_SequenceLoader, self).__init__()

        self.lgtPath_label = QtWidgets.QLabel('lighting dir: ')
        self.lgtPath = QtWidgets.QLineEdit()
        self.lgtPath.setMinimumWidth(500)
        self.lgtPath_btn = QtWidgets.QPushButton('Browse')
        self.lgtPath_btn.clicked.connect(self.browse)
        self.renderVersion_label = QtWidgets.QLabel("lighting ver: ")
        self.renderVersion_mu = QtWidgets.QComboBox()
        self.renderVersion_mu.setMinimumWidth(250)
        self.load_btn = QtWidgets.QPushButton('Load Sequence')
        self.load_btn.clicked.connect(self.SequenceLoader)

        self.file_layout = QtWidgets.QHBoxLayout()
        self.master_layout = QtWidgets.QVBoxLayout()
        self.combobox_layout = QtWidgets.QHBoxLayout()

        self.file_layout.addWidget(self.lgtPath_label)
        self.file_layout.addWidget(self.lgtPath)
        self.file_layout.addWidget(self.lgtPath_btn)
        self.combobox_layout.addWidget(self.renderVersion_label)
        self.combobox_layout.addWidget(self.renderVersion_mu)
        self.combobox_layout.addStretch(1)


        self.master_layout.addLayout(self.file_layout)
        self.master_layout.addLayout(self.combobox_layout)
        self.master_layout.addWidget(self.load_btn)
        self.master_layout.addStretch(1)
        self.setLayout(self.master_layout)
        self.setWindowTitle("Sequence Loader")

        self.setDefault()


    def setDefault(self):
        '''set default value when instancing'''

        self.lgtPath.setText(getLightingPath())
        self.getVersions()


    def run(self):
        '''run panel instance'''
        self.show()
        self.raise_()


    def browse(self):
        '''browse for lighting dir'''
        dir = nuke.getFilename(
            "select lighting dir",
            pattern='*/',
            default=getLightingPath()
            )
        self.lgtPath.setText(dir)


    def getVersions(self):
        '''get the render versions with given lighting dir and populate combox'''
        dir_lgt = self.lgtPath.text()
        ls = [v for v in os.listdir() if '_lgt_' in v]
        self.renderLayer_mu.addItems(ls)

        print "render versions:\n %s" % '\n'.join(ls)


    def SequenceLoader(self):
        '''main function construct the image group'''

        dir_renderVersion = os.path.join(self.lgtPath.text(), self.renderVersion_mu.currentText()).replace('\\', '/')
        if dir_renderVersion == None:
            nuke.message("Import Canceled")
        else:
            name_renderVersion = os.path.basename(dir_renderVersion.rstrip('/')) # TIO_orbit_1k_v001
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

            self.close()
