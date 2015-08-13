import PySide

from PySide import QtCore, QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QPlainTextEdit

keywords = [
    # functions
    "time", "rand", "step", "randVec", "norm", "vecAngle", "angleVec", "cycle", 
    "wrap", "ease", "easeDelta", "sprite", "abs", "cos", "sin", "tan",

    # sprite & particles registers
    "p.x", "p.y", "p.dx", "p.dy", "sp.x", "sp.y", "sp.sx", "sp.sy", 
    "sp.r", "sp.g", "sp.b", "sp.glow", "sp.idx", "sp.opacity", "sp.rot",

    # EaseTypes 
    "EaseType.EASE_IN", "EaseType.EASE_OUT", "EaseType.FLAT", "EaseType.LINEAR", "EaseType.SHARP_EASE_IN", 
    "EaseType.SHARP_EASE_OUT", "EaseType.EXTRA_SHARP_EASE_IN", "EaseType.EXTRA_SHARP_EASE_OUT", "EaseType.SHARP_SMOOTH", 
    "EaseType.SMOOTH", "EaseType.SOFT_EASE_IN", "EaseType.SOFT_EASE_OUT", "EaseType.SOFT_SMOOTH", "EaseType.SINE_EASE_IN", 
    "EaseType.SINE_EASE_OUT", "EaseType.SINE_SMOOTH", "EaseType.CIRC_EASE_IN", "EaseType.CIRC_EASE_OUT", "EaseType.CIRC_SMOOTH", 
    "EaseType.BOUNCE_IN", "EaseType.BOUNCE_OUT", "EaseType.BOUNCE_SMOOTH", "EaseType.ELASTIC_IN", "EaseType.ELASTIC_OUT", 
    "EaseType.ELASTIC_SMOOTH", "EaseType.BACK_EASE_IN", "EaseType.BACK_EASE_OUT", "EaseType.BACK_SMOOTH",
]

