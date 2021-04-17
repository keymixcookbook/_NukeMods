import nuke
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
    from PySide import QtOpenGL
else:
    from PySide2 import QtGui, QtCore, QtWidgets, QtOpenGL

def findDagWidget():
    stack = QtWidgets.QApplication.topLevelWidgets()
    widgets = []
    while stack:
        widget = stack.pop()
        if widget.windowTitle() == nuke.activeViewer().node().name():
            viewerAreas = [c for c in widget.children() if isinstance(c, QtOpenGL.QGLWidget)]
            widgets.append(viewerAreas[1])
        elif widget.objectName() == 'DAG.1':
            for w in widget.children():
                if isinstance(w, QtOpenGL.QGLWidget):
                    widgets.append(w)
        stack.extend(c for c in widget.children() if c.isWidgetType())
    return widgets

class mouseIntercepter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.MidButton:
                def sendkey(key):
                    new_event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier)
                    QtWidgets.QApplication.instance().postEvent(
                       obj,
                       new_event)
                return True
            else:
                return False
        else:
            return False

#Disable Event Filter
try: viewer.removeEventFilter(my_filter)
except: pass


# Install event filter
if __name__ == "__main__":
	dag = findDagWidget()
	my_filter = mouseIntercepter()
	for w in dag:
		w.installEventFilter(my_filter)


#nuke.menu('Nuke').addMenu("Edit").addCommand('disable mid button',"exec(open('YOUR_PATH\disableMidMouseButton.py').read())", 'alt+shift+b')
