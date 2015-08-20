# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'particlescriptdialog.ui'
#
# Created: Thu Aug 20 12:59:56 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ParticleScriptDialog(object):
    def setupUi(self, ParticleScriptDialog):
        ParticleScriptDialog.setObjectName("ParticleScriptDialog")
        ParticleScriptDialog.resize(731, 635)
        self.verticalLayout = QtGui.QVBoxLayout(ParticleScriptDialog)
        self.verticalLayout.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(ParticleScriptDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabInit = QtGui.QWidget()
        self.tabInit.setObjectName("tabInit")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabInit)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.initScript = ParticleScriptEditor(self.tabInit)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(12)
        self.initScript.setFont(font)
        self.initScript.setObjectName("initScript")
        self.verticalLayout_3.addWidget(self.initScript)
        self.tabWidget.addTab(self.tabInit, "")
        self.tabRender = QtGui.QWidget()
        self.tabRender.setObjectName("tabRender")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabRender)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.renderScript = ParticleScriptEditor(self.tabRender)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(12)
        self.renderScript.setFont(font)
        self.renderScript.setObjectName("renderScript")
        self.verticalLayout_4.addWidget(self.renderScript)
        self.tabWidget.addTab(self.tabRender, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btnOpen = QtGui.QToolButton(ParticleScriptDialog)
        self.btnOpen.setObjectName("btnOpen")
        self.gridLayout.addWidget(self.btnOpen, 0, 1, 1, 1)
        self.btnSaveAs = QtGui.QToolButton(ParticleScriptDialog)
        self.btnSaveAs.setObjectName("btnSaveAs")
        self.gridLayout.addWidget(self.btnSaveAs, 1, 2, 1, 1)
        self.btnSave = QtGui.QToolButton(ParticleScriptDialog)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 0, 2, 1, 1)
        self.btnLoadFromState = QtGui.QToolButton(ParticleScriptDialog)
        self.btnLoadFromState.setObjectName("btnLoadFromState")
        self.gridLayout.addWidget(self.btnLoadFromState, 0, 0, 1, 1)
        self.btnLoadCustom = QtGui.QToolButton(ParticleScriptDialog)
        self.btnLoadCustom.setObjectName("btnLoadCustom")
        self.gridLayout.addWidget(self.btnLoadCustom, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(ParticleScriptDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ParticleScriptDialog)

    def retranslateUi(self, ParticleScriptDialog):
        ParticleScriptDialog.setWindowTitle(QtGui.QApplication.translate("ParticleScriptDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInit), QtGui.QApplication.translate("ParticleScriptDialog", "Init script", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRender), QtGui.QApplication.translate("ParticleScriptDialog", "Render script", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOpen.setText(QtGui.QApplication.translate("ParticleScriptDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAs.setText(QtGui.QApplication.translate("ParticleScriptDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("ParticleScriptDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadFromState.setText(QtGui.QApplication.translate("ParticleScriptDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadCustom.setText(QtGui.QApplication.translate("ParticleScriptDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

from widgets.particlescripteditor import ParticleScriptEditor
