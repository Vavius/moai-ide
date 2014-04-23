import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from colorama import Fore, Back, Style
from time import strftime

from layout.consoledock_ui import Ui_consoledock as Ui



def printSeparator(runningFile, colored):
    if colored:
        print(Style.RESET_ALL + Style.NORMAL + Fore.GREEN)
    
    print(5 * '\n' + 30 * '%%%')
    print('\t' + strftime('%H:%M:%S') + '\t' + runningFile)
    print(30 * '%%%')
    
    if colored:
        print(Style.RESET_ALL + Style.DIM)

class ConsoleDock(QDockWidget):
    def __init__(self, parent=None):
        super(ConsoleDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.mainWindow = self.parent()

    def onReload(self, runningFile, colored):
        self.ui.localConsoleTextBox.clear()
        self.ui.deviceConsoleTextBox.clear()
        printSeparator(runningFile, colored)