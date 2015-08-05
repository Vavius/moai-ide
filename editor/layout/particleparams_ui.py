# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'particleparams.ui'
#
# Created: Wed Aug  5 14:50:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_particleParams(object):
    def setupUi(self, particleParams):
        particleParams.setObjectName("particleParams")
        particleParams.resize(393, 748)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.paramsView = QtGui.QTreeView(self.dockWidgetContents)
        self.paramsView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.paramsView.setTabKeyNavigation(True)
        self.paramsView.setAlternatingRowColors(True)
        self.paramsView.setIndentation(0)
        self.paramsView.setObjectName("paramsView")
        self.verticalLayout.addWidget(self.paramsView)
        particleParams.setWidget(self.dockWidgetContents)

        self.retranslateUi(particleParams)
        QtCore.QMetaObject.connectSlotsByName(particleParams)

    def retranslateUi(self, particleParams):
        particleParams.setWindowTitle(QtGui.QApplication.translate("particleParams", "Particle Params", None, QtGui.QApplication.UnicodeUTF8))

