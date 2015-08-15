import PySide

from PySide import QtCore, QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QPlainTextEdit

keywords = {
    "functions" : [
        "time", "rand", "step", "randVec", "norm", "vecAngle", "angleVec", "cycle", 
        "wrap", "ease", "easeDelta", "sprite", "abs", "cos", "sin", "tan"
    ],

    "particle" : [
        "p.x", "p.y", "p.dx", "p.dy"
    ],

    "sprite" : [
        "sp.x", "sp.y", "sp.sx", "sp.sy", "sp.r", "sp.g", "sp.b", "sp.glow", "sp.idx", "sp.opacity", "sp.rot"
    ],

    # EaseTypes 
    "easetypes" : [
        "EaseType.EASE_IN", "EaseType.EASE_OUT", "EaseType.FLAT", "EaseType.LINEAR", "EaseType.SHARP_EASE_IN", 
        "EaseType.SHARP_EASE_OUT", "EaseType.EXTRA_SHARP_EASE_IN", "EaseType.EXTRA_SHARP_EASE_OUT", "EaseType.SHARP_SMOOTH", 
        "EaseType.SMOOTH", "EaseType.SOFT_EASE_IN", "EaseType.SOFT_EASE_OUT", "EaseType.SOFT_SMOOTH", "EaseType.SINE_EASE_IN", 
        "EaseType.SINE_EASE_OUT", "EaseType.SINE_SMOOTH", "EaseType.CIRC_EASE_IN", "EaseType.CIRC_EASE_OUT", "EaseType.CIRC_SMOOTH", 
        "EaseType.BOUNCE_IN", "EaseType.BOUNCE_OUT", "EaseType.BOUNCE_SMOOTH", "EaseType.ELASTIC_IN", "EaseType.ELASTIC_OUT", 
        "EaseType.ELASTIC_SMOOTH", "EaseType.BACK_EASE_IN", "EaseType.BACK_EASE_OUT", "EaseType.BACK_SMOOTH"
    ]
}

class Highlighter(QtGui.QSyntaxHighlighter):
    dark = {
        "light-gray":   "#CCC",
        "gray":         "#888",
        "dark-gray":    "#282828",
        "yellow":       "#E6DB74",
        "blue":         "#66D9EF",
        "red":          "#F92672",
        "purple":       "#AE81FF",
        "orange":       "#FD971F",
        "green":        "#A6E22E",
    }
    bright = {
        "blue":     "#0000bb",
        "purple":   "#9128b1",
        "orange":   "#0066cc",
        "red":      "#af1212",
        "yellow":   "#007700",
        "gray":     "#AAB",
    }

    def __init__(self, *args):
        super(Highlighter, self).__init__(*args)

        self.keywordFormat = QtGui.QTextCharFormat()
        self.constantsFormat = QtGui.QTextCharFormat()
        self.builtinRegFormat = QtGui.QTextCharFormat()
        self.commentFormat = QtGui.QTextCharFormat()
        self.operatorFormat = QtGui.QTextCharFormat()
        self.quotationFormat = QtGui.QTextCharFormat()

        keywordPatterns = ["\\b%s\\b" % x for x in keywords['functions']]
        constantsPatterns = ["\\b%s\\b" % x for x in keywords['easetypes']]
        # numbers (int, float, hex)
        constantsPatterns.append("\\b(0x[a-fA-F\d]+|\d+(\.\d+)?([eE]-?\d+)?)\\b")
        constantsPatterns.append("\\bEaseType\\b")

        builtinRegPatters = ["\\b%s\\b" % x for x in keywords['particle']]
        builtinRegPatters.extend(["\\b%s\\b" % x for x in keywords['sprite']])
        builtinRegPatters.extend(('\\bp\\b', '\\bsp\\b'))

        self.highlightingRules = []
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), self.keywordFormat) for pattern in keywordPatterns] )
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), self.constantsFormat) for pattern in constantsPatterns] )
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), self.builtinRegFormat) for pattern in builtinRegPatters] )

        self.highlightingRules.append((QtCore.QRegExp("[\\+\\-\\*/=]"), self.operatorFormat))
        self.highlightingRules.append((QtCore.QRegExp("\".*\""), self.quotationFormat))
        self.highlightingRules.append((QtCore.QRegExp("--[^\n]*"), self.commentFormat))

        self.applyDarkTheme(False)

    def applyDarkTheme(self, dark):
        theme = self.dark if dark else self.bright 
        self.keywordFormat.setForeground ( QtGui.QColor(theme['blue']) )
        self.commentFormat.setForeground ( QtGui.QColor(theme['gray']) )
        self.operatorFormat.setForeground ( QtGui.QColor(theme['red']) )
        self.constantsFormat.setForeground ( QtGui.QColor(theme['purple']) )
        self.quotationFormat.setForeground ( QtGui.QColor(theme['yellow']) )
        self.builtinRegFormat.setForeground ( QtGui.QColor(theme['orange']) )

        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class ParticleScriptCompleter(QtGui.QCompleter):
    currentModel = None

    def __init__(self, parent=None):
        super(ParticleScriptCompleter, self).__init__(parent = parent)

        default = list(keywords['functions'])
        default.append('EaseType')

        self.defaultModel = QtGui.QStringListModel(default)
        self.particleModel = QtGui.QStringListModel(keywords['particle'])
        self.spriteModel = QtGui.QStringListModel(keywords['sprite'])
        self.easeModel = QtGui.QStringListModel(keywords['easetypes'])

        self.setModel(self.defaultModel)

    def setCompletionPrefix(self, prefix):
        lower = prefix.lower()
        
        if lower.startswith("sp."):
            self.setCurrentModel(self.spriteModel)
        elif lower.startswith("p."):
            self.setCurrentModel(self.particleModel)
        elif lower.startswith("easetype."):
            self.setCurrentModel(self.easeModel)
        else:
            self.setCurrentModel(self.defaultModel)

        super(ParticleScriptCompleter, self).setCompletionPrefix(prefix)


    def setCurrentModel(self, model):
        if self.currentModel != model:
            self.currentModel = model
            self.setModel(model)


