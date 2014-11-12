import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QPlainTextEdit

class QConsole (QPlainTextEdit):
    def __init__(self, parent=None):
        super(QConsole, self).__init__(parent)

        self.history = []
        self.current = -1
        
    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Up:
                current = max(0, self.current - 1)
                if 0 <= current < len(self.history):
                    # self.setText(self.history[current])
                    self.current = current
                event.accept()
                return
            
            elif event.key() == QtCore.Qt.Key_Down:
                current = min(len(self.history), self.current + 1)
                if 0 <= current < len(self.history):
                    # self.setText(self.history[current])
                    pass
                else:
                    self.clear()
                self.current = current
                event.accept()
                return

            elif event.key() == QtCore.Qt.Key_Return:
                event.accept()
                return

        super(QConsole, self).keyPressEvent(event)

    # def 

    def setLastString(self, string):
        pass

    def execute(self, string):
        pass

    def display(self, string):
        pass