class Highlighter(QtGui.QSyntaxHighlighter):
    monokai = {
        "light-gray":   "#CCC",
        "gray":         "#888",
        "dark-gray":    "#282828",
        "yellow":       "#E6DB74",
        "blue":         "#66D9EF",
        "pink":         "#F92672",
        "purple":       "#AE81FF",
        "orange":       "#FD971F",
        "green":        "#A6E22E",
        "sea-green":    "#529B2F",
    }
    bright = {

    }

    def __init__(self, *args):
        super(Highlighter, self).__init__(*args)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QColor(self.monokai['blue']))

        constantsFormat = QtGui.QTextCharFormat()
        constantsFormat.setForeground(QtGui.QColor(self.monokai['purple']))

        builtinRegFormat = QtGui.QTextCharFormat()
        builtinRegFormat.setForeground(QtGui.QColor(self.monokai['orange']))

        keywordPatterns = [ 
            "\\btime\\b", "\\brand\\b", "\\bstep\\b", 
            "\\brandVec\\b", "\\bnorm\\b", "\\bvecAngle\\b", 
            "\\bangleVec\\b", "\\bcycle\\b", "\\bwrap\\b", 
            "\\bease\\b", "\\beaseDelta\\b", "\\bsprite\\b", 
            "\\babs\\b", "\\bcos\\b", "\\bsin\\b", "\\btan\\b"
        ]

        constantsPatterns = [
            "\\b(0x[a-fA-F\d]+|\d+(\.\d+)?([eE]-?\d+)?)\\b", # numbers (int, float, hex)
            "\\bEaseType.EASE_IN\\b",
            "\\bEaseType.EASE_OUT\\b",
            "\\bEaseType.FLAT\\b",
            "\\bEaseType.LINEAR\\b",
            "\\bEaseType.SHARP_EASE_IN\\b",
            "\\bEaseType.SHARP_EASE_OUT\\b",
            "\\bEaseType.EXTRA_SHARP_EASE_IN\\b",
            "\\bEaseType.EXTRA_SHARP_EASE_OUT\\b",
            "\\bEaseType.SHARP_SMOOTH\\b",
            "\\bEaseType.SMOOTH\\b",
            "\\bEaseType.SOFT_EASE_IN\\b",
            "\\bEaseType.SOFT_EASE_OUT\\b",
            "\\bEaseType.SOFT_SMOOTH\\b",
            "\\bEaseType.SINE_EASE_IN\\b",
            "\\bEaseType.SINE_EASE_OUT\\b",
            "\\bEaseType.SINE_SMOOTH\\b",
            "\\bEaseType.CIRC_EASE_IN\\b",
            "\\bEaseType.CIRC_EASE_OUT\\b",
            "\\bEaseType.CIRC_SMOOTH\\b",
            "\\bEaseType.BOUNCE_IN\\b",
            "\\bEaseType.BOUNCE_OUT\\b",
            "\\bEaseType.BOUNCE_SMOOTH\\b",
            "\\bEaseType.ELASTIC_IN\\b",
            "\\bEaseType.ELASTIC_OUT\\b",
            "\\bEaseType.ELASTIC_SMOOTH\\b",
            "\\bEaseType.BACK_EASE_IN\\b",
            "\\bEaseType.BACK_EASE_OUT\\b",
            "\\bEaseType.BACK_SMOOTH\\b",
        ]

        builtinRegPatters = ["\\bp\\b", "\\bsp\\b",
            "\\bp.x\\b",
            "\\bp.y\\b",
            "\\bp.dx\\b",
            "\\bp.dy\\b",

            "\\bsp.x\\b",
            "\\bsp.y\\b",
            "\\bsp.sx\\b",
            "\\bsp.sy\\b",
            "\\bsp.r\\b",
            "\\bsp.g\\b",
            "\\bsp.b\\b",
            "\\bsp.glow\\b",
            "\\bsp.idx\\b",
            "\\bsp.opacity\\b",
            "\\bsp.rot\\b",
        ]

        self.highlightingRules = []
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), keywordFormat) for pattern in keywordPatterns] )
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), constantsFormat) for pattern in constantsPatterns] )
        self.highlightingRules.extend( [(QtCore.QRegExp(pattern), builtinRegFormat) for pattern in builtinRegPatters] )

        commentFormat = QtGui.QTextCharFormat()
        commentFormat.setForeground(QtGui.QColor(self.monokai['gray']))
        self.highlightingRules.append((QtCore.QRegExp("--[^\n]*"), commentFormat))

        operatorFormat = QtGui.QTextCharFormat()
        operatorFormat.setForeground(QtGui.QColor(self.monokai['pink']))
        self.highlightingRules.append((QtCore.QRegExp("[\\+\\-\\*/=]"), operatorFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtGui.QColor(self.monokai['yellow']))
        self.highlightingRules.append((QtCore.QRegExp("\".*\""), quotationFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class ParticleScriptEditor (QPlainTextEdit):
    def __init__(self, parent=None):
        super(ParticleScriptEditor, self).__init__(parent)
        
        self.highlighter = Highlighter(self.document())

        #Autocompleter
        # global keywords
        # self.completer = QtGui.QCompleter(keywords, self)
        # self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer.setWidget(self)
        # self.autocompleteStart = None

        #Connect signals
        # self.completer.activated.connect(self.onAutoComplete)
        # self.connect(self.completer, QtCore.SIGNAL("activated(QString)"), self.onAutoComplete)

    # @QtCore.Slot(str)
    # def onAutoComplete(self, text):
    #     print("complete")

    #     # Select the text from autocompleteStart until the current cursor
    #     cursor = self.textCursor()
    #     cursor.setPosition(self.autocompleteStart, cursor.KeepAnchor)
    #     # Replace it with the selected text 
    #     cursor.insertText(text)
    #     self.autocompleteStart = None

    # def keyPressEvent(self,event):
    #     key = event.key()
    #     if key == Qt.Key_Tab:
    #         if self.autocompleteStart is not None:
    #             #Let the completer handle this one!
    #             event.ignore()
    #             return

    #     # Allowed keys that do not close the autocompleteList:
    #     # alphanumeric and _
    #     # Backspace (until start of autocomplete word)

    #     if self.autocompleteStart is not None and not event.text().isalnum() and event.text != '_' and \
    #         not ((key == Qt.Key_Backspace) and self.textCursor().position() > self.autocompleteStart):
    #         self.completer.popup().hide()
    #         self.autocompleteStart = None
        
    #     # Apply the key
    #     QtGui.QPlainTextEdit.keyPressEvent(self, event)
        
    #     if event.text()=='.':
    #         # Pop-up the autocompleteList
    #         rect = self.cursorRect(self.textCursor())
    #         rect.setSize(QtCore.QSize(100, 150))
    #         self.autocompleteStart = self.textCursor().position()
    #         self.completer.complete(rect) # The popup is positioned in the next if block
        
    #     if self.autocompleteStart:
    #         prefix = self.toPlainText()[ self.autocompleteStart : self.textCursor().position() ]
            
    #         # While we type, the start of the autocompletion may move due to line wrapping
    #         # Find the start of the autocompletion and move the completer popup there
    #         cur = self.textCursor()
    #         cur.setPosition(self.autocompleteStart)
    #         position = self.cursorRect(cur).bottomLeft() + self.geometry().topLeft() + self.viewport().pos()
    #         # self.completer.popup().move(position)

    #         print("prefix", prefix)
    #         print("pos", position)

    #         self.completer.setCompletionPrefix(prefix)
    #         # Select the first one of the matches
    #         self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0));
