import sys, os, json
import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QDialog

from layout.particlescriptdialog_ui import Ui_ParticleScriptDialog as Ui

class ParticleScriptDialog(QDialog):
    api = None
    lastScriptDir = None
    scriptPath = None

    def __init__(self, parent=None):
        super(ParticleScriptDialog, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)
        self.particleEditor = parent

        self.initEditor = ui.initScript
        self.renderEditor = ui.renderScript

        actionSave = QtGui.QAction('Save script', self, shortcut = "Ctrl+S", triggered=self.onSave)
        actionSaveAs = QtGui.QAction('Save script as...', self, shortcut = "Ctrl+Shift+S", triggered=self.onSaveAs)

        actionOpen = QtGui.QAction('Open script...', self, triggered=self.onOpen)
        actionLoadCustom = QtGui.QAction('Load custom', self, triggered=self.onLoadCustom)
        actionLoadFromState = QtGui.QAction('Load from state', self, triggered=self.onLoadFromState)

        ui.btnSave.setDefaultAction(actionSave)
        ui.btnSaveAs.setDefaultAction(actionSaveAs)
        ui.btnOpen.setDefaultAction(actionOpen)
        ui.btnLoadCustom.setDefaultAction(actionLoadCustom)
        ui.btnLoadFromState.setDefaultAction(actionLoadFromState)

    def readScript(self, path):
        if not path: return

        with open(path) as f:
            stateId = self.particleEditor.stateList.currentRow() + 1
            data = json.load(f)
            
            if 'init' in data:
                self.api.setUserInitScript(stateId, data['init'])
                self.initEditor.setPlainText(data['init'])

            if 'render' in data:
                self.api.setUserRenderScript(stateId, data['render'])
                self.renderEditor.setPlainText(data['render'])

    def writeScript(self, path):
        if not path: return

        with open(path, 'w') as f:
            stateId = self.particleEditor.stateList.currentRow() + 1
            script = {
                "init" : self.api.getUserInitScript(stateId),
                "render" : self.api.getUserRenderScript(stateId)
            }
            print(script)
            json.dump(script, f)

    def setApi(self, api):
        self.api = api

    @QtCore.Slot()
    def onLoadCustom(self):
        if self.api:
            stateId = self.particleEditor.stateList.currentRow() + 1
            init = self.api.getUserInitScript(stateId)
            render = self.api.getUserRenderScript(stateId)
            self.initEditor.setPlainText(init or "")
            self.renderEditor.setPlainText(render or "")

    @QtCore.Slot()
    def onLoadFromState(self):
        if self.api:
            stateId = self.particleEditor.stateList.currentRow() + 1
            init = self.api.getInitScript(stateId)
            render = self.api.getRenderScript(stateId)
            self.initEditor.setPlainText(init or "")
            self.renderEditor.setPlainText(render or "")

    @QtCore.Slot()
    def onOpen(self):
        if not self.api:
            return

        filename, filt = QtGui.QFileDialog.getOpenFileName(self, "Open script", self.lastScriptDir or "~", "Script files (*.json)")
        if filename:
            self.lastScriptDir = os.path.dirname(filename)
            self.scriptPath = filename
            self.readScript(filename)

    @QtCore.Slot()
    def onSave(self):
        if self.api:
            stateId = self.particleEditor.stateList.currentRow() + 1
            init = self.initEditor.toPlainText()
            render = self.renderEditor.toPlainText()
            self.api.setUserInitScript(stateId, init)
            self.api.setUserRenderScript(stateId, render)
            self.writeScript(self.scriptPath)

    @QtCore.Slot()
    def onSaveAs(self):
        if not self.api:
            return

        filename, filt = QtGui.QFileDialog.getSaveFileName(self, "Save script as", self.lastScriptDir or "~", "Script files (*.json)")
        if filename:
            self.lastScriptDir = os.path.dirname(filename)
            self.scriptPath = filename
            self.writeScript(filename)

    def onStateSelected(self, stateId):
        if self.api:
            init = self.api.getUserInitScript(stateId)
            render = self.api.getUserRenderScript(stateId)
            self.initEditor.setPlainText(init or "")
            self.renderEditor.setPlainText(render or "")

