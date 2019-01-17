# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

"""\
This module provides all the Nuke-specific functions and Classes.
"""
__all__ = []

def __filterNames(name):
  namesList = ["import_module"]
  if name[0] == "_" or name in namesList: return False
  return True

def import_module(name, filterRule):
  global __all__
  import inspect
  mod = __import__(name)
  for i in dir(mod):
    obj = getattr(mod, i)
    if filterRule(i):
      __all__.append(i)

# get the functions that are compiled into Nuke:
from _nuke import *
from utils import *
from callbacks import *
from colorspaces import *
from executeInMain import *
from overrides import *

import _nukemath as math
import _geo as geo

from scripts import scriptSaveAndClear

import_module(__name__, __filterNames)

