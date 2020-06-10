import re, sys, traceback, os, string
from StringIO import StringIO

import PySide.QtGui
import PySide.QtCore

ICONSIZE = 22
FN_CTRLKEYNAME = "Ctrl"
FN_SPACESINTAB = 4

iconRoot = os.path.dirname(__file__)
previousIconPath = os.path.join(iconRoot, "previous.png")
nextIconPath = os.path.join(iconRoot, "next.png")
clearHistoryIconPath = os.path.join(iconRoot, "clearHistory.png")
sourceIconPath = os.path.join(iconRoot, "source.png")
loadIconPath = os.path.join(iconRoot, "load.png")
saveIconPath = os.path.join(iconRoot, "save.png")
runIconPath = os.path.join(iconRoot, "run.png")
clearOutputIconPath = os.path.join(iconRoot, "clearOutput.png")
inputOnIcon = os.path.join(iconRoot, "inputOn.png")
inputOffIcon = os.path.join(iconRoot, "inputOff.png")
outputOnIcon = os.path.join(iconRoot, "outputOn.png")
outputOffIcon = os.path.join(iconRoot, "outputOff.png")
bothOnIcon = os.path.join(iconRoot, "bothOn.png")
bothOffIcon = os.path.join(iconRoot, "bothOff.png")

defaultColor = PySide.QtGui.QColor(0, 0, 0)
kwdsFgColour = PySide.QtGui.QColor(25, 25, 80)
stringLiteralsFgColourDQ = PySide.QtGui.QColor(150, 35, 35)
stringLiteralsFgColourSQ = PySide.QtGui.QColor(150, 35, 35)
commentsFgColour = PySide.QtGui.QColor(30, 75, 15)
defaultFont = PySide.QtGui.QFont("Courier")
defaultFont.setPointSize(12)

indent = "  "

