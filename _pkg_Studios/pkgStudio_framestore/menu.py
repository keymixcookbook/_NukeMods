import nuke
import nukescripts


def launchRV():
    '''launch RV with multiple selections and stack'''
    path_read = []

    for n in nuke.selectedNodes('Group'):
        if 'fAsset' in n.knobs():
            with n:
                for r in nuke.allNodes('Read'):
                    path_read.append(nuke.filename(r))
        else:
            print "%s not a fAsset Read node" % n.name()

    if path_read:
        cmd = "rv -c -s 0.25 -over %s &" % ' '.join(path_read)
        os.system(cmd)
