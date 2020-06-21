import re, sys, traceback, os, string
from StringIO import StringIO

import PySide.QtGui
import PySide.QtCore



def runScript(self):
    _selection = False
    self.highlightCurrentLine()

    #Get text
    text = self.toPlainText()

    #Check if we've got some text selected. If so, replace text with selected text
    tc = self.textCursor()
    if tc.hasSelection() :
        _selection = True
        rawtext = tc.selectedText()
        rawSplit = rawtext.splitlines()
        rawJoined = '\n'.join(rawSplit)
        text = rawJoined.lstrip().rstrip()

    #Fix syntax error if last line is a comment with no new line
    if not text.endswith('\n') :
        text = text + '\n'

    #Compile
    result = None
    compileSuccess = False
    runError = False

    try :
        type = 'exec'
        if text.count('\n') == 1:
          type = 'single'
        compiled = compile(text, '<string>', type)
        compileSuccess = True
    except Exception,e:
        result = traceback.format_exc()
        runError = True
        compileSuccess = False

    oldStdOut = sys.stdout
    if compileSuccess :
        #Override stdout to capture exec results
        buffer = StringIO()
        sys.stdout = buffer
        try:
            exec(compiled, globals())
        except Exception,e:
            runError = True
            result = traceback.format_exc()
        else:
            result = buffer.getvalue()
    sys.stdout = oldStdOut

    #Update output
    self._output.updateOutput( text )
    self._output.updateOutput( "# Result: \n" )
    self._output.updateOutput( result )
    self._output.updateOutput( "\n" )

    if runError :
        self._errorLine = self.getErrorLineFromTraceback(result)
        self.highlightErrorLine()

    else :
        #Update history stack
        self._editor._historyStack.append(text)

        #Update button state
        self._editor.clearHistoryButton.setEnabled(1)
        self._editor.previousButton.setEnabled(1)
        self._editor.nextButton.setEnabled(0)
