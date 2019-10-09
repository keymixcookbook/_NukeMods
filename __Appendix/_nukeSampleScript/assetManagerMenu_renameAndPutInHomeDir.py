import assetManager

# CREATE A READ NODE AND OPEN THE "DB" TAB
def customRead():
	n = nuke.createNode( 'Read' )
	n['DB'].setFlag( 0 )

# ADD CUSTOM READ AND WRITE TO TOOLBAR
nuke.menu( 'Nodes' ).addCommand( 'Image/WriteAsset', lambda: nuke.createNode( 'WriteAsset' ), 'w' )
nuke.menu( 'Nodes' ).addCommand( 'Image/Read', customRead, 'r' )

# ADD EASY SAVE TO SHOT MENU
shotMenu = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )
nuke.menu( 'Nuke' ).addCommand( shotMenu+'/Easy Save', assetManager.easySave )


# SET FILE BROWSER FAVORITES
nuke.addFavoriteDir(
    name = 'NUKE SCRIPTS',
    directory = assetManager.nukeDir(),
    type = nuke.SCRIPT)

# HELPER FUNCTION FOR NUKE SCRIPT PANEL
def nkPanelHelper():
	# GET ALL NUKE SCRIPTS FOR CURRENT SHOT
	nkScripts = assetManager.getNukeScripts()
	if not nkScripts:
		# IF THERE ARE NONE DON'T DO ANYTHING
		return
	# CREATE PANEL
	p = assetManager.NkPanel( nkScripts )
	# ADJUST SIZE
	p.setMinimumSize( 200, 200 )

	# IF PANEL WAS CONFIRMED AND A NUKE SCRIPT WAS SELECTED, OPEN IT
	if p.showModalDialog():
		if p.selectedScript:
			nuke.scriptOpen( p.selectedScript )

# ADD CALLBACKS
nuke.addOnScriptSave( assetManager.checkScriptName )
nuke.addOnUserCreate( nkPanelHelper, nodeClass='Root')
nuke.addOnUserCreate( assetManager.createVersionKnobs, nodeClass='Read' ) 
nuke.addKnobChanged( assetManager.updateVersionKnob, nodeClass='Read' )  
#nuke.addBeforeRender( assetManager.createOutDirs, nodeClass='Write' )
nuke.knobDefault( 'Write.beforeRender', 'assetManager.createOutDirs()')



#RGS-TRAPCODE-001
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# The Particular V2 Gizmo
import ParticularV2_3DScript															#import the scripts for use in nuke
toolbar = nuke.toolbar("Nodes")															#get main toolbar
tcMenu = toolbar.addMenu("Trapcode")													#get 'Trapcode' menu
tcMenu.addCommand("Particular 3D Gizmo", "ParticularV2_3DScript.pv2_createGizmo(nuke)")	#add command and run start command. 
																						#need to pass in nuke
#create callbacks
ParticularV2_3DScript.pv2_createCallbacks()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
