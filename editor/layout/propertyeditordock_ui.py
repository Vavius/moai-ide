# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'propertyeditordock.ui'
#
# Created: Sun Aug  9 13:31:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_propertyeditordock(object):
    def setupUi(self, propertyeditordock):
        propertyeditordock.setObjectName("propertyeditordock")
        propertyeditordock.resize(457, 399)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        propertyeditordock.setWidget(self.dockWidgetContents)

        self.retranslateUi(propertyeditordock)
        QtCore.QMetaObject.connectSlotsByName(propertyeditordock)

    def retranslateUi(self, propertyeditordock):
        propertyeditordock.setWindowTitle(QtGui.QApplication.translate("propertyeditordock", "Property Editor", None, QtGui.QApplication.UnicodeUTF8))

