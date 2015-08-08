import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget, QColor, QColorDialog, QPixmap

from layout.particleeditor_ui import Ui_particleEditor as Ui
import moaipy

import luainterface

def luaTableToDict(t):
    d = dict()
    for k, v in t.items():
        if type(v) == moaipy._LuaTable:
            d[k] = luaTableToDict(v)
        else:
            d[k] = v
    return d

class ParticleEditorDock(QDockWidget):
    activeModelType = None

    def __init__(self, parent=None):
        super(ParticleEditorDock, self).__init__(parent)

        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        intValidator = QtGui.QIntValidator()
        intValidator.setRange(0, 99000)
        ui.editParticleLimit.setValidator(intValidator)
        ui.editSpriteLimit.setValidator(intValidator)

        self.emitterList = ui.listEmitter
        self.stateList = ui.listState

        self.createColorPicker()

        self.mainWindow = self.parent()
        self.propertyModel = self.mainWindow.particleParamsDock.getModel()
        self.treeView = self.mainWindow.particleParamsDock.getTreeView()

        self.propertyModel.itemDataChanged.connect(self.onModelParamChange)

    def readSettings(self):
        settings = QtCore.QSettings()
        self.lastTextureDir = settings.value("particle/texdir", "~")

    def writeSettings(self):
        settings = QtCore.QSettings()
        settings.setValue("particle/texdir", self.lastTextureDir or "~")

    def populateComponentList(self):
        components = self.api.getComponentList()
        for k, v in components.items():
            self.ui.cmbComponent.addItem(v)

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

    def loadEditorScene(self, lua):
        self.api = lua.require("ParticleEditor")
        self.populateComponentList()
        self.ui.editParticleLimit.setText('128')
        self.ui.editSpriteLimit.setText('128')

    def updateEmitterList(self):
        emitters = self.api.listEmitters()
        self.emitterList.clear()

        for i, name in emitters.items():
            self.emitterList.addItem(name)

    def updateStateList(self):
        states = self.api.listStates()
        self.stateList.clear()

        for i, name in states.items():
            self.stateList.addItem(name)

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
        self.api.setParticleLimit(int(limit))

    @QtCore.Slot(str)
    def onEditSpriteLimit(self, limit):
        self.api.setSpriteLimit(int(limit))

    @QtCore.Slot()
    def onEmitterClick(self):
        index = self.emitterList.currentRow()
        if index < 0:
            return
        
        data = self.api.getEmitterData(int(index) + 1)
        self.propertyModel.setModelData(luaTableToDict(data))
        self.treeView.expandAll()
        self.activeModelType = 'emitter'
        self.api.hideGizmos()

    @QtCore.Slot()
    def onStateClick(self):
        index = self.stateList.currentRow()
        if index < 0:
            return

        data = self.api.getStateData(int(index) + 1)
        self.propertyModel.setModelData(luaTableToDict(data))
        self.treeView.expandAll()
        self.activeModelType = 'state'
        self.api.hideGizmos()

    @QtCore.Slot()
    def onDeleteEmitter(self):
        idx = self.emitterList.currentRow() + 1
        self.api.removeEmitter(idx)
        self.updateEmitterList()
        self.propertyModel.setModelData(None)

    @QtCore.Slot()
    def onDeleteState(self):
        idx = self.stateList.currentRow() + 1
        self.api.removeState(idx)
        self.updateStateList()
        self.propertyModel.setModelData(None)

    @QtCore.Slot()
    def onNewComponent(self):
        idx = self.stateList.currentRow() + 1
        if idx < 0: return
        component = self.ui.cmbComponent.currentText()
        self.api.addComponent(idx, component)
        self.onStateClick()

    @QtCore.Slot()
    def onDeleteComponent(self):
        pass

    @QtCore.Slot()
    def onLoadTexture(self):
        filename, filt = QtGui.QFileDialog.getOpenFileName(self, "Load texture atlas", self.lastTextureDir or "~", "MOAI texture atlas (*.lua)")
        if filename:
            self.lastTextureDir = os.path.dirname(filename)
            self.api.loadTextureAtlas(filename)

    @QtCore.Slot(bool)
    def onWrapSprites(self, flag):
        self.api.setWrapSprites(flag)

    @QtCore.Slot(bool)
    def onWrapParticles(self, flag):
        self.api.setWrapParticles(flag)

    @QtCore.Slot(bool)
    def onReverseDraw(self, flag):
        self.api.setReverseDrawOrder(flag)

    @QtCore.Slot(object, object)
    def onModelParamChange(self, paramId, value):
        if self.activeModelType == 'emitter':
            emitterId = self.emitterList.currentRow()
            if emitterId < 0: return
            if self.api.setEmitterParam(emitterId + 1, str(paramId), value):
                self.onEmitterClick()

        elif self.activeModelType == 'state':
            stateId = self.stateList.currentRow()
            if stateId < 0: return
            if self.api.setStateParam(stateId + 1, str(paramId), value):
                self.onStateClick()

