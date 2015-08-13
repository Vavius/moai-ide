import sys
import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QDialog

from layout.particlescriptdialog_ui import Ui_ParticleScriptDialog as Ui

class ParticleScriptDialog(QDialog):
    def __init__(self, parent=None):
        super(ParticleScriptDialog, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

