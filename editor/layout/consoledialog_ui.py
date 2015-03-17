# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'consoledialog.ui'
#
# Created: Fri Mar 13 13:41:59 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Console(object):
    def setupUi(self, Console):
        Console.setObjectName("Console")
        Console.resize(774, 528)
        self.verticalLayout = QtGui.QVBoxLayout(Console)
        self.verticalLayout.setContentsMargins(2, 12, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Console)
        self.tabWidget.setObjectName("tabWidget")
        self.localLogTab = QtGui.QWidget()
        self.localLogTab.setObjectName("localLogTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.localLogTab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.localConsoleTextBox = QConsole(self.localLogTab)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.localConsoleTextBox.setFont(font)
        self.localConsoleTextBox.setCenterOnScroll(False)
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

        self.retranslateUi(Console)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Console)

    def retranslateUi(self, Console):
        Console.setWindowTitle(QtGui.QApplication.translate("Console", "Lua console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.localLogTab), QtGui.QApplication.translate("Console", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mobileLogTab), QtGui.QApplication.translate("Console", "Device", None, QtGui.QApplication.UnicodeUTF8))

from widgets.qconsole import QConsole
