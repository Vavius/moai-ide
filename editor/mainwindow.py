#!/usr/bin/python

import sys

import platform
import PySide
import os
import errno
import argparse

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings, QCoreApplication

from layout.mainwindow_ui import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget
from livereload import LiveReload

# dock widgets
from outlinerdock import OutlinerDock
from consoledock import ConsoleDock
from environmentdock import EnvironmentDock
from debugdock import DebugDock
from profilerdock import ProfilerDock

from colorama import Fore, Back, Style
from time import strftime

import luainterface

colorPrintEnabled = True

def tracebackFunc(trace):
    if colorPrintEnabled:
        print(Style.RESET_ALL + Fore.RED + Style.BRIGHT + trace + Style.RESET_ALL + Style.DIM)
    else:
        print(trace)

def luaBeforePrint():
    style = strftime("%H:%M:%S")
    if colorPrintEnabled:
        style = style + Style.RESET_ALL + Style.NORMAL
    style = style + '  '
    print style,
    
def luaAfterPrint():
    if colorPrintEnabled:
        style = Style.RESET_ALL + Style.DIM
        sys.stdout.write(style)


class MainWindow(QMainWindow):
    runningFile = None

    def __init__(self, parent=None, script=None):
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
        self.profilerDock = ProfilerDock(self)
        self.environmentDock = EnvironmentDock(self)

        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.consoleDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.outlinerDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.environmentDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.debugDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.profilerDock)

        actionOutliner = self.outlinerDock.toggleViewAction()
        actionConsole = self.consoleDock.toggleViewAction()
        actionEnvironment = self.environmentDock.toggleViewAction()
        actionDebug = self.debugDock.toggleViewAction()
        actionProfiler = self.profilerDock.toggleViewAction()

        self.outlinerDock.hide()
        self.consoleDock.hide()
        self.debugDock.hide()
        self.profilerDock.hide()
        
        ui.menuWindow.addAction(actionOutliner)
        ui.menuWindow.addAction(actionEnvironment)
        ui.menuWindow.addAction(actionConsole)
        ui.menuWindow.addAction(actionDebug)
        ui.menuWindow.addAction(actionProfiler)
        
        self.livereload = LiveReload()
        self.livereload.fullReloadFunc = self.reloadMoai

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateLiveReload)
        self.timer.start(1000)

        self.runningFile = script
        self.workingDir = ""
        self.readSettings()
        if script:
            QtCore.QTimer.singleShot(0, self, QtCore.SLOT("reloadMoai()"))

    def closeEvent(self, event):
        self.writeSettings()
        QMainWindow.closeEvent(self, event)

    def readSettings(self):
        settings = QSettings()

        self.restoreGeometry(settings.value("main/geometry"))
        self.restoreState(settings.value("main/windowState"))
        
        self.environmentDock.readSettings()
        self.debugDock.readSettings()

        self.runAttempts = settings.value("main/openProjectAttempts", 0) + 1
        settings.setValue("main/openProjectAttempts", self.runAttempts)

        # do not load projects if it crashed last time
        if not self.runningFile and self.runAttempts < 3:
            self.runningFile = settings.value("main/currentFile")
            self.workingDir = settings.value("main/workingDir", "")
            QtCore.QTimer.singleShot(0, self, QtCore.SLOT("reloadMoai()"))
        

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("main/geometry", self.saveGeometry())
        settings.setValue("main/windowState", self.saveState())
        settings.setValue("main/currentFile", self.runningFile)
        settings.setValue("main/workingDir", self.workingDir)
        self.environmentDock.writeSettings()
        self.debugDock.writeSettings()

    @QtCore.Slot()
    def showOpenFileDialog(self):
        fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", "~", "Lua source (*.lua )")
        if fileName:
            workingDir = os.path.dirname(fileName)
            luaFile = os.path.basename(fileName)
            self.openFile(luaFile, workingDir)

    @QtCore.Slot()
    def reloadMoai(self):
        if self.runningFile:
            self.consoleDock.onReload(os.path.join(self.workingDir, self.runningFile), colorPrintEnabled)
            self.openFile(self.runningFile, self.workingDir)

    @QtCore.Slot()
    def updateLiveReload(self):
        self.livereload.update()

    @QtCore.Slot(str)
    def onMessage(self, message):
        pass

    def resizeMoaiView(self, width, height):
        self.moaiWidget.resize(width, height)

    # lua
    def openFile(self, fileName, workingDir = ""):
        self.moaiWidget.refreshContext()
        self.moaiWidget.setWorkingDirectory(workingDir)
        self.moaiWidget.setTraceback(tracebackFunc)
        self.moaiWidget.setPrint(luaBeforePrint, luaAfterPrint)
        
        self.debugDock.updateAllDebugValues()
        self.environmentDock.applyEnvironmentSettings()
        self.profilerDock.applyProfilingSettings()
        
        self.moaiWidget.loadLuaFramework()
        
        self.moaiWidget.runScript(fileName)
        self.runningFile = fileName
        self.workingDir = workingDir

        self.environmentDock.startSession(False)

        self.livereload.lua = self.moaiWidget.lua
        self.livereload.watchDirectory(workingDir)

        self.runAttempts = 0
        settings = QSettings()
        settings.setValue("main/openProjectAttempts", self.runAttempts)


class ConsoleStream(QtCore.QObject):
    message = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

if __name__ == '__main__':
    QCoreApplication.setOrganizationName("DigitalClick")
    QCoreApplication.setOrganizationDomain("cloudteam.pro")
    QCoreApplication.setApplicationName("Moai Editor")

    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='PySide Qt MOAI host with some debugging capabilities')
    parser.add_argument('script', nargs='?', type=str, help='MOAI script to execute')
    parser.add_argument('--nocolor', action='store_true', help='disable colored terminal output')

    args = parser.parse_args()
    colorPrintEnabled = not args.nocolor

    mainWindow = MainWindow(script = args.script)

    # all output except traceback and user prints is DIM
    if colorPrintEnabled:
        print(Style.DIM)
    
    mainWindow.show()
    app.exec_()
    
    if colorPrintEnabled:
        print(Style.RESET_ALL)
