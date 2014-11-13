import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDialog
from PySide.QtCore import QSettings

from colorama import Fore, Back, Style
from time import strftime

from layout.consoledialog_ui import Ui_Console as Ui
import luainterface

class ConsoleDialog(QDialog):
    def __init__(self, parent=None):
        super(ConsoleDialog, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        ui.localConsoleTextBox.setDelegate(self)
        self.lua = None
        self.readSettings()

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def showEvent(self, event):
        self.readSettings()
        event.accept()

    def readSettings(self):
        settings = QSettings()
        self.restoreGeometry(settings.value("console/geometry"))

    def writeSettings(self):
        settings = QSettings()
        settings.setValue("console/geometry", self.saveGeometry())

    def execute(self, string):
        if self.lua:
            textBox = self.ui.localConsoleTextBox
            
            def onPrint(output):
                textBox.display(output, False)
            luainterface.setConsolePrint(self.lua, onPrint)

            output = luainterface.runConsoleCommand(self.lua, string)
            textBox.display(output)