class ScriptEditor(PySide.QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScriptEditor, self).__init__(parent)

        self.setWindowTitle( "Script Editor" )
        self.setObjectName( "foundry.ui.scripteditor" )

        #Make history stack
        self._historyStack = []
        self._currentStackItem = None

        #Make splitter
        self.splitter = PySide.QtGui.QSplitter(PySide.QtCore.Qt.Vertical)

        #Make output widget
        self._output = ScriptOutputWidget(parent=self)
        self._output.setReadOnly(1)
        self._output.setAcceptRichText(0)
        self._output.setTabStopWidth(self._output.tabStopWidth() / 4)
        self._output.setFocusPolicy(PySide.QtCore.Qt.ClickFocus)
        self._output.setAutoFillBackground( 0 )

        #Make input widget and set focus
        self._input = ScriptInputWidget(self._output, self, self)
        self._input.setTabStopWidth(self._input.tabStopWidth() / 4)
        self._input.setFocusPolicy(PySide.QtCore.Qt.StrongFocus)
        self._input.setFocus(PySide.QtCore.Qt.OtherFocusReason)
        self._editabledoc = self._input.document()
        self.setFocusProxy( self._input )

        self.updateFont(defaultFont)

        #Add highlighter
        self._highlighterInput = InputHighlighter(self._editabledoc, parent=self._input)

        #Add input and output to splitter
        self.splitter.addWidget(self._output)
        self.splitter.addWidget(self._input)
        self.splitter.setStretchFactor(0,0)

        #Buttons
        self.previousButton = self.createButton( "", previousIconPath )
        self.previousButton.setToolTip( "Previous script<br>Hotkey: " + FN_CTRLKEYNAME + "+[" )
        self.previousButton.setEnabled( 0 )
        self.previousButton.setProperty("group","left")
        self.previousButton.clicked.connect(self.previous)

        self.nextButton = self.createButton( "", nextIconPath )
        self.nextButton.setToolTip( "Next script<br>Hotkey: " + FN_CTRLKEYNAME + "+]" )
        self.nextButton.setEnabled( 0 )
        self.nextButton.setProperty("group","center")
        self.nextButton.clicked.connect(self.next)

        self.clearHistoryButton = self.createButton( "", clearHistoryIconPath )
        self.clearHistoryButton.setToolTip( "Clear history" )
        self.clearHistoryButton.setEnabled( 0 )
        self.clearHistoryButton.setProperty("group","right")
        self.clearHistoryButton.clicked.connect(self.clearHistory)

        self.sourceButton = self.createButton( "", sourceIconPath )
        self.sourceButton.setToolTip( "Source a script" )
        self.sourceButton.setProperty("group","left")
        self.sourceButton.clicked.connect(self.sourceScript)

        self.loadButton = self.createButton( "", loadIconPath )
        self.loadButton.setToolTip( "Load a script" )
        self.loadButton.setProperty("group","center")
        self.loadButton.clicked.connect(self.loadScript)

        self.saveButton = self.createButton( "", saveIconPath )
        self.saveButton.setToolTip( "Save a script" )
        self.saveButton.setProperty("group","center")
        self.saveButton.clicked.connect(self.saveScript)

        self.runButton = self.createButton( "", runIconPath )
        self.runButton.setToolTip( "Run the current script<br>Hotkey: " + FN_CTRLKEYNAME + "+Return" )
        self.runButton.setProperty("group","right")
        self.runButton.clicked.connect(self.runScript)

        self.clearOutputButton = self.createButton( "", clearOutputIconPath )
        self.clearOutputButton.setToolTip( "Clear output window<br>Hotkey: " + FN_CTRLKEYNAME + "+Backspace" )
        self.clearOutputButton.clicked.connect(self.clearOutput)

        self._inputButton = self.createButton( "", inputOnIcon, inputOffIcon )
        self._inputButton.setToolTip( "Show input only" )
        self._inputButton.setProperty("group","left")
        self._inputButton.setCheckable(1)

        self._outputButton = self.createButton( "", outputOnIcon, outputOffIcon )
        self._outputButton.setToolTip( "Show output only" )
        self._outputButton.setProperty("group","center")
        self._outputButton.setCheckable(1)

        self._bothButton = self.createButton( "", bothOnIcon, bothOffIcon )
        self._bothButton.setToolTip( "Show both input and output" )
        self._bothButton.setProperty("group","right")
        self._bothButton.setCheckable(1)
        self._bothButton.setChecked(1) # This is the default active button in the radio group.

        #Add buttons to button group
        self._layoutButtons = PySide.QtGui.QButtonGroup()
        self._layoutButtons.addButton(self._inputButton)
        self._layoutButtons.addButton(self._outputButton)
        self._layoutButtons.addButton(self._bothButton)

        self._inputButton.clicked.connect(self.setInputLayout)
        self._outputButton.clicked.connect(self.setOutputLayout)
        self._bothButton.clicked.connect(self.setBothLayout)

        #Setup button layout
        buttonLayout = PySide.QtGui.QHBoxLayout()
        buttonLayout.setContentsMargins( 2, 2, 2, 2 )
        buttonLayout.setSpacing( 0 )
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.clearHistoryButton)
        buttonLayout.addSpacing( 15 )
        buttonLayout.addWidget(self.sourceButton)
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.runButton)
        buttonLayout.addSpacing( 15 )
        buttonLayout.addWidget(self._inputButton)
        buttonLayout.addWidget(self._outputButton)
        buttonLayout.addWidget(self._bothButton)
        buttonLayout.addSpacing( 15 )
        buttonLayout.addWidget(self.clearOutputButton)
        buttonLayout.setAlignment(PySide.QtCore.Qt.AlignLeft)

        #Setup main layout
        layout = PySide.QtGui.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins( 2, 2, 2, 2 )
        layout.setSpacing( 2 )
        layout.addLayout(buttonLayout)
        layout.addWidget(self.splitter)

    def createButton(self, text, onIcon, offIcon=None):
        icon = PySide.QtGui.QIcon()
        icon.addFile(onIcon, PySide.QtCore.QSize(ICONSIZE, ICONSIZE), PySide.QtGui.QIcon.Normal, PySide.QtGui.QIcon.On)
        if offIcon :
            icon.addFile(offIcon, PySide.QtCore.QSize(ICONSIZE, ICONSIZE), PySide.QtGui.QIcon.Normal, PySide.QtGui.QIcon.Off)
        b = PySide.QtGui.QPushButton(icon, text)
        b.setFocusPolicy(PySide.QtCore.Qt.NoFocus)
        return b

    def previous(self) :

        #Store the current text in the array if the current stack item is none
        if not self._currentStackItem :
            self._historyStack.append(self._input.toPlainText())
            self._currentStackItem = len(self._historyStack) - 2
        else :
            self._currentStackItem -= 1

        #Replace the text with the select latest
        replacementText = self._historyStack[self._currentStackItem]
        self._input.setPlainText(replacementText)

        #Enable the next button
        self.nextButton.setEnabled(1)

        #If this is the first item in the history stack, disable the previous button
        if self._currentStackItem == 0 :
            self.previousButton.setEnabled(0)

    def next(self) :
        #Store the current text in the array if the current stack item is none
        self._currentStackItem += 1

        #Replace the text with the select latest
        replacementText = self._historyStack[self._currentStackItem]
        self._input.setPlainText(replacementText)

        #Enable the previous button
        self.previousButton.setEnabled(1)

        #If this is the last item in the history stack, disable the previous button
        if self._currentStackItem == (len(self._historyStack) - 1) :
            self.nextButton.setEnabled(0)

    def clearHistory(self) :
        self._historyStack = []
        self.previousButton.setEnabled(0)
        self.nextButton.setEnabled(0)
        self.clearHistoryButton.setEnabled(0)

    def sourceScript(self) :
        #Load script
        filename = PySide.QtGui.QFileDialog.getOpenFileName(self, 'Source Script...', os.path.expanduser('~'), "Python File (*.py)")[0]
        if filename == '' :
            return

        #Save text in input
        currentInputText = self._input.toPlainText()

        #Get text from file
        txt = open(filename)

        #Replace text in input
        self._input.setPlainText(txt.read())

        #Execute text in input
        self.runScript()

        #Restore original text
        self._input.setPlainText(currentInputText)

        return

    def loadScript(self) :

        #Load script
        filename = PySide.QtGui.QFileDialog.getOpenFileName(self, 'Load Script...', os.path.expanduser('~'), "Python File (*.py)")[0]
        if filename == '' :
            return

        #Store current text in history stack
        self._historyStack.append(self._input.toPlainText())
        self.previousButton.setEnabled(1)

        #Get text from file
        txt = open(filename)

        #Replace text in input
        self._input.setPlainText(txt.read())

        return

    def saveScript(self) :

        #Get text from input
        textToSave = self._input.toPlainText()

        #Get save path
        filename = PySide.QtGui.QFileDialog.getSaveFileName(self, 'Save Script...', os.path.expanduser('~'), "Python File (*.py)")[0]
        if filename == '' :
            return

        #Fix filename
        if not filename.endswith('.py') :
            filename = '%s.py' % filename

        #Write script
        try :
            fileToWrite = open(filename, 'w')
            fileToWrite.write(textToSave)
            fileToWrite.close()

            outputText = '%s\nSuccessfully saved to file : %s.\n' % (self._output.toPlainText(), filename)
            self._output.setPlainText(outputText)
        except : 
            outputText = '%s\n\Couldn\'t save to file : %s.\n' % (self._output.toPlainText(), filename)
            self._output.setPlainText(outputText)

        self._output.moveCursor(PySide.QtGui.QTextCursor.End)
        self._output.ensureCursorVisible()

        return


    def runScript(self) :
        self._input.runScript()

    def clearOutput(self) :
        self._output.clear()  
        self._input.highlightCurrentLine()

    def setInputLayout(self) :
        self._input.show()
        self._output.hide()

    def setOutputLayout(self) :
        self._input.hide()
        self._output.show()


    def setBothLayout(self) :
        self._input.show()
        self._output.show()

    def updateFont(self, font):
      tc = self._output.textCursor()
      tc.select(PySide.QtGui.QTextCursor.Document)
      self._output.setTextCursor(tc)
      self._output.setCurrentFont(font)
      tc.clearSelection()
      self._output.setTextCursor(tc)
      self._output.document().setDefaultFont(font)

      tc = self._input.textCursor()
      tc.select(PySide.QtGui.QTextCursor.Document)
      self._input.setTextCursor(tc)
      tc.clearSelection()
      self._input.setTextCursor(tc)
      self._editabledoc.setDefaultFont(font)

