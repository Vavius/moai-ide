import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QPlainTextEdit

keys = (
    QtCore.Qt.Key_Left,
    QtCore.Qt.Key_Right,
    QtCore.Qt.Key_Up,
    QtCore.Qt.Key_Down,
    QtCore.Qt.Key_Return
)

class QConsole (QPlainTextEdit):
    def __init__(self, parent=None):
        super(QConsole, self).__init__(parent)

        self.delegate = None
        self.history = []
        self.current = -1

        cursor = self.textCursor()
        self.initialCursorPosition = cursor.position()
        self.lastCursorPosition = cursor.position()
        self.cursorValid = True

        self.cursorPositionChanged.connect(self.onCursor)
        self.showGreeting()
        
    def keyPressEvent(self, event):
        if not self.cursorValid:
            if event.key() in keys or event.text() != '':
                cursor = self.textCursor()
                cursor.setPosition(self.lastCursorPosition)
                self.setTextCursor(cursor)

        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Up:
                current = max(0, self.current - 1)
                if 0 <= current < len(self.history):
                    self.setLastString(self.history[current])
                    self.current = current
                event.accept()
                return
            
            elif event.key() == QtCore.Qt.Key_Down:
                current = min(len(self.history), self.current + 1)
                if 0 <= current < len(self.history):
                    self.setLastString(self.history[current])
                else:
                    self.setLastString('')
                self.current = current
                event.accept()
                return

            elif event.key() == QtCore.Qt.Key_Return:
                event.accept()
                self.execute()
                return

        super(QConsole, self).keyPressEvent(event)
    

    def onCursor(self):
        cursor = self.textCursor()
        if cursor.position() < self.initialCursorPosition:
            self.cursorValid = False
            # self.setReadOnly(True)

            # don't allow to delete symbols before initialCursorPosition
            # (easier to append removed space here, than catching remove events)
            if cursor.atEnd():
                self.insertPlainText(' ')

            # on the same greeting line
            if self.initialCursorPosition - cursor.position() < 4:
                mode = QtGui.QTextCursor.KeepAnchor if cursor.anchor() > self.initialCursorPosition else QtGui.QTextCursor.MoveAnchor
                cursor.setPosition(self.initialCursorPosition, mode)
                self.setTextCursor(cursor)

        else:
            self.cursorValid = True
            self.lastCursorPosition = cursor.position()
            # self.setReadOnly(False)
        
    def setDelegate(self, delegate):
        self.delegate = delegate

    def setLastString(self, string):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.setPosition(self.initialCursorPosition)
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.insertPlainText(string)
        cursor.endEditBlock()

    def showGreeting(self):
        self.appendPlainText('>>> ')
        self.initialCursorPosition = self.textCursor().position()
        self.document().clearUndoRedoStacks()
        self.ensureCursorVisible()

    def execute(self):
        cursor = self.textCursor()
        cursor.setPosition(self.initialCursorPosition)
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
        command = cursor.selectedText()

        cursor.movePosition(QtGui.QTextCursor.End)
        self.setTextCursor(cursor)

        if not command:
            self.showGreeting()
            return

        if command[0] == '=':
            command = 'return ' + command[1:]

        if self.delegate:
            self.delegate.execute(command)
        self.history.append(command)
        self.current = len(self.history)

    def display(self, string, greeting = True):
        if string:
            self.appendPlainText(string)
        if greeting:
            self.showGreeting()


