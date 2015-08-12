# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outlinerdock.ui'
#
# Created: Tue Aug 11 18:48:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_outlinerdock(object):
    def setupUi(self, outlinerdock):
        outlinerdock.setObjectName("outlinerdock")
        outlinerdock.resize(400, 359)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        outlinerdock.setWidget(self.dockWidgetContents)

        self.retranslateUi(outlinerdock)
        QtCore.QMetaObject.connectSlotsByName(outlinerdock)

    def retranslateUi(self, outlinerdock):
        outlinerdock.setWindowTitle(QtGui.QApplication.translate("outlinerdock", "Outliner", None, QtGui.QApplication.UnicodeUTF8))

