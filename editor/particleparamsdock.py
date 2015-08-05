import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget, QAbstractItemView

from layout.particleparams_ui import Ui_particleParams as Ui

from widgets.propertyitemmodel import PropertyItemModel, ComboDelegate
import luainterface

class ParticleParamsDock(QDockWidget):
    def __init__(self, parent=None):
        super(ParticleParamsDock, self).__init__(parent)

        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)
        self.mainWindow = self.parent()

        treeModel = PropertyItemModel(self)
        ui.paramsView.setModel(treeModel)

        self.itemDelegate = ComboDelegate(self)
        ui.paramsView.setItemDelegate(self.itemDelegate)

        
