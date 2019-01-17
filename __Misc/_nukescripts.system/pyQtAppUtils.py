# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import nuke
from nukescripts import pyAppUtils

class pyQtAppHelper(pyAppUtils.pyAppHelper, nuke.FnPySingleton):
  """ Helper class to initialise PyQt in a separate thread """

  def __init__(self, argv = [], start = None):
    try:
      if self.__pyQtApp: pass
    except:
      super(pyQtAppHelper, self).__init__(start)
      self.__pyQtApp = None

    if start:
      self.start(argv)


  def getApplication(self, argv):
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    if self.__pyQtApp is None:
      self.__pyQtApp = QtGui.QApplication(argv)
    return self.__pyQtApp


  def closeApplication(self):
    self.__pyQtApp = None


  def start(self, argv):
    super(pyQtAppHelper, self).initiate()
    self.run(self.getApplication, (argv,))


  def stop(self):
    self.run(self.closeApplication)
    super(pyQtAppHelper, self).terminate()
