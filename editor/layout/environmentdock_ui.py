# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'environmentdock.ui'
#
# Created: Sun Apr 13 01:06:33 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_environmentdock(object):
    def setupUi(self, environmentdock):
        environmentdock.setObjectName("environmentdock")
        environmentdock.resize(301, 687)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 13, 1, 1, 1)
        self.dpiEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.dpiEdit.setObjectName("dpiEdit")
        self.gridLayout.addWidget(self.dpiEdit, 14, 2, 1, 1)
        self.widthEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.widthEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.widthEdit.setObjectName("widthEdit")
        self.gridLayout.addWidget(self.widthEdit, 10, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 10, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 9, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)
        self.countryBox = QtGui.QComboBox(self.dockWidgetContents)
        self.countryBox.setObjectName("countryBox")
        self.gridLayout.addWidget(self.countryBox, 17, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1)
        self.availableDevicesList = QtGui.QComboBox(self.dockWidgetContents)
        self.availableDevicesList.setObjectName("availableDevicesList")
        self.gridLayout.addWidget(self.availableDevicesList, 4, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(45, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.updateDevicesBtn = QtGui.QToolButton(self.dockWidgetContents)
        self.updateDevicesBtn.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resources/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.updateDevicesBtn.setIcon(icon)
        self.updateDevicesBtn.setIconSize(QtCore.QSize(16, 16))
        self.updateDevicesBtn.setAutoRaise(False)
        self.updateDevicesBtn.setObjectName("updateDevicesBtn")
        self.gridLayout.addWidget(self.updateDevicesBtn, 4, 3, 1, 1)
        self.fullAutoreload = QtGui.QCheckBox(self.dockWidgetContents)
        self.fullAutoreload.setObjectName("fullAutoreload")
        self.gridLayout.addWidget(self.fullAutoreload, 7, 2, 1, 1)
        self.localAutoreload = QtGui.QCheckBox(self.dockWidgetContents)
        self.localAutoreload.setFocusPolicy(QtCore.Qt.TabFocus)
        self.localAutoreload.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.localAutoreload.setObjectName("localAutoreload")
        self.gridLayout.addWidget(self.localAutoreload, 5, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(44, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 4, 1, 1)
        self.reloadNowBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.reloadNowBtn.setObjectName("reloadNowBtn")
        self.gridLayout.addWidget(self.reloadNowBtn, 8, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 426, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 20, 2, 1, 1)
        self.deviceAutoreload = QtGui.QCheckBox(self.dockWidgetContents)
        self.deviceAutoreload.setFocusPolicy(QtCore.Qt.TabFocus)
        self.deviceAutoreload.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.deviceAutoreload.setObjectName("deviceAutoreload")
        self.gridLayout.addWidget(self.deviceAutoreload, 6, 2, 1, 1)
        self.documentsBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.documentsBtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.documentsBtn.setAutoRepeat(False)
        self.documentsBtn.setDefault(False)
        self.documentsBtn.setFlat(True)
        self.documentsBtn.setObjectName("documentsBtn")
        self.gridLayout.addWidget(self.documentsBtn, 15, 2, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 14, 1, 1, 1)
        self.heightEdit = QtGui.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heightEdit.sizePolicy().hasHeightForWidth())
        self.heightEdit.setSizePolicy(sizePolicy)
        self.heightEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.heightEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.heightEdit.setObjectName("heightEdit")
        self.gridLayout.addWidget(self.heightEdit, 13, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.dockWidgetContents)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 17, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 15, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.dockWidgetContents)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 16, 1, 1, 1)
        self.languageBox = QtGui.QComboBox(self.dockWidgetContents)
        self.languageBox.setObjectName("languageBox")
        self.gridLayout.addWidget(self.languageBox, 16, 2, 1, 1)
        environmentdock.setWidget(self.dockWidgetContents)

        self.retranslateUi(environmentdock)
        QtCore.QObject.connect(self.reloadNowBtn, QtCore.SIGNAL("clicked()"), environmentdock.reloadMoai)
        QtCore.QObject.connect(self.localAutoreload, QtCore.SIGNAL("toggled(bool)"), environmentdock.setAutoreloadHost)
        QtCore.QObject.connect(self.fullAutoreload, QtCore.SIGNAL("toggled(bool)"), environmentdock.setAutoreloadFull)
        QtCore.QObject.connect(self.deviceAutoreload, QtCore.SIGNAL("toggled(bool)"), environmentdock.setAutoreloadDevice)
        QtCore.QObject.connect(self.availableDevicesList, QtCore.SIGNAL("currentIndexChanged(int)"), environmentdock.setCurrentDevice)
        QtCore.QObject.connect(self.updateDevicesBtn, QtCore.SIGNAL("clicked()"), environmentdock.updateDeviceList)
        QtCore.QObject.connect(self.dpiEdit, QtCore.SIGNAL("textChanged(QString)"), environmentdock.setScreenDpi)
        QtCore.QObject.connect(self.countryBox, QtCore.SIGNAL("currentIndexChanged(int)"), environmentdock.setCountryCode)
        QtCore.QObject.connect(self.languageBox, QtCore.SIGNAL("currentIndexChanged(int)"), environmentdock.setLanguageCode)
        QtCore.QObject.connect(self.documentsBtn, QtCore.SIGNAL("clicked()"), environmentdock.browseDocuments)
        QtCore.QMetaObject.connectSlotsByName(environmentdock)
        environmentdock.setTabOrder(self.availableDevicesList, self.updateDevicesBtn)
        environmentdock.setTabOrder(self.updateDevicesBtn, self.localAutoreload)
        environmentdock.setTabOrder(self.localAutoreload, self.deviceAutoreload)
        environmentdock.setTabOrder(self.deviceAutoreload, self.fullAutoreload)
        environmentdock.setTabOrder(self.fullAutoreload, self.reloadNowBtn)
        environmentdock.setTabOrder(self.reloadNowBtn, self.widthEdit)
        environmentdock.setTabOrder(self.widthEdit, self.heightEdit)
        environmentdock.setTabOrder(self.heightEdit, self.dpiEdit)
        environmentdock.setTabOrder(self.dpiEdit, self.documentsBtn)
        environmentdock.setTabOrder(self.documentsBtn, self.countryBox)

    def retranslateUi(self, environmentdock):
        environmentdock.setWindowTitle(QtGui.QApplication.translate("environmentdock", "Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("environmentdock", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("environmentdock", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("environmentdock", "Remote Device", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("environmentdock", "Auto Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.updateDevicesBtn.setText(QtGui.QApplication.translate("environmentdock", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.fullAutoreload.setText(QtGui.QApplication.translate("environmentdock", "Full reload", None, QtGui.QApplication.UnicodeUTF8))
        self.localAutoreload.setText(QtGui.QApplication.translate("environmentdock", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.reloadNowBtn.setText(QtGui.QApplication.translate("environmentdock", "Reload now", None, QtGui.QApplication.UnicodeUTF8))
        self.deviceAutoreload.setText(QtGui.QApplication.translate("environmentdock", "Device", None, QtGui.QApplication.UnicodeUTF8))
        self.documentsBtn.setText(QtGui.QApplication.translate("environmentdock", "docs/", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("environmentdock", "DPI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("environmentdock", "Country Code", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("environmentdock", "Documents", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("environmentdock", "Language Code", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
