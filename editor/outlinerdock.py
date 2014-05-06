import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from layout.outlinerdock_ui import Ui_outlinerdock as Ui

import luainterface

class OutlinerDock(QDockWidget):
    def __init__(self, parent=None):
        super(OutlinerDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.mainWindow = self.parent()