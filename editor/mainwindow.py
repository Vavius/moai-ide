#!/usr/bin/python

import sys
import platform
import PySide
import os
import errno

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings

from ui_mainWindow import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget
from livereload import LiveReload

import luainterface

def tracebackFunc(textBox):
    def printToConsole(trace):
        textBox.moveCursor(QtGui.QTextCursor.End)
        textBox.insertPlainText(trace)
        textBox.insertPlainText('\n')
    return printToConsole

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

        actionPropertyEditor = ui.propertyEditor.toggleViewAction()
        actionObjectPallete = ui.objectPallete.toggleViewAction()
        actionEnvironmentSettings = ui.environmentSettings.toggleViewAction()
        actionConsole = ui.consoleOutput.toggleViewAction()
        ui.propertyEditor.hide()
        ui.objectPallete.hide()
        ui.consoleOutput.hide()

        ui.menuWindow.addAction(actionPropertyEditor)
        ui.menuWindow.addAction(actionObjectPallete)
        ui.menuWindow.addAction(actionEnvironmentSettings)
        ui.menuWindow.addAction(actionConsole)

        intValidator = PySide.QtGui.QIntValidator()
        intValidator.setRange(128, 4096)
        ui.widthEdit.setValidator(intValidator)
        ui.heightEdit.setValidator(intValidator)
        ui.widthEdit.textChanged.connect(self.viewSizeEditingFinished)
        ui.heightEdit.textChanged.connect(self.viewSizeEditingFinished)

        self.livereload = LiveReload()
        self.livereload.fullReloadFunc = self.reloadMoai

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateLiveReload)
        self.timer.start(1000)

        self.readSettings()

    def closeEvent(self, event):
        settings = QSettings("DigitalClick", "MoaiEditor")

        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("width", self.ui.widthEdit.text())
        settings.setValue("height", self.ui.heightEdit.text())
        settings.setValue("currentFile", self.runningFile)
        settings.setValue("autoreloadDevice", self.ui.deviceAutoreload.isChecked())
        settings.setValue("autoreloadHost", self.ui.localAutoreload.isChecked())
        settings.setValue("autoreloadFull", self.ui.fullAutoreload.isChecked())
        QMainWindow.closeEvent(self, event)

    def readSettings(self):
        settings = QSettings("DigitalClick", "MoaiEditor")

        glSize = self.moaiWidget.sizeHint()
        
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))
        self.ui.widthEdit.setText( settings.value("width", str(glSize.width())) )
        self.ui.heightEdit.setText( settings.value("height", str(glSize.height())) )
        self.ui.deviceAutoreload.setChecked( settings.value("autoreloadDevice", False) )
        self.ui.localAutoreload.setChecked( settings.value("autoreloadHost", False) )
        self.ui.fullAutoreload.setChecked( settings.value("autoreloadFull", False) )

        self.livereload.setAutoreloadDevice(self.ui.deviceAutoreload.isChecked())
        self.livereload.setAutoreloadHost(self.ui.localAutoreload.isChecked())
        self.livereload.setAutoreloadFull(self.ui.fullAutoreload.isChecked())

        if not self.runningFile:
            self.runningFile = settings.value("currentFile")
            QtCore.QTimer.singleShot(0, self, QtCore.SLOT("reloadMoai()"))

    @QtCore.Slot()
    def showOpenFileDialog(self):
        fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", "~", "Lua source (*.lua )")
        if fileName:
            self.openFile(fileName)

    @QtCore.Slot()
    def reloadMoai(self):
        if self.runningFile:
            self.ui.localConsoleTextBox.clear()
            self.ui.deviceConsoleTextBox.clear()
            self.openFile(self.runningFile)

    @QtCore.Slot(bool)
    def setAutoreloadDevice(self, flag):
        self.livereload.setAutoreloadDevice(flag)

    @QtCore.Slot(bool)
    def setAutoreloadHost(self, flag):
        self.livereload.setAutoreloadHost(flag)

    @QtCore.Slot(bool)
    def setAutoreloadFull(self, flag):
        self.livereload.setAutoreloadFull(flag)

    @QtCore.Slot()
    def updateLiveReload(self):
        self.livereload.update()

    @QtCore.Slot(str)
    def onMessage(self, message):
        pass
        # self.ui.localConsoleTextBox.moveCursor(QtGui.QTextCursor.End)
        # self.ui.localConsoleTextBox.insertPlainText(message)
        # self.ui.deviceConsoleTextBox.moveCursor(QtGui.QTextCursor.End)
        # self.ui.deviceConsoleTextBox.insertPlainText(message)

    @QtCore.Slot(int)
    def setCurrentDevice(self, index):
        currentDeviceIP = self.deviceList[index]['ip']
        self.livereload.setCurrentDeviceIP(currentDeviceIP)

    @QtCore.Slot()
    def updateDeviceList(self):
        self.deviceList = luainterface.search(self.moaiWidget.lua)
        print(self.deviceList)
        self.ui.availableDevicesList.clear()
        for d in self.deviceList:
            self.ui.availableDevicesList.addItem("%s [%s]" % (d['name'], d['ip']))

    def viewSizeEditingFinished(self):
        try:
            width = int(self.ui.widthEdit.text())
        except ValueError:
            width = 640

        try:
            height = int(self.ui.heightEdit.text())
        except ValueError:
            height = 480

        self.resizeMoaiView(width, height)

    def resizeMoaiView(self, width, height):
        self.moaiWidget.resize(width, height)

    # lua 
    def openFile(self, fileName):
        workingDir = os.path.dirname(fileName)
        luaFile = os.path.basename(fileName)

        self.moaiWidget.refreshContext()

        def traceback(err):
            print(traceback)
        self.moaiWidget.setTraceback(traceback)
        # self.moaiWidget.setTraceback(tracebackFunc(self.ui.localConsoleTextBox))
        self.moaiWidget.setWorkingDirectory(workingDir)
        self.moaiWidget.runScript(luaFile)
        self.runningFile = fileName

        self.livereload.lua = self.moaiWidget.lua
        self.livereload.watchDirectory(workingDir)


class ConsoleStream(QtCore.QObject):
    message = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()

    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    

    mainWindow.show()
    app.exec_()
