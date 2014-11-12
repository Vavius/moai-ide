# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'consoledock.ui'
#
# Created: Wed Nov 12 16:43:37 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_consoledock(object):
    def setupUi(self, consoledock):
        consoledock.setObjectName("consoledock")
        consoledock.resize(939, 641)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(2, 0, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.localLogTab = QtGui.QWidget()
        self.localLogTab.setObjectName("localLogTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.localLogTab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.localConsoleTextBox = QConsole(self.localLogTab)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(14)
        self.localConsoleTextBox.setFont(font)
        self.localConsoleTextBox.setCenterOnScroll(True)
        self.localConsoleTextBox.setObjectName("localConsoleTextBox")
        self.verticalLayout_2.addWidget(self.localConsoleTextBox)
        self.tabWidget.addTab(self.localLogTab, "")
        self.mobileLogTab = QtGui.QWidget()
        self.mobileLogTab.setObjectName("mobileLogTab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.mobileLogTab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.deviceConsoleTextBox = QtGui.QTextEdit(self.mobileLogTab)
        self.deviceConsoleTextBox.setObjectName("deviceConsoleTextBox")
        self.verticalLayout_3.addWidget(self.deviceConsoleTextBox)
        self.tabWidget.addTab(self.mobileLogTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        consoledock.setWidget(self.dockWidgetContents)

        self.retranslateUi(consoledock)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(consoledock)

    def retranslateUi(self, consoledock):
        consoledock.setWindowTitle(QtGui.QApplication.translate("consoledock", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.localLogTab), QtGui.QApplication.translate("consoledock", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mobileLogTab), QtGui.QApplication.translate("consoledock", "Device", None, QtGui.QApplication.UnicodeUTF8))

from widgets.qconsole import QConsole
