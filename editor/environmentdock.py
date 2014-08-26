import sys, os
import PySide

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget
from PySide.QtCore import QSettings, QLocale
from locales import Languages

from layout.environmentdock_ui import Ui_environmentdock as Ui

import luainterface

DEFAULT_LANGUAGE_CODE = 13

class EnvironmentDock(QDockWidget):
    def __init__(self, parent=None):
        super(EnvironmentDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)
        self.mainWindow = self.parent()

        floatValidator = PySide.QtGui.QDoubleValidator()
        floatValidator.setRange(128, 4096)
        ui.widthEdit.setValidator(floatValidator)
        ui.heightEdit.setValidator(floatValidator)

        dpiValidator = PySide.QtGui.QDoubleValidator()
        dpiValidator.setRange(20, 1000)
        ui.dpiEdit.setValidator(dpiValidator)
        
        ui.widthEdit.textChanged.connect(self.viewSizeEditingFinished)
        ui.heightEdit.textChanged.connect(self.viewSizeEditingFinished)
        
        for idx in xrange(0, len(Languages)):
            ui.languageBox.addItem(QLocale.languageToString(Languages[idx]))
        

    def readSettings(self):
        settings = QSettings()

        glSize = self.mainWindow.moaiWidget.sizeHint()
        
        self.ui.widthEdit.setText( settings.value("env/width", str(glSize.width())) )
        self.ui.heightEdit.setText( settings.value("env/height", str(glSize.height())) )
        self.ui.deviceAutoreload.setChecked( settings.value("env/autoreloadDevice", False) )
        self.ui.localAutoreload.setChecked( settings.value("env/autoreloadHost", False) )
        self.ui.fullAutoreload.setChecked( settings.value("env/autoreloadFull", False) )
        self.ui.dpiEdit.setText( settings.value("env/dpi", "132") )
        self.ui.documentsBtn.setText( settings.value("env/documents", "docs/") )

        lang = settings.value("env/languageCode", DEFAULT_LANGUAGE_CODE)
        self.ui.languageBox.setCurrentIndex( lang )
        self.updateCountriesCombobox( lang )
        self.ui.countryBox.setCurrentIndex( settings.value("env/countryCode", 0))

        self.mainWindow.livereload.setAutoreloadDevice(self.ui.deviceAutoreload.isChecked())
        self.mainWindow.livereload.setAutoreloadHost(self.ui.localAutoreload.isChecked())
        self.mainWindow.livereload.setAutoreloadFull(self.ui.fullAutoreload.isChecked())

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("env/width", self.ui.widthEdit.text())
        settings.setValue("env/height", self.ui.heightEdit.text())
        settings.setValue("env/autoreloadDevice", self.ui.deviceAutoreload.isChecked())
        settings.setValue("env/autoreloadHost", self.ui.localAutoreload.isChecked())
        settings.setValue("env/autoreloadFull", self.ui.fullAutoreload.isChecked())

        settings.setValue("env/dpi", self.ui.dpiEdit.text())
        settings.setValue("env/documents", self.ui.documentsBtn.text())
        settings.setValue("env/countryCode", self.ui.countryBox.currentIndex())
        settings.setValue("env/languageCode", self.ui.languageBox.currentIndex())

    @QtCore.Slot(bool)
    def setAutoreloadDevice(self, flag):
        self.mainWindow.livereload.setAutoreloadDevice(flag)

    @QtCore.Slot(bool)
    def setAutoreloadHost(self, flag):
        self.mainWindow.livereload.setAutoreloadHost(flag)

    @QtCore.Slot(bool)
    def setAutoreloadFull(self, flag):
        self.mainWindow.livereload.setAutoreloadFull(flag)

    @QtCore.Slot(int)
    def setCurrentDevice(self, index):
        if self.deviceList:
            currentDeviceIP = self.deviceList[index]['ip']
            self.mainWindow.livereload.setCurrentDeviceIP(currentDeviceIP)

    @QtCore.Slot()
    def updateDeviceList(self):
        self.deviceList = luainterface.search(self.mainWindow.moaiWidget.lua)
        print(self.deviceList)
        self.ui.availableDevicesList.clear()
        for d in self.deviceList:
            self.ui.availableDevicesList.addItem("%s [%s]" % (d['name'], d['ip']))

    @QtCore.Slot()
    def reloadMoai(self):
        self.mainWindow.reloadMoai()

    @QtCore.Slot()
    def clearRemoteOverrides(self):
        self.mainWindow.livereload.clearRemoteOverrides()


    @QtCore.Slot(int)
    def setCountryCode(self, idx):
        country = self.ui.countryBox.itemData(idx)
        if country:
            locale = QLocale(Languages[self.ui.languageBox.currentIndex()], QLocale.Country(country))
            name = locale.name()
            codes = name.split('_')
            self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('languageCode', '%s')" % codes[0])
            self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('countryCode', '%s')" % codes[1])


    @QtCore.Slot(int)
    def setLanguageCode(self, idx):
        self.updateCountriesCombobox(idx)

    def updateCountriesCombobox(self, languageIdx):
        if not languageIdx in Languages:
            languageIdx = DEFAULT_LANGUAGE_CODE

        countries = QLocale.countriesForLanguage(Languages[languageIdx])
        countryBox = self.ui.countryBox
        countryBox.clear()
        for country in countries:
            countryBox.addItem(QLocale.countryToString(country), country)


    @QtCore.Slot()
    def browseDocuments(self):
        projectDir = self.mainWindow.workingDir
        currentDocs = os.path.join(projectDir, self.ui.documentsBtn.text())
        upOneLevel = os.path.normpath( os.path.join(currentDocs, '..') )
        docsDir = QtGui.QFileDialog.getExistingDirectory(self, "Choose document directory", upOneLevel)
        if docsDir:
            relPath = os.path.relpath(docsDir, projectDir)
            self.ui.documentsBtn.setText(relPath)
            self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('documentDirectory', '%s')" % relPath )


    def viewSizeEditingFinished(self):
        try:
            width = float(self.ui.widthEdit.text())
        except ValueError:
            width = 640

        try:
            height = float(self.ui.heightEdit.text())
        except ValueError:
            height = 480

        self.mainWindow.resizeMoaiView(width, height)

    @QtCore.Slot(str)
    def setScreenDpi(self, dpiStr):
        try:
            dpi = float(dpiStr)
        except ValueError:
            dpi = 132

        self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('screenDpi', %f)" % dpi )


    @QtCore.Slot()
    def onStartSession(self):
        self.startSession(self.ui.sessionResume.isChecked())

    @QtCore.Slot()
    def onEndSession(self):
        self.mainWindow.moaiWidget.runString ( "if MOAIApp then MOAIApp.dispatchEvent (MOAIApp.SESSION_END) end" )

    @QtCore.Slot()
    def onOpenedFromUrl(self):
        url = self.ui.urlEdit.text()
        self.mainWindow.moaiWidget.runString ( "if MOAIApp then MOAIApp.dispatchEvent (MOAIApp.APP_OPENED_FROM_URL, '%s') end" % url )

    @QtCore.Slot()
    def sendNotification(self):
        userInfo = self.ui.pushUserInfo.document().toPlainText()
        event = 'MOAINotifications.LOCAL_NOTIFICATION_MESSAGE_RECEIVED'
        if self.ui.pushLocal.isChecked():
            event = 'MOAINotifications.REMOTE_NOTIFICATION_MESSAGE_RECEIVED'

        self.mainWindow.moaiWidget.runString ( "if MOAIApp then MOAINotifications.dispatchEvent (%s, %s) end" % (event, userInfo) )


    def startSession(self, resume):
        flag = 'true' if resume else 'false'
        self.mainWindow.moaiWidget.runString ( "if MOAIApp then MOAIApp.dispatchEvent (MOAIApp.SESSION_START, %s) end" % flag )


    def applyEnvironmentSettings(self):
        lang = Languages[self.ui.languageBox.currentIndex()]
        country = QLocale.Country(self.ui.countryBox.itemData(self.ui.countryBox.currentIndex()))

        locale = QLocale(lang, country)
        name = locale.name()
        codes = name.split('_')

        relPath = self.ui.documentsBtn.text()
        dpi = float(self.ui.dpiEdit.text())

        self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('languageCode', '%s')" % codes[0])
        self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('countryCode', '%s')" % codes[1])
        self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('screenDpi', %f)" % dpi )
        self.mainWindow.moaiWidget.runString( "MOAIEnvironment.setValue('documentDirectory', '%s')" % relPath )
