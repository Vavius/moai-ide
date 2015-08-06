import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget, QColor, QColorDialog, QPixmap

from layout.particleeditor_ui import Ui_particleEditor as Ui

import luainterface

class ParticleEditorDock(QDockWidget):
    def __init__(self, parent=None):
        super(ParticleEditorDock, self).__init__(parent)

        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.createColorPicker()

        self.mainWindow = self.parent()

    def createColorPicker(self):
        self.bgColorBtn = self.ui.btnBgColor
        self.bgColorBtn.color = QColor(255, 255, 255, 255)
        pixmap = QPixmap(16, 16)
        pixmap.fill(self.bgColorBtn.color)

        self.bgColorBtn.pixmap = pixmap
        self.bgColorBtn.setIcon(pixmap)
        self.bgColorBtn.setAutoFillBackground(False)
        self.bgColorBtn.setIconSize(QtCore.QSize(16, 16))

    def setBgBtnColor(self, color):
        btn = self.bgColorBtn
        
        btn.pixmap.fill(color)
        btn.setIcon(btn.pixmap)
        btn.color = color

    def setPropertyModel(self, propertyModel):
        self.propertyModel = propertyModel

    def loadEditorScene(self, lua):
        self.api = lua.require("ParticleEditor")

    def updateEmitterList(self):
        pass

    def updateStateList(self):
        pass

    def updateModel(self):
        pass

    @QtCore.Slot()
    def onBgColorClick(self):
        color = QColorDialog().getColor(self.bgColorBtn.color, self, "Backgroud color")

        if color.isValid():
            self.setBgBtnColor(color)

            c = [float(x)/255.0 for x in color.getRgb()]
            self.api.setBgColor(*c)

    @QtCore.Slot()
    def onNewEmitter(self):
        self.api.addEmitter()
        self.updateEmitterList()

    @QtCore.Slot()
    def onNewState(self):
        self.api.addState()
        self.updateStateList()

    @QtCore.Slot(str)
    def onEditParticleLimit(self, limit):
        pass

    @QtCore.Slot(str)
    def onEditSpriteLimit(self, limit):
        pass

    @QtCore.Slot(int)
    def onEmitterClick(self, index):
        pass

    @QtCore.Slot(int)
    def onStateClick(self, index):
        pass

    @QtCore.Slot()
    def onDeleteEmitter(self):
        pass

    @QtCore.Slot()
    def onDeleteState(self):
        pass

    @QtCore.Slot()
    def onNewComponent(self):
        pass

    @QtCore.Slot()
    def onDeleteComponent(self):
        pass

    @QtCore.Slot()
    def onLoadTexture(self):
        pass

    @QtCore.Slot(bool)
    def onWrapSprites(self, flag):
        pass

    @QtCore.Slot(bool)
    def onWrapParticles(self, flag):
        pass

    @QtCore.Slot(bool)
    def onReverseDraw(self, flag):
        pass

    def onModelParamChange(self, param, value):
        pass

