import nuke




########## AddMenuItem Func ##########




def addMenuItem(type, mu, name, mod, hotkey="", icon="", shortcutContext=1):

    '''
    type: 'm'= modules, 'f' = functions
    mu: menu variable
    mod: module/function name
    hotkey: ctl, alt, shift + letter
    icon: image file name + ext
    '''

    if type == 'm':
        mu.addCommand(name, "mod_{mod}.{func}".format(mod=mod.split('(')[0],func=mod), hotkey, icon=icon, shortcutContext=shortcutContext)
    elif type == 'f':
        mu.addCommand(name, "{func}".format(func=mod), hotkey, icon=icon, shortcutContext=shortcutContext)




########## KuFunc Menubar ##########




kuMu = nuke.menu('Nuke').addMenu('KU')

addMenuItem('f', kuMu, 'Connect Mask Input', "mask()", hotkey="ctrl+Y")
addMenuItem('f', kuMu, 'Change label',"labelChange()", hotkey="shift+N")
addMenuItem('m', kuMu, 'Linked Postage Stamp',"LinkedStamp()", hotkey="f4")
addMenuItem('f', kuMu, 'Group Connect A', "groupConnect()", hotkey="alt+ctrl+Y")
addMenuItem('f', kuMu, 'Set Operation', "mergeOp()", hotkey="alt+O")
addMenuItem('m', kuMu, 'Branching', "Branching()", hotkey="j", shortcutContext=2)
addMenuItem('f', kuMu, 'CycleChannels/rgba', "cycleChannels()", hotkey="c", shortcutContext=2)
addMenuItem('f', kuMu, 'CycleChannels/all channels', "cycleChannels(mode='all')", hotkey="shift+c", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/>', "setSize(0.25)", hotkey="alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<', "setSize(-0.25)", hotkey="alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/>>', "setSize(0.5)", hotkey="shift+alt+.", shortcutContext=2)
addMenuItem('f', kuMu, 'SetVal/<<', "setSize(-0.5)", hotkey="shift+alt+,", shortcutContext=2)
addMenuItem('f', kuMu, 'Launch Selection in RV', "launchRV()", hotkey="f2")
kuMu.addSeparator()
addMenuItem('m', kuMu, 'Set Grain Channels', "GrainChannel()")
addMenuItem('m', kuMu, 'Link Clone', "LinkClone()")
addMenuItem('m', kuMu, 'Find Hidden Inputs', "RestoreHiddenInputs()")
addMenuItem('m', kuMu, 'Scale DAG', "ScaleTree()")
kuMu.addSeparator()
addMenuItem('m', kuMu, '$GUI Switch/switch', "GUISwitch(mode='switch')", hotkey="shift+D")
addMenuItem('m', kuMu, '$GUI Switch/reverse', "GUISwitch(mode='reverse')", hotkey="ctrl+shift+D")
kuMu.addSeparator()
kuMu.addCommand('Shuffle', "nuke.createNode('Shuffle')", "h", shortcutContext=2)
kuMu.addCommand('Expression', "nuke.createNode('Expression')", "e", shortcutContext=2)
