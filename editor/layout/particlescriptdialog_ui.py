# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'particlescriptdialog.ui'
#
# Created: Thu Aug 13 17:28:02 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ParticleScriptDialog(object):
    def setupUi(self, ParticleScriptDialog):
        ParticleScriptDialog.setObjectName("ParticleScriptDialog")
        ParticleScriptDialog.resize(731, 664)
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
        self.btnLoad = QtGui.QPushButton(ParticleScriptDialog)
        self.btnLoad.setObjectName("btnLoad")
        self.gridLayout.addWidget(self.btnLoad, 0, 0, 1, 1)
        self.btnLoadState = QtGui.QPushButton(ParticleScriptDialog)
        self.btnLoadState.setObjectName("btnLoadState")
        self.gridLayout.addWidget(self.btnLoadState, 0, 2, 1, 1)
        self.btnSaveAs = QtGui.QPushButton(ParticleScriptDialog)
        self.btnSaveAs.setObjectName("btnSaveAs")
        self.gridLayout.addWidget(self.btnSaveAs, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(ParticleScriptDialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ParticleScriptDialog)

    def retranslateUi(self, ParticleScriptDialog):
        ParticleScriptDialog.setWindowTitle(QtGui.QApplication.translate("ParticleScriptDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInit), QtGui.QApplication.translate("ParticleScriptDialog", "Init script", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRender), QtGui.QApplication.translate("ParticleScriptDialog", "Render script", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoad.setText(QtGui.QApplication.translate("ParticleScriptDialog", "Load from state", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadState.setText(QtGui.QApplication.translate("ParticleScriptDialog", "Load custom script", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAs.setText(QtGui.QApplication.translate("ParticleScriptDialog", "Save as", None, QtGui.QApplication.UnicodeUTF8))

from widgets.particlescripteditor import ParticleScriptEditor
