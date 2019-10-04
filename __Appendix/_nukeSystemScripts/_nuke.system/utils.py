# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import os.path
import nuke

class FnPySingleton(object):
  def __new__(type, *args, **kwargs):
    if not '_the_instance' in type.__dict__:
      type._the_instance = object.__new__(type)
    return type._the_instance

def script_directory():
  scriptFilePath = nuke.root().knob("name").value()
  if not scriptFilePath:
    return ""

  return os.path.dirname(scriptFilePath)

