'''
# source: https://community.foundry.com/discuss/topic/102647/how-can-i-import-all-sequence-images-from-one-folder-and-sub?mode=Post&postID=891904
import aovs exrs as image group

filename structure:

<show>_<shot####>_lgt_v<###>/<RenderLayer>/<RenderPass>/<RenderPass>.%04d.exr
bpp_ism0010_lgt_v011/masterLayer/albeto/albeto.1001.exr

'''



def _version_():
	'''

	version 1.2
	- symlink fix to UNIX style
	- fixing channel shuffle of crptomatte, Z matte
	- enable 'Raw' to data passes

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
from kputl import joinPath
from Qt import QtWidgets, QtGui, QtCore




#-------------------------------------------------------------------------------
#-Global Variables
#-------------------------------------------------------------------------------


DATA_AOV = ['P', 'N', 'Z', 'crypto_object', 'crypto_material','crypto_asset']



#-------------------------------------------------------------------------------
#-Supporting Function
#-------------------------------------------------------------------------------




def createRead(path):
	'''create read from path
	@path: full path for AOV, (str)
	return: aov read node, (obj)
	'''

	exrs = nuke.getFileNameList(path)[0] # ['albedo.####.exr 1-96']
	frames, range = exrs.split(' ')
	first, last = range.split('-')
	first = int(first)
	last = int(last)
	aov = nuke.nodes.Read(
		file=joinPath(path, frames),
		name=os.path.basename(path),
		first=first,
		last=last,
		label=os.path.basename(path)
		)
	isData = True if aov.name() in DATA_AOV else False
	aov['raw'].setValue(isData)

	return aov


def getAOVs(dir_renderVersion):
	'''get renderLayer, then passes
	@path: Render root path (ie. '/TIO_orbit_1k_v001'), str
	return: {<renderLayer>: [<renderPasses>]}
	'''
	ls_aov = {} # {RenderLayer: [RenderPasses, RenderPasses]}
	for l in nuke.getFileNameList(dir_renderVersion):
		thisLayer = [p for p in nuke.getFileNameList(joinPath(dir_renderVersion, l))]
		ls_aov[l] = thisLayer

	return ls_aov


def shuffling(node_B, aov_rest):
	'''create ShuffleCopy with changing nodes, then connects output
	@node_B: node on B pipe (obj), changes per interation
	@aov_rest: list of nodes except the beauty node (list of objs)
	'''
	curB = node_B
	for n in aov_rest:
		if 'crypto_' in n.name():
			thisB = nuke.nodes.Copy(
						inputs=[curB, n],
						name='in_%s' % n.name(),
						channels='all',
						from0='-none',
						to0='-none'
			)
		elif n.name() == 'Z':
			thisB = nuke.nodes.ShuffleCopy(
						inputs=[curB, n],
						name='in_%s' % n.name(),
						out = 'depth',
						red = 'red'
						)
		else:
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
		# print curB.name()
	nuke.nodes.Output(inputs=[curB])


def getLightingPath():
	'''get lighting render dir from kupipeline'''
	import mod_StudioLoad

	SHOW=mod_StudioLoad.LoadSlate()['SHOW']
	SHOT=mod_StudioLoad.LoadSlate()['SHOT']
	path=joinPath('K:/PROJECTS/Personal/', SHOW, SHOT, 'assets', 'lighting')
	return path




#------------------------------------------------------------------------------
#-Main function
#------------------------------------------------------------------------------




class Core_SequenceLoader(QtWidgets.QWidget):
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
		dir = QtWidgets.QFileDialog.getExistingDirectory(self,
			"set lighting directory",
			self.lgtPath.text(),
			QtWidgets.QFileDialog.ShowDirsOnly
		)

		if dir != None:
			self.lgtPath.setText(dir)
			self.getVersions()


	def getVersions(self):
		'''get the render versions with given lighting dir and populate combox'''
		dir_lgt = self.lgtPath.text()
		ls_excute = ['tmp', '.DS_Store']
		ls = [v for v in os.listdir(dir_lgt) if v not in ls_excute]
		self.renderVersion_mu.clear()
		if len(ls)>0:
			self.renderVersion_mu.addItems(ls)
			self.load_btn.setEnabled(True)
			self.load_btn.setText("Load Sequence")
			# print "render versions:\n-%s" % '\n-'.join(ls)
		else:
			self.load_btn.setEnabled(False)
			self.load_btn.setText("NO RENDER VERSION FOUND IN DIR")
			print "\n**********\nNO RENDER VERSION FOUND IN DIR:\n%s\n**********\n" % dir_lgt


	def SequenceLoader(self):
		'''main function construct the image group'''

		dir_renderVersion = joinPath(self.lgtPath.text(), self.renderVersion_mu.currentText())
		if dir_renderVersion == None:
			nuke.message("Import Canceled")
		else:
			name_renderVersion = os.path.basename(dir_renderVersion.rstrip('/')) # TIO_orbit_1k_v001
			ver_renderVersion = int(name_renderVersion.split('_v')[1])
			RGBA = 'beauty'

			# Building Image Group
			ls_aov = getAOVs(dir_renderVersion)
			for p in ls_aov[ls_aov.keys()[0]]:
				nuke.Layer(p, ['%s.red' % p, '%s.green' % p, '%s.blue' % p, '%s.alpha' % p])
			# nodeLabel = '%s\nv%s' % (name_renderVersion.split('_v')[0], name_renderVersion.split('_v')[1])
			nodeLabel = "nuke.thisNode().name()+'\\n'+nuke.thisNode()['tx_version'].value()+'\\n\\n'+nuke.thisNode()['tx_layer'].value()+'\\n'+'v'+nuke.thisNode()['int_thisVersion'].value()"
			for l in ls_aov.keys():
				imgGroup = nuke.nodes.Group(autolabel=nodeLabel, postage_stamp=1)
				imgGroup.setName('kpRead1')
				t_tab = nuke.Tab_Knob('tb_user', 'kpRead')
				k_pipeline = nuke.Text_Knob('kupipeline', 'kpRead', 'kpRead') # Ku Pipeline Identifier
				k_renderVersion = nuke.Text_Knob('tx_version','<b>render: </b>', name_renderVersion.split('_v')[0])
				mod=os.path.basename(__file__).split('.py')[0]
				k_verUp = nuke.PyScript_Knob('btn_verUp', '<b>&#9650;</b>', '%s.versionUp(nuke.thisNode())' % mod)
				k_verDown = nuke.PyScript_Knob('btn_verDown', '<b>&#9660;</b>', '%s.versionDown(nuke.thisNode())' % mod)
				k_verLatest = nuke.PyScript_Knob('btn_verLatest', '<b>&#9733;</b>', '%s.versionLatest(nuke.thisNode())' % mod)
				k_thisVersion = nuke.Text_Knob('int_thisVersion', '<b>version: </b>')
				k_thisVersion.setValue('%03d' % ver_renderVersion)
				k_renderLayer = nuke.Text_Knob('tx_layer','<b>layer: </b>', l)
				k_div = nuke.Text_Knob('', "<b>Switch Version:</b>" )
				k_path = nuke.Text_Knob('tx_dir','<b>path: </b>', dir_renderVersion)
				# k_aov = nuke.Text_Knob('tx_aov', '<b>aovs: </b>', '\n'.join(ls_aov[l]))

				# k_thisVersion.setEnabled(False)
				k_thisVersion.setFlag(nuke.STARTLINE)
				k_path.setVisible(False)
				k_verUp.setFlag(nuke.STARTLINE)
				k_verUp.setTooltip("Version Up")
				k_verDown.clearFlag(nuke.STARTLINE)
				k_verDown.setTooltip("Version Down")
				k_verLatest.clearFlag(nuke.STARTLINE)
				k_verLatest.setTooltip("Latest Version")
				k_pipeline.setVisible(False)

				for k in [t_tab, k_pipeline, k_path, k_renderVersion, k_thisVersion, k_renderLayer, k_div, k_verUp, k_verDown, k_verLatest]:
					imgGroup.addKnob(k)

				with imgGroup:
					aov_beauty = None
					aov_rest = []
					for p in ls_aov[l]:
						path = joinPath(dir_renderVersion, l, p)
						createRead(path)
					aov_beauty = nuke.toNode(RGBA)
					aov_rest = [n for n in nuke.allNodes('Read') if n != aov_beauty]
					shuffling(aov_beauty, aov_rest)

			self.close()




#------------------------------------------------------------------------------
#-Button Functions
#------------------------------------------------------------------------------




def versionChange(n, cur_ver, new_ver):
	'''change version, up/down/latest
	@n: node, obj
	@cur_ver: current version, int
	@new_ver: new version, int
	'''

	new_ver_str = '_v%03d' % new_ver
	path_ver=n['tx_dir'].value()
	path_lgt=os.path.dirname(n['tx_dir'].value())
	cur_ver_str = '_v%03d' % cur_ver
	new_path = path_ver.replace(cur_ver_str, new_ver_str)

	if os.path.isdir(new_path):
		with n:
			all_read = nuke.allNodes('Read')
			for r in all_read:
				thisFilename=nuke.filename(r)
				thisFilename=thisFilename.replace(cur_ver_str, new_ver_str)
				r['file'].setValue(thisFilename)
			n['tx_dir'].setValue(new_path)
			n['int_thisVersion'].setValue('%03d' % new_ver)

	else:
		print "No version %s found" % new_path


def versionUp(n):
	'''version up button'''
	cur_ver = int(n['int_thisVersion'].value())
	new_ver = cur_ver+1

	versionChange(n, cur_ver, new_ver)


def versionDown(n):
	'''version down button'''
	cur_ver = int(n['int_thisVersion'].value())
	new_ver = cur_ver-1

	versionChange(n, cur_ver, new_ver)


def versionLatest(n):
	'''version latest button'''
	path_lgt=os.path.dirname(n['tx_dir'].value())
	renderVersion = n['tx_version'].value()
	ls_renderVersion = [int(v.split('_v')[1]) for v in os.listdir(path_lgt) if renderVersion in v]
	cur_ver = int(n['int_thisVersion'].value())
	new_ver = max(ls_renderVersion)

	versionChange(n, cur_ver, new_ver)




#------------------------------------------------------------------------------
#-Instancing
#------------------------------------------------------------------------------




SequenceLoader=Core_SequenceLoader()
