# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'particleeditor.ui'
#
# Created: Fri Jun 19 00:15:23 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_particleEditor(object):
    def setupUi(self, particleEditor):
        particleEditor.setObjectName("particleEditor")
        particleEditor.resize(365, 695)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listEmitter = QtGui.QListWidget(self.groupBox)
        self.listEmitter.setSelectionRectVisible(True)
        self.listEmitter.setObjectName("listEmitter")
        self.verticalLayout_2.addWidget(self.listEmitter)
        self.btnAddEmitter = QtGui.QPushButton(self.groupBox)
        self.btnAddEmitter.setObjectName("btnAddEmitter")
        self.verticalLayout_2.addWidget(self.btnAddEmitter)
        self.btnDeleteEmitter = QtGui.QPushButton(self.groupBox)
        self.btnDeleteEmitter.setObjectName("btnDeleteEmitter")
        self.verticalLayout_2.addWidget(self.btnDeleteEmitter)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listState = QtGui.QListWidget(self.groupBox_2)
        self.listState.setSelectionRectVisible(True)
        self.listState.setObjectName("listState")
        self.verticalLayout_3.addWidget(self.listState)
        self.btnAddState = QtGui.QPushButton(self.groupBox_2)
        self.btnAddState.setObjectName("btnAddState")
        self.verticalLayout_3.addWidget(self.btnAddState)
        self.btnDeleteState = QtGui.QPushButton(self.groupBox_2)
        self.btnDeleteState.setObjectName("btnDeleteState")
        self.verticalLayout_3.addWidget(self.btnDeleteState)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        particleEditor.setWidget(self.dockWidgetContents)

        self.retranslateUi(particleEditor)
        QtCore.QMetaObject.connectSlotsByName(particleEditor)

    def retranslateUi(self, particleEditor):
        particleEditor.setWindowTitle(QtGui.QApplication.translate("particleEditor", "Particle Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("particleEditor", "Emitters", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddEmitter.setText(QtGui.QApplication.translate("particleEditor", "New emitter", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteEmitter.setText(QtGui.QApplication.translate("particleEditor", "Remove emitter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("particleEditor", "Particle States", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddState.setText(QtGui.QApplication.translate("particleEditor", "New state", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteState.setText(QtGui.QApplication.translate("particleEditor", "Remove state", None, QtGui.QApplication.UnicodeUTF8))

