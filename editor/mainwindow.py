#!/usr/bin/python

import sys

import platform
import PySide
import os
import errno
import argparse

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings, QCoreApplication, QLocale

from layout.mainwindow_ui import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget
from livereload import LiveReload

# dock widgets
from outlinerdock import OutlinerDock
from consoledialog import ConsoleDialog
from environmentdock import EnvironmentDock
from debugdock import DebugDock
from profilerdock import ProfilerDock
from statsdock import StatsDock
from particleeditordock import ParticleEditorDock
from particleparamsdock import ParticleParamsDock

from colorama import Fore, Back, Style
from time import strftime

import luainterface
import locale

colorPrintEnabled = True

rootPath = os.path.dirname(os.path.abspath(__file__))

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

def printSeparator(runningFile, colored):
    if colored:
        print(Style.RESET_ALL + Style.NORMAL + Fore.GREEN)
    
    print(5 * '\n' + 30 * '%%%')
    print('\t' + strftime('%H:%M:%S') + '\t' + runningFile)
    print(30 * '%%%')
    
    if colored:
        print(Style.RESET_ALL + Style.DIM)


class MainWindow(QMainWindow):
    runningFile = None

    def __init__(self, parent=None, script=None):
        super(MainWindow, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        # self.setDockNestingEnabled(True)

        self.moaiWidget = MOAIWidget()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.moaiWidget)
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)

        self.outlinerDock = OutlinerDock(self)
        self.consoleDialog = ConsoleDialog(self)
        self.debugDock = DebugDock(self)
        self.profilerDock = ProfilerDock(self)
        self.environmentDock = EnvironmentDock(self)
        self.statsDock = StatsDock(self)
        self.particleParamsDock = ParticleParamsDock(self)
        self.particleEditorDock = ParticleEditorDock(self)

        # self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.consoleDialog)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.outlinerDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.environmentDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.debugDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.profilerDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.statsDock)
        self.tabifyDockWidget(self.environmentDock, self.particleEditorDock)
        self.tabifyDockWidget(self.debugDock, self.particleParamsDock)

        actionOutliner = self.outlinerDock.toggleViewAction()
        actionEnvironment = self.environmentDock.toggleViewAction()
        actionDebug = self.debugDock.toggleViewAction()
        actionProfiler = self.profilerDock.toggleViewAction()
        actionStats = self.statsDock.toggleViewAction()
        actionParticleEditor = self.particleEditorDock.toggleViewAction()
        actionParticleParams = self.particleParamsDock.toggleViewAction()

        self.outlinerDock.hide()
        self.consoleDialog.hide()
        self.debugDock.hide()
        self.profilerDock.hide()
        self.statsDock.hide()
        self.particleEditorDock.hide()
        self.particleParamsDock.hide()

        ui.menuWindow.addAction(actionOutliner)
        ui.menuWindow.addAction(actionEnvironment)
        ui.menuWindow.addAction(actionDebug)
        ui.menuWindow.addAction(actionProfiler)
        ui.menuWindow.addAction(actionStats)
        ui.menuWindow.addAction(actionParticleEditor)
        ui.menuWindow.addAction(actionParticleParams)
        ui.menuWindow.addSeparator()
        ui.menuWindow.addAction(QtGui.QAction('&Console', self, statusTip="Open console window", shortcut="Shift+Ctrl+C", triggered=self.showConsole))

        self.viewMenu = self.menuBar().addMenu('&View')
        self.viewMenu.addAction(QtGui.QAction('&Fullscreen on', self, statusTip="Enter Fullscreen", shortcut="Shift+Ctrl+F", triggered=self.fullscreen))
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(QtGui.QAction('&Fullscreen off', self, statusTip="Exit Fullscreen", shortcut="Alt+Ctrl+F", triggered=self.normal))

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

    def fullscreen(self):
        self.setWindowState(QtCore.Qt.WindowFullScreen)

    def normal(self):
        self.setWindowState(QtCore.Qt.WindowNoState)

    def showConsole(self):
        self.consoleDialog.show()
        self.consoleDialog.activateWindow()

    def closeEvent(self, event):
        self.writeSettings()
        self.statsDock.stopTimer()
        self.moaiWidget.finalize()
        event.accept()

    def readSettings(self):
        settings = QSettings()

        self.restoreGeometry(settings.value("main/geometry"))
        self.restoreState(settings.value("main/windowState"))
        
        self.environmentDock.readSettings()
        self.debugDock.readSettings()
        self.particleEditorDock.readSettings()

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
        self.particleEditorDock.writeSettings()

    @QtCore.Slot()
    def showOpenFileDialog(self):
        fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", self.workingDir or "~", "Lua source (*.lua )")
        if fileName:
            workingDir = os.path.dirname(fileName)
            luaFile = os.path.basename(fileName)
            self.openFile(luaFile, workingDir)

    @QtCore.Slot()
    def reloadMoai(self):
        if self.runningFile:
            self.environmentDock.onEndSession()
            printSeparator(os.path.join(self.workingDir, self.runningFile), colorPrintEnabled)
            self.openFile(self.runningFile, self.workingDir)

    @QtCore.Slot()
    def reloadRemote(self):
        self.livereload.runStringRemote("if MOAISim.scheduleRelaunch then MOAISim.scheduleRelaunch() end")

    @QtCore.Slot()
    def updateLiveReload(self):
        self.livereload.update()

    @QtCore.Slot(str)
    def onMessage(self, message):
        pass

    @QtCore.Slot()
    def launchParticleEditor(self):
        fileName = os.path.join(rootPath, "lua/editor-framework/main.lua")
        luaFile = os.path.basename(fileName)
        workingDir = os.path.dirname(fileName)

        self.openFile(luaFile, workingDir)
        self.particleEditorDock.loadEditorScene(self.moaiWidget.lua)

    def resizeMoaiView(self, width, height):
        self.moaiWidget.resize(width, height)

    # lua
    def openFile(self, fileName, workingDir = ""):
        self.statsDock.stopTimer()

        self.moaiWidget.refreshContext()
        self.moaiWidget.setWorkingDirectory(workingDir)
        self.moaiWidget.setTraceback(tracebackFunc)
        self.moaiWidget.setPrint(luaBeforePrint, luaAfterPrint)
        
        self.moaiWidget.loadEditorFramework()

        self.debugDock.updateAllDebugValues()
        self.environmentDock.applyEnvironmentSettings()
        self.profilerDock.applyProfilingSettings()
        
        self.moaiWidget.loadLuaFramework()
        
        self.moaiWidget.runScript(fileName)
        self.runningFile = fileName
        self.workingDir = workingDir

        self.environmentDock.startSession(False)

        self.livereload.lua = self.moaiWidget.lua
        self.consoleDialog.lua = self.moaiWidget.lua
        self.livereload.watchDirectory(workingDir)

        self.statsDock.setLuaState(self.moaiWidget.lua)
        self.statsDock.startTimer()

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
    QLocale.setDefault(QLocale(QLocale.C))
    locale.setlocale(locale.LC_ALL, 'C')

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
    
    # mainWindow.show()
    mainWindow.showNormal()

    app.exec_()
    if colorPrintEnabled:
        print(Style.RESET_ALL)
