# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profilerdock.ui'
#
# Created: Wed Aug  5 14:50:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_profilerdock(object):
    def setupUi(self, profilerdock):
        profilerdock.setObjectName("profilerdock")
        profilerdock.resize(234, 468)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setEnabled(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.shinyProfiler = QtGui.QCheckBox(self.groupBox)
        self.shinyProfiler.setObjectName("shinyProfiler")
        self.verticalLayout.addWidget(self.shinyProfiler)
        self.shinyUpdateBtn = QtGui.QPushButton(self.groupBox)
        self.shinyUpdateBtn.setEnabled(False)
        self.shinyUpdateBtn.setObjectName("shinyUpdateBtn")
        self.verticalLayout.addWidget(self.shinyUpdateBtn)
        self.shinyClearBtn = QtGui.QPushButton(self.groupBox)
        self.shinyClearBtn.setEnabled(False)
        self.shinyClearBtn.setObjectName("shinyClearBtn")
        self.verticalLayout.addWidget(self.shinyClearBtn)
        self.shinyFlatBtn = QtGui.QPushButton(self.groupBox)
        self.shinyFlatBtn.setEnabled(False)
        self.shinyFlatBtn.setObjectName("shinyFlatBtn")
        self.verticalLayout.addWidget(self.shinyFlatBtn)
        self.shinyTreeBtn = QtGui.QPushButton(self.groupBox)
        self.shinyTreeBtn.setEnabled(False)
        self.shinyTreeBtn.setObjectName("shinyTreeBtn")
        self.verticalLayout.addWidget(self.shinyTreeBtn)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.actionProfiler = QtGui.QCheckBox(self.dockWidgetContents)
        self.actionProfiler.setObjectName("actionProfiler")
        self.gridLayout.addWidget(self.actionProfiler, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        profilerdock.setWidget(self.dockWidgetContents)

        self.retranslateUi(profilerdock)
        QtCore.QObject.connect(self.actionProfiler, QtCore.SIGNAL("toggled(bool)"), profilerdock.toggleActionProfiling)
        QtCore.QObject.connect(self.shinyProfiler, QtCore.SIGNAL("toggled(bool)"), profilerdock.toggleShiny)
        QtCore.QObject.connect(self.shinyClearBtn, QtCore.SIGNAL("clicked()"), profilerdock.shinyClear)
        QtCore.QObject.connect(self.shinyFlatBtn, QtCore.SIGNAL("clicked()"), profilerdock.shinyFlatReport)
        QtCore.QObject.connect(self.shinyTreeBtn, QtCore.SIGNAL("clicked()"), profilerdock.shinyTreeReport)
        QtCore.QObject.connect(self.shinyProfiler, QtCore.SIGNAL("toggled(bool)"), self.shinyClearBtn.setEnabled)
        QtCore.QObject.connect(self.shinyProfiler, QtCore.SIGNAL("toggled(bool)"), self.shinyFlatBtn.setEnabled)
        QtCore.QObject.connect(self.shinyProfiler, QtCore.SIGNAL("toggled(bool)"), self.shinyTreeBtn.setEnabled)
        QtCore.QObject.connect(self.shinyProfiler, QtCore.SIGNAL("toggled(bool)"), self.shinyUpdateBtn.setEnabled)
        QtCore.QObject.connect(self.shinyUpdateBtn, QtCore.SIGNAL("clicked()"), profilerdock.shinyUpdate)
        QtCore.QMetaObject.connectSlotsByName(profilerdock)

    def retranslateUi(self, profilerdock):
        profilerdock.setWindowTitle(QtGui.QApplication.translate("profilerdock", "Profiler", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("profilerdock", "Shiny Profiler", None, QtGui.QApplication.UnicodeUTF8))
        self.shinyProfiler.setText(QtGui.QApplication.translate("profilerdock", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.shinyUpdateBtn.setText(QtGui.QApplication.translate("profilerdock", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.shinyClearBtn.setText(QtGui.QApplication.translate("profilerdock", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.shinyFlatBtn.setText(QtGui.QApplication.translate("profilerdock", "Flat Report", None, QtGui.QApplication.UnicodeUTF8))
        self.shinyTreeBtn.setText(QtGui.QApplication.translate("profilerdock", "Tree Report", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProfiler.setText(QtGui.QApplication.translate("profilerdock", "Action Profiling", None, QtGui.QApplication.UnicodeUTF8))

