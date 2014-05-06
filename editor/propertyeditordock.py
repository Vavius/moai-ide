import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from propertyeditordock_ui import Ui_propertyeditordock as Ui

import luainterface

class PropertyEditorDock(QDockWidget):
    def __init__(self, parent=None):
        super(PropertyEditorDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.mainWindow = self.parent()