#Need to add in the proper methods here
class ScriptOutputWidget(PySide.QtGui.QTextEdit) :
    def __init__(self, parent=None):
        super(ScriptOutputWidget, self).__init__(parent)

        #Setup mutex vars
        _pendingMutex = None
        _pendingOutput = None

        self.setSizePolicy(PySide.QtGui.QSizePolicy.Expanding, PySide.QtGui.QSizePolicy.Expanding)

    def paintEvent(self, event):
        PySide.QtGui.QTextEdit.paintEvent(self, event)

    def keyPressEvent(self, event) :
        PySide.QtGui.QTextEdit.keyPressEvent(self, event)

    def updateOutput(self, text) : 
        self.moveCursor(PySide.QtGui.QTextCursor.End)
        self.insertPlainText(text)
        self.moveCursor(PySide.QtGui.QTextCursor.End)


#Need to add in the proper methods here
class ScriptInputWidget(PySide.QtGui.QPlainTextEdit) :
    def __init__(self, output, editor, parent=None):
        super(ScriptInputWidget, self).__init__(parent)

        #Setup vars
        self._output = output
        self._editor = editor
        self._errorLine = 0
        self._showErrorHighlight = True
        self._completer = None
        self._currentCompletion = None
        self._completerShowing = False
        self._showLineNumbers = True

        self.setSizePolicy(PySide.QtGui.QSizePolicy.Expanding, PySide.QtGui.QSizePolicy.Expanding)

        #Setup completer
        self._completer = PySide.QtGui.QCompleter(self)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(PySide.QtGui.QCompleter.UnfilteredPopupCompletion)
        self._completer.setCaseSensitivity(PySide.QtCore.Qt.CaseSensitive)
        self._completer.setModel(PySide.QtGui.QStringListModel())

        #Setup line numbers
        self._lineNumberArea = LineNumberArea(self, parent=self)

        #Setup connections
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self._completer.activated.connect(self.insertCompletion)
        self._completer.highlighted.connect(self.completerHighlightChanged)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)

        self.updateLineNumberAreaWidth()
        self._lineNumberArea.setVisible( self._showLineNumbers )

    def lineNumberAreaWidth(self) :

        if not self._showLineNumbers :
            return 0

        digits = 1
        maxNum = max(1, self.blockCount())
        while (maxNum >= 10) :
            maxNum /= 10
            digits += 1

        space = 5 + self.fontMetrics().width('9') * digits
        return space


    def updateLineNumberAreaWidth(self) :
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy) :
        if (dy) :
            self._lineNumberArea.scroll(0, dy)
        else :
            self._lineNumberArea.update(0, rect.y(), self._lineNumberArea.width(), rect.height())

        if (rect.contains(self.viewport().rect())) :
            self.updateLineNumberAreaWidth()


    def resizeEvent(self, event) :
        PySide.QtGui.QPlainTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self._lineNumberArea.setGeometry(PySide.QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event) :

        painter = PySide.QtGui.QPainter(self._lineNumberArea)
        #painter.fillRect(event.rect(), self.palette().base())

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int( self.blockBoundingGeometry(block).translated(self.contentOffset()).top() )
        bottom = top + int( self.blockBoundingRect(block).height() )
        currentLine = self.document().findBlock(self.textCursor().position()).blockNumber()

        font = painter.font()
        pen = painter.pen()
        painter.setPen( self.palette().color(PySide.QtGui.QPalette.Text) )

        while (block.isValid() and top <= event.rect().bottom()) :

            if (block.isVisible() and bottom >= event.rect().top()) :

                if ( blockNumber == currentLine ) :
                    painter.setPen(PySide.QtGui.QColor(255, 255, 255))
                    font.setBold(True)
                    painter.setFont(font)

                elif ( blockNumber == int(self._errorLine) - 1 ) :
                    painter.setPen(PySide.QtGui.QColor(127, 0, 0))
                    font.setBold(True)
                    painter.setFont(font)

                else :
                    painter.setPen(PySide.QtGui.QColor(75, 75, 75))
                    font.setBold(False)
                    painter.setFont(font)

                number = "%s" % str(blockNumber + 1)
                painter.drawText(0, top, self._lineNumberArea.width(), self.fontMetrics().height(), PySide.QtCore.Qt.AlignRight, number)

            #Move to the next block
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1


    def highlightCurrentLine(self) :

        extraSelections = []

        if (self._showErrorHighlight and not self.isReadOnly()) :
            selection = PySide.QtGui.QTextEdit.ExtraSelection()

            lineColor = PySide.QtGui.QColor(255, 255, 255, 40)            

            selection.format.setBackground(lineColor)
            selection.format.setProperty(PySide.QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)
        self._errorLine = 0


    def highlightErrorLine(self) :

        extraSelections = []

        if (self._showErrorHighlight and not self.isReadOnly()) :
            if (self._errorLine != 0) :
                selection = PySide.QtGui.QTextEdit.ExtraSelection()

                selection.format.setBackground(PySide.QtGui.QColor(255, 0, 0, 40))
                selection.format.setProperty(PySide.QtGui.QTextFormat.OutlinePen, PySide.QtGui.QPen(PySide.QtGui.QColor(127, 0, 0, 0)))
                selection.format.setProperty(PySide.QtGui.QTextFormat.FullWidthSelection, True)
                
                pos = self.document().findBlockByLineNumber(int(self._errorLine)-1).position()
                cursor = self.textCursor()
                cursor.setPosition(pos)
                
                selection.cursor = cursor
                selection.cursor.clearSelection()
                extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event) :

        #Get the key being pressed
        ctrlToggled = ((event.modifiers() and (PySide.QtCore.Qt.ControlModifier)) != 0)
        altToggled = ((event.modifiers() and (PySide.QtCore.Qt.AltModifier)) != 0)
        shiftToggled = ((event.modifiers() and (PySide.QtCore.Qt.ShiftModifier)) != 0)
        keyBeingPressed = event.key()

        #Get completer state
        self._completerShowing = self._completer.popup().isVisible()
        
        #If the completer is showing
        if self._completerShowing :
            tc = self.textCursor()
            #If we're hitting enter, do completion
            if keyBeingPressed == PySide.QtCore.Qt.Key_Return or keyBeingPressed == PySide.QtCore.Qt.Key_Enter :
                self.insertCompletion(self._currentCompletion)
                self._currentCompletion = ""
                self._completer.popup().hide()
                self._completerShowing = False

                #Disable the next button and set current stack item to none
                self._editor.nextButton.setEnabled(0)
                self._editor._currentStackItem = None

            #If you're hitting right or escape, hide the popup
            elif keyBeingPressed == PySide.QtCore.Qt.Key_Right or keyBeingPressed == PySide.QtCore.Qt.Key_Escape:
                self._completer.popup().hide()
                self._completerShowing = False
            #If you hit tab, escape or ctrl-space, hide the completer
            elif keyBeingPressed == PySide.QtCore.Qt.Key_Tab or keyBeingPressed == PySide.QtCore.Qt.Key_Escape or (ctrlToggled and keyBeingPressed == PySide.QtCore.Qt.Key_Space) :
                self._currentCompletion = ""
                self._completer.popup().hide()
                self._completerShowing = False
            #If none of the above, update the completion model
            else :
                PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)
                #Edit completion model
                colNum = tc.columnNumber()
                posNum = tc.position()
                inputText = self.toPlainText()
                inputTextSplit = inputText.splitlines()
                runningLength = 0
                currentLine = None
                for line in inputTextSplit :
                    length = len(line)
                    runningLength += length
                    if runningLength >= posNum : 
                        currentLine = line
                        break
                    runningLength += 1
                if currentLine : 
                    token = currentLine.split(" ")[-1]
                    if "(" in token :
                            token = token.split("(")[-1]
                    self.completeTokenUnderCursor(token)
            return

        #If the completer is not showing
        #If you hit ctrl-enter or ctrl-return, run the script
        if (ctrlToggled and (keyBeingPressed == PySide.QtCore.Qt.Key_Return or keyBeingPressed == PySide.QtCore.Qt.Key_Enter)) :
            if (self._editor) :
                self._editor.runScript()
            return

        #Add auto indent on enter if ':' is the last character of the previous line
        if keyBeingPressed == PySide.QtCore.Qt.Key_Return or keyBeingPressed == PySide.QtCore.Qt.Key_Enter :
            PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)

            tc = self.textCursor()
            tc.movePosition(PySide.QtGui.QTextCursor.Up)
            previousLine = tc.block().text()
            if previousLine.endswith(':') or previousLine.endswith(': ')  :
                previousLineTabCount = len(previousLine.split(indent))
                self.insertPlainText(indent*previousLineTabCount)

            #Disable the next button
            self._editor.nextButton.setEnabled(0)
            self._editor._currentStackItem = None

            return


        #Add support for increasing/decreasing indentation on selected
        if (ctrlToggled or shiftToggled) and keyBeingPressed == PySide.QtCore.Qt.Key_BraceLeft :
            self.decreaseIndentationSelected()

            #Disable the next button
            self._editor.nextButton.setEnabled(0)
            self._editor._currentStackItem = None

            return

        if (ctrlToggled or shiftToggled) and keyBeingPressed == PySide.QtCore.Qt.Key_BraceRight :
            self.increaseIndentationSelected()

            #Disable the next button
            self._editor.nextButton.setEnabled(0)
            self._editor._currentStackItem = None

            return

        #Add support for commenting out selected code
        if ctrlToggled and keyBeingPressed == PySide.QtCore.Qt.Key_Slash :
            self.commentSelected()

            #Disable the next button
            self._editor.nextButton.setEnabled(0)
            self._editor._currentStackItem = None

            return

        #Add support for clearing output
        if ctrlToggled and keyBeingPressed == PySide.QtCore.Qt.Key_Backspace : 
            self._editor.clearOutput()
            return

        #Add support for copy/paste
        if ctrlToggled and (keyBeingPressed == PySide.QtCore.Qt.Key_V or keyBeingPressed == PySide.QtCore.Qt.Key_C):
            PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)
            return

        #Now add tab key support
        if (ctrlToggled or shiftToggled) and keyBeingPressed == PySide.QtCore.Qt.Key_Tab : 
            self.decreaseIndentationSelected()

            #Disable the next button
            self._editor.nextButton.setEnabled(0)
            self._editor._currentStackItem = None

            return

        if not ctrlToggled and not altToggled and not shiftToggled and keyBeingPressed == PySide.QtCore.Qt.Key_Tab :
            #Get text cursor
            tc = self.textCursor()

            #If there is a selection, increase the indentation and return
            if tc.hasSelection() :
                self.increaseIndentationSelected()

                #Disable the next button
                self._editor.nextButton.setEnabled(0)
                self._editor._currentStackItem = None

                return 

            #If there's no selection
            colNum = tc.columnNumber()
            posNum = tc.position()

            allCode = self.toPlainText()

            #...and if there's text in the editor
            if len(allCode.split()) > 0 : 
                #There is text in the editor
                currentLine = tc.block().text()

                #If you're not at the end of the line just add a tab
                if colNum < len(currentLine) :
                    #If there isn't a ')' directly to the right of the cursor add a tab
                    if currentLine[colNum:colNum+1] != ')' :
                        PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)

                        #Disable the next button
                        self._editor.nextButton.setEnabled(0)
                        self._editor._currentStackItem = None

                        return
                    #Else show the completer
                    else : 
                        token = currentLine[:colNum].split(" ")[-1]
                        if "(" in token :
                            token = token.split("(")[-1]

                        self.completeTokenUnderCursor(token)

                        #Disable the next button
                        self._editor.nextButton.setEnabled(0)
                        self._editor._currentStackItem = None

                        return

                #If you are at the end of the line, 
                else : 
                    #If there's nothing to the right of you add a tab
                    if currentLine[colNum-1:] == "" :
                        PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)

                        #Disable the next button
                        self._editor.nextButton.setEnabled(0)
                        self._editor._currentStackItem = None

                        return

                    #Else update token and show the completer
                    token = currentLine.split(" ")[-1]
                    if "(" in token :
                        token = token.split("(")[-1]

                    self.completeTokenUnderCursor(token)

                    #Disable the next button
                    self._editor.nextButton.setEnabled(0)
                    self._editor._currentStackItem = None

                    return

            #...else just add in a tab
            else : 
                PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)

                #Disable the next button
                self._editor.nextButton.setEnabled(0)
                self._editor._currentStackItem = None

                return

        #If we get to here just accept the keypress
        PySide.QtGui.QPlainTextEdit.keyPressEvent(self, event)

        #Disable the next button
        self._editor.nextButton.setEnabled(0)
        self._editor._currentStackItem = None

        return

    def canInsertFromMimeData(self, source):

      if source.hasUrls():
        urls = source.urls()
        return len(urls) != 0 and len(urls[0].toLocalFile()) != 0

      if source.hasFormat("text/x-python"):
        return True

      return PySide.QtGui.QPlainTextEdit.canInsertFromMimeData(self, source)

    def insertFromMimeData(self, mimeData):

      hasPython = mimeData.hasFormat("text/x-python")
      if mimeData.hasUrls() and not hasPython:
        path = mimeData.urls()[0].toLocalFile()
        if len(path) != 0:
          file = PySide.QtCore.QFile(path)
          if file.open( PySide.QtCore.QIODevice.ReadOnly | PySide.QtCore.QIODevice.Text ):
            stream = PySide.QtCore.QTextStream( file )
            text = stream.read( 128*1024 ) # Limit size in case people drop big binary files on it by accident
            # Check that it was really text
            if not all(c in string.printable for c in text):
              return
            self.textCursor().insertText(text)
        return

      # Check if we're trying to paste text in
      if mimeData.hasText() or hasPython:
        # We are.  Grab it, and do a simple search/replace
        if hasPython:
          text = mimeData.data("text/x-python")
        else:
          text = mimeData.text()
        text.replace("\t", indent)
        # Prepare to paste in
        modifiedData = PySide.QtCore.QMimeData()
        modifiedData.setText(text)
        mimeData = modifiedData

      PySide.QtGui.QPlainTextEdit.insertFromMimeData(self, mimeData)

    def commentSelected(self) :

        tc = self.textCursor()

        #Get selection stats
        selStart = tc.selectionStart()
        selEnd = tc.selectionEnd()

        #Get selection split to lines
        if selStart == selEnd :
            selectedText = tc.block().text()
        else : 
            selectedText = tc.selectedText()

        selectedSplit = selectedText.splitlines()

        #Are we commenting/uncommenting
        if selectedSplit[0].startswith('#') :
            mode = 'uncommenting'
        else :
            mode = 'commenting'

        print mode

        newLines = []
        alteredLinesCount = 0
        for line in selectedSplit :
            #If there is a '\t' at the start of the line, remove it
            if mode == 'commenting' :
                newLines.append('#%s' % line)
                alteredLinesCount+=1
            else : 
                alteredLine = line.replace('#', '', 1)
                alteredLinesCount+=1
                newLines.append(alteredLine)

        #Combine all sections
        newSelected = '\n'.join(newLines)

        #Replace text
        if selStart == selEnd :
            #Delete current block before inserting
            tc.select(PySide.QtGui.QTextCursor.BlockUnderCursor)
            tc.insertText('\n%s' % newSelected)
        else :
            tc.insertText(newSelected)

        #If there was no selection, just move cursor
        if selStart == selEnd :
            if mode == 'commenting' :
                tc.setPosition(selStart+1)
            else :
                tc.setPosition(selStart-1)
        else : 
            if mode == 'commenting' :
                tc.setPosition(selStart)
                tc.setPosition(selEnd+alteredLinesCount, PySide.QtGui.QTextCursor.KeepAnchor)
            else : 
                tc.setPosition(selStart)
                tc.setPosition(selEnd-alteredLinesCount, PySide.QtGui.QTextCursor.KeepAnchor)
        
        self.setTextCursor(tc)

        return

    def increaseIndentationSelected(self) :
        
        tc = self.textCursor()

        #Get selection stats
        selStart = tc.selectionStart()
        selEnd = tc.selectionEnd()

        #Get selection split to lines
        selectedText = tc.selectedText()
        selectedSplit = selectedText.splitlines()

        #Add tab to start of lines
        newLines = []
        for line in selectedSplit :
            newLines.append('\t%s' % line)

        #Combine all sections
        newSelected = '\n'.join(newLines)

        #Replace text
        tc.insertText(newSelected)

        #Reselect
        tc.setPosition(selStart)
        tc.setPosition(selEnd+(len(selectedSplit)), PySide.QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(tc)

        return 

    def decreaseIndentationSelected(self):

        tc = self.textCursor()

        #Get selection stats
        selStart = tc.selectionStart()
        selEnd = tc.selectionEnd()

        #Get selection split to lines
        if selStart == selEnd :
            selectedText = tc.block().text()
        else : 
            selectedText = tc.selectedText()

        selectedSplit = selectedText.splitlines()

        #Remove tab from start of lines
        newLines = []
        alteredLinesCount = 0
        for line in selectedSplit :
            #If there is a '\t' at the start of the line, remove it
            if line.startswith('\t') :
                alteredLine = line.replace('\t', '', 1)
                alteredLinesCount+=1
                newLines.append(alteredLine)
            elif line.startswith(' ' * FN_SPACESINTAB) :
                alteredLine = line.replace(' ' * FN_SPACESINTAB, '', 1)
                alteredLinesCount+=1
                newLines.append(alteredLine)
            #Else just leave it as it is
            else : 
                newLines.append(line)

        #Combine all sections
        newSelected = '\n'.join(newLines)

        #Replace text
        if selStart == selEnd :
            #Delete current block before inserting
            tc.select(PySide.QtGui.QTextCursor.BlockUnderCursor)
            tc.insertText('\n%s' % newSelected)
            return
        tc.insertText(newSelected)

        #Reselect
        tc.setPosition(selStart)
        tc.setPosition(selEnd-alteredLinesCount, PySide.QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(tc)

        return

    def completionsForToken(self, token):
        def findModules(searchString):
            sysModules =  sys.modules
            globalModules = globals()
            allModules = dict(sysModules, **globalModules)
            allKeys = list(set(globals().keys() + sys.modules.keys()))
            allKeysSorted = [x for x in sorted(set(allKeys))]

            if searchString == '' :	
                matching = []
                for x in allModules :
                    if x.startswith(searchString) :
                        matching.append(x)
                return matching
            else : 
                try : 
                    if sys.modules.has_key(searchString) :
                        return dir(sys.modules['%s' % searchString])
                    elif globals().has_key(searchString): 
                        return dir(globals()['%s' % searchString])
                    else : 
                        return []
                except :
                    return None

        completerText = token

        #Get text before last dot
        moduleSearchString = '.'.join(completerText.split('.')[:-1])

        #Get text after last dot
        fragmentSearchString = completerText.split('.')[-1] if completerText.split('.')[-1] != moduleSearchString else ''

        #Get all the modules that match module search string
        allModules = findModules(moduleSearchString)

        #If no modules found, do a dir
        if not allModules :
            if len(moduleSearchString.split('.')) == 1 :
                matchedModules = []
            else :
                try : 
                    trimmedModuleSearchString = '.'.join(moduleSearchString.split('.')[:-1])
                    matchedModules = [x for x in dir(getattr(sys.modules[trimmedModuleSearchString], moduleSearchString.split('.')[-1])) if '__' not in x and x.startswith(fragmentSearchString)]
                except : 
                    matchedModules = []
        else : 
            matchedModules = [x for x in allModules if '__' not in x and x.startswith(fragmentSearchString)]

        return matchedModules

    def completeTokenUnderCursor(self, token) :

        #Clean token
        token = token.lstrip().rstrip()

        completionList = self.completionsForToken(token)
        if len(completionList) == 0 :
            return

        #Set model for _completer to completion list
        self._completer.model().setStringList(completionList)

        #Set the prefix
        self._completer.setCompletionPrefix(token)

        #Check if we need to make it visible
        if self._completer.popup().isVisible() :
            rect = self.cursorRect()
            rect.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
            self._completer.complete(rect)
            return

        #Make it visible
        if len(completionList) == 1 :
            self.insertCompletion(completionList[0])
        else :
            rect = self.cursorRect()
            rect.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
            self._completer.complete(rect)

        return 

    def insertCompletion(self, completion):
        if completion :
            token = self._completer.completionPrefix()
            if len(token.split('.')) == 0 : 
                tokenFragment = token
            else :
                tokenFragment = token.split('.')[-1]

            textToInsert = completion[len(tokenFragment):]
            tc = self.textCursor()
            tc.insertText(textToInsert)
        return
        
    def completerHighlightChanged(self, highlighted):
        self._currentCompletion = highlighted

    def getErrorLineFromTraceback(self, tracebackStr) : 
        finalLine = None
        for line in tracebackStr.split('\n') :    
            if 'File "<string>", line' in line :
                finalLine = line
        if finalLine == None :
            return 0
        try :
            errorLine = finalLine.split(',')[1].split(' ')[2]
            return errorLine
        except : 
            return 0

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

#Need to add in the proper methods here
class InputHighlighter(PySide.QtGui.QSyntaxHighlighter) :
    def __init__(self, doc, parent=None):

        super(InputHighlighter, self).__init__(parent)

        self.setDocument(doc)

        self._rules = []
        self._keywords = PySide.QtGui.QTextCharFormat()
        self._strings = PySide.QtGui.QTextCharFormat()
        self._stringSingleQuotes = PySide.QtGui.QTextCharFormat()
        self._comment = PySide.QtGui.QTextCharFormat()

        self._keywords.setForeground(kwdsFgColour)
        self._keywords.setFontWeight(PySide.QtGui.QFont.Bold)

        #Construct rules for keywords
        keywordPatterns = []
        for pattern in ["\\band\\b","\\bas\\b","\\bassert\\b"
                    ,"\\bbreak\\b","\\bclass\\b","\\bcontinue\\b"
                   ,"\\bdef\\b","\\bdel\\b","\\belif\\b","\\belse\\b"
                   ,"\\bexcept\\b","\\bexec\\b","\\bfinally\\b","\\bfor\\b"
                   ,"\\bfrom\\b","\\bglobal\\b","\\bif\\b","\\bimport\\b"
                   ,"\\bin\\b","\\bis\\b","\\blambda\\b","\\bnot\\b"
                   ,"\\bor\\b","\\bpass\\b","\\bprint\\b","\\braise\\b"
                   ,"\\breturn\\b","\\btry\\b","\\bwhile\\b","\\bwith\\b"
                   ,"\\byield\\b"
                   ,"\\bTrue\\b","\\bFalse\\b"
                   ,"\\bint\\b","\\bfloat\\b"] :
                   rule = {}
                   rule['pattern'] = pattern
                   rule['format'] = self._keywords
                   self._rules.append(rule)

        #String Literals
        self._strings.setForeground(stringLiteralsFgColourDQ)
        rule = {}
        rule['pattern'] = "\"([^\"\\\\]|\\\\.)*\""
        rule['format'] = self._strings
        self._rules.append(rule)

        #String single quotes
        self._stringSingleQuotes.setForeground(stringLiteralsFgColourSQ)
        rule = {}
        rule['pattern'] = "'([^'\\\\]|\\\\.)*'"
        rule['format'] = self._stringSingleQuotes
        self._rules.append(rule)

        #Comments
        self._comment.setForeground(commentsFgColour)
        rule = {}
        rule['pattern'] = "#[^\n]*"
        rule['format'] = self._comment
        self._rules.append(rule)


    def highlightBlock(self, text) :

        text = str(text)

        for rule in self._rules :
            expression = rule['pattern']
            
            if len(text) > 0 : 
                results = re.finditer(expression, text)

                #Loop through all results
                for result in results : 
                    index = result.start()
                    length = result.end() - result.start()
                    self.setFormat(index, length, rule['format'])

class LineNumberArea(PySide.QtGui.QWidget):
    def __init__(self, scriptInputWidget, parent=None):
        super(LineNumberArea, self).__init__(parent)

        self._scriptInputWidget = scriptInputWidget
        self.setStyleSheet("text-align: center;")

    def sizeHint(self) :
        return PySide.QtCore.QSize(self._scriptInputWidget.lineNumberAreaWidth(), 0)

    def paintEvent(self, event) :
        self._scriptInputWidget.lineNumberAreaPaintEvent(event)
        return
