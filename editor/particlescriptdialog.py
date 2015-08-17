import sys
import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QDialog

from layout.particlescriptdialog_ui import Ui_ParticleScriptDialog as Ui

class ParticleScriptDialog(QDialog):
    api = None

    def __init__(self, parent=None):
        super(ParticleScriptDialog, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)
        self.particleEditor = parent

        self.initEditor = ui.initScript
        self.renderEditor = ui.renderScript

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
    def onSave(self):
        if self.api:
            init = self.initEditor.toPlainText()
            render = self.renderEditor.toPlainText()
            self.api.setUserInitScript(init)
            self.api.setUserRenderScript(render)

    @QtCore.Slot()
    def onSaveAs(self):
        if self.api:
            pass

    def onStateSelected(self, stateId):
        if self.api:
            init = self.api.getUserInitScript(stateId)
            render = self.api.getUserRenderScript(stateId)
            self.initEditor.setPlainText(init or "")
            self.renderEditor.setPlainText(render or "")

