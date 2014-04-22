import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QGroupBox

class QGroupBoxCollapsible (QGroupBox):
    def __init__(self, parent=None):
        super(QGroupBoxCollapsible, self).__init__(parent)
        self.toggled.connect(self.collapse)
        self.setStyleSheet("""
                QGroupBox::indicator::checked { image: url(:/icon/resources/arrow_on.png); }
                QGroupBox::indicator::unchecked { image: url(:/icon/resources/arrow_off.png); }
            """)

    @QtCore.Slot(bool)
    def collapse(self, flag):
        for child in self.children():
            if hasattr(child, "setVisible"):
                child.setVisible(flag)