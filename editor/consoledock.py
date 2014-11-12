import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from colorama import Fore, Back, Style
from time import strftime

from layout.consoledock_ui import Ui_consoledock as Ui
import luainterface

class ConsoleDock(QDockWidget):
    def __init__(self, parent=None):
        super(ConsoleDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        ui.localConsoleTextBox.setDelegate(self)
        self.lua = None


    def execute(self, string):
        if self.lua:
            textBox = self.ui.localConsoleTextBox
            
            def onPrint(output):
                textBox.display(output, False)
            luainterface.setConsolePrint(self.lua, onPrint)

            output = luainterface.runConsoleCommand(self.lua, string)
            textBox.display(output)
