import sys, os
import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from layout.profilerdock_ui import Ui_profilerdock as Ui


class ProfilerDock(QDockWidget):
    def __init__(self, parent=None):
        super(ProfilerDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.mainWindow = self.parent()

        self.shinyCmd = {
            'start' : '''   shiny = require("shiny"); shiny.start() 
                            shiny_thread = MOAICoroutine.new() 
                            shiny_thread:run(function() 
                                -- while true do shiny.update(); coroutine.yield() end 
                            end) ''',
            'update': 'shiny.update()',
            'stop'  : 'shiny.stop(); if shiny_thread then shiny_thread:stop(); shiny_thread = nil; end',
            'clear' : 'shiny.clear()',
            'flat'  : 'print(shiny.flat_string())',
            'tree'  : 'print(shiny.tree_string())',
        }



    @QtCore.Slot(bool)
    def toggleActionProfiling(self, flag):
        self.mainWindow.moaiWidget.runString("MOAIActionMgr.setProfilingEnabled( %s )" % ('true' if flag else 'false'))

    @QtCore.Slot(bool)
    def toggleShiny(self, flag):
        if flag:
            self.mainWindow.moaiWidget.runString(self.shinyCmd['start'])
        else:
            self.mainWindow.moaiWidget.runString(self.shinyCmd['stop'])

    @QtCore.Slot()
    def shinyUpdate(self):
        self.mainWindow.moaiWidget.runString(self.shinyCmd['update'])

    @QtCore.Slot()
    def shinyClear(self):
        self.mainWindow.moaiWidget.runString(self.shinyCmd['clear'])

    @QtCore.Slot()
    def shinyFlatReport(self):
        self.mainWindow.moaiWidget.runString(self.shinyCmd['flat'])

    @QtCore.Slot()
    def shinyTreeReport(self):
        self.mainWindow.moaiWidget.runString(self.shinyCmd['tree'])

    def applyProfilingSettings(self):
        self.toggleActionProfiling(self.ui.actionProfiler.isChecked())
        self.toggleShiny(self.ui.shinyProfiler.isChecked())