class ParticleScriptEditor (QPlainTextEdit):
    completer = None

    def __init__(self, parent=None):
        super(ParticleScriptEditor, self).__init__(parent)

        self.highlighter = Highlighter(self.document())
        self.setCompleter(ParticleScriptCompleter(self))

    def setCompleter(self, completer):
        if self.completer:
            self.completer.activated.disconnect(self.insertCompletion)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()

        # replace prefix completion wariant (this is to fix case)
        prefix = self.completer.completionPrefix()
        tc.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor, len(prefix))
        tc.removeSelectedText()
        tc.insertText(completion)
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        pos = tc.position()
        tc.select(QtGui.QTextCursor.WordUnderCursor)

        # Don't treat dot (.) as word separator. It should be included into the completer prefix (sp. p. EaseType.)
        # Hacky way: select previous character, and if it is dot then add one more word to selection
        start = tc.selectionStart()
        end = tc.selectionEnd()

        if start > 0:
            tc.setPosition(end, QtGui.QTextCursor.MoveAnchor)
            tc.setPosition(start - 1, QtGui.QTextCursor.KeepAnchor)

        selection = tc.selectedText()
        if selection and selection[0] == '.':
            tc.movePosition(QtGui.QTextCursor.PreviousWord, QtGui.QTextCursor.KeepAnchor)
        else:
            tc.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
        
        return tc.selectedText()

    def isCursorAtWordEnd(self):
        tc = self.textCursor()
        pos = tc.position()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectionEnd() == pos

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        super(ParticleScriptEditor, self).focusInEvent(event)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.StyleChange:
            wnd = QtCore.QCoreApplication.instance().mainWindow
            self.completer.popup().setStyleSheet(wnd.styleSheet())
            self.highlighter.applyDarkTheme(wnd.useDarkSkin)
            
        super(ParticleScriptEditor, self).changeEvent(event)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        # has ctrl-E been pressed??
        isShortcut = event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_E
        if not self.completer or not isShortcut:
            super(ParticleScriptEditor, self).keyPressEvent(event)

        # ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier)
        if ctrlOrShift and not event.text():
            return

        hasModifier = (event.modifiers() != QtCore.Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        eow = "~!@#$%^&*()_+{}|:\"<>?,/;'[]\\-=" #end of word
        endOfWord = not event.text() or event.text()[-1] in eow
        lowLetterCount = len(completionPrefix) < 1

        if not isShortcut and (not self.isCursorAtWordEnd() or hasModifier or endOfWord or lowLetterCount):
            self.completer.popup().hide()
            return

        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!


