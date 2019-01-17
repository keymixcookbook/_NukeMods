# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import nuke

# This is for testing that all plugins were compiled correctly
def load_all_plugins():
  tried = 0
  failed = 0
  p = nuke.plugins(nuke.ALL, "*."+nuke.PLUGIN_EXT)
  for i in p:
    # Ignore Alembic_In, since it isn't a nuke plugin.
    # TODO - Needs to be moved a directory up so it doesn't show as a nuke plugin
    if i.find("Alembic_In") != -1:
      continue

    tried += 1
    print i
    try:
      try_load = nuke.load(i)
    except:
      print i, "failed to load."
      failed += 1
  if failed > 0:
    print failed, "of", tried, "plugin(s) total did not load"
  else:
    print "All available binary plugins (",tried,") successfully loaded"

