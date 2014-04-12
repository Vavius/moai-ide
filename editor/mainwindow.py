#!/usr/bin/python

import sys
sys.path.append("layout")

import platform
import PySide
import os
import errno

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings, QCoreApplication

from mainwindow_ui import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget
from livereload import LiveReload

# dock widgets
from outlinerdock import OutlinerDock
from consoledock import ConsoleDock
from environmentdock import EnvironmentDock
from debugdock import DebugDock

from colorama import Fore, Back, Style
from time import strftime

import luainterface

def tracebackFunc(trace):
    print(Style.RESET_ALL + Fore.RED + Style.BRIGHT + trace + Style.RESET_ALL + Style.DIM)

def luaBeforePrint():
    style = strftime("%H:%M:%S") + Style.RESET_ALL + Style.NORMAL + '  '
    print style,
    
def luaAfterPrint():
    style = Style.RESET_ALL + Style.DIM
    sys.stdout.write(style)


class MainWindow(QMainWindow):
    runningFile = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.moaiWidget = MOAIWidget()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.moaiWidget)
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)

        self.outlinerDock = OutlinerDock(self)
        self.consoleDock = ConsoleDock(self)
        self.debugDock = DebugDock(self)
        self.environmentDock = EnvironmentDock(self)

        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.consoleDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.outlinerDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.environmentDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.debugDock)

        actionOutliner = self.outlinerDock.toggleViewAction()
        actionConsole = self.consoleDock.toggleViewAction()
        actionEnvironment = self.environmentDock.toggleViewAction()
        actionDebug = self.debugDock.toggleViewAction()

        self.outlinerDock.hide()
        self.consoleDock.hide()
        self.debugDock.hide()
        
        ui.menuWindow.addAction(actionOutliner)
        ui.menuWindow.addAction(actionEnvironment)
        ui.menuWindow.addAction(actionConsole)
        ui.menuWindow.addAction(actionDebug)
        
        self.livereload = LiveReload()
        self.livereload.fullReloadFunc = self.reloadMoai

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateLiveReload)
        self.timer.start(1000)

        self.readSettings()

    def closeEvent(self, event):
        self.writeSettings()
        QMainWindow.closeEvent(self, event)

    def readSettings(self):
        settings = QSettings()

        self.restoreGeometry(settings.value("main/geometry"))
        self.restoreState(settings.value("main/windowState"))
        
        self.environmentDock.readSettings()
        self.debugDock.readSettings()
        if not self.runningFile:
            self.runningFile = settings.value("main/currentFile")
            QtCore.QTimer.singleShot(0, self, QtCore.SLOT("reloadMoai()"))
        

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("main/geometry", self.saveGeometry())
        settings.setValue("main/windowState", self.saveState())
        settings.setValue("main/currentFile", self.runningFile)
        self.environmentDock.writeSettings()
        self.debugDock.writeSettings()        

    @QtCore.Slot()
    def showOpenFileDialog(self):
        fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", "~", "Lua source (*.lua )")
        if fileName:
            self.openFile(fileName)

    @QtCore.Slot()
    def reloadMoai(self):
        if self.runningFile:
            self.consoleDock.onReload(self.runningFile)
            self.openFile(self.runningFile)

    @QtCore.Slot()
    def updateLiveReload(self):
        self.livereload.update()

    @QtCore.Slot(str)
    def onMessage(self, message):
        pass

    def resizeMoaiView(self, width, height):
        self.moaiWidget.resize(width, height)

    # lua 
    def openFile(self, fileName):
        self.workingDir = os.path.dirname(fileName)
        luaFile = os.path.basename(fileName)

        self.moaiWidget.refreshContext()

        self.moaiWidget.setTraceback(tracebackFunc)
        self.moaiWidget.setPrint(luaBeforePrint, luaAfterPrint)
        self.moaiWidget.setWorkingDirectory(self.workingDir)
        self.debugDock.updateAllDebugValues()
        self.environmentDock.applyEnvironmentSettings()
        self.moaiWidget.runScript(luaFile)
        self.runningFile = fileName

        self.livereload.lua = self.moaiWidget.lua
        self.livereload.watchDirectory(self.workingDir)


class ConsoleStream(QtCore.QObject):
    message = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

if __name__ == '__main__':
    QCoreApplication.setOrganizationName("DigitalClick")
    QCoreApplication.setOrganizationDomain("cloudteam.com")
    QCoreApplication.setApplicationName("Moai Editor")

    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    # all output except traceback and user prints is DIM
    print(Style.DIM)
    mainWindow.show()
    app.exec_()
    print(Style.RESET_ALL)
