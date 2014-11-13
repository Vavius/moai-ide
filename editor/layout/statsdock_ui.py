# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statsdock.ui'
#
# Created: Thu Nov 13 15:37:44 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_statsdock(object):
    def setupUi(self, statsdock):
        statsdock.setObjectName("statsdock")
        statsdock.resize(374, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.formLayout = QtGui.QFormLayout(self.dockWidgetContents)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.lblFps = QtGui.QLabel(self.dockWidgetContents)
        self.lblFps.setObjectName("lblFps")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblFps)
        self.valueFps = QtGui.QLabel(self.dockWidgetContents)
        self.valueFps.setObjectName("valueFps")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.valueFps)
        self.lblDrawCount = QtGui.QLabel(self.dockWidgetContents)
        self.lblDrawCount.setObjectName("lblDrawCount")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblDrawCount)
        self.valueDrawCalls = QtGui.QLabel(self.dockWidgetContents)
        self.valueDrawCalls.setObjectName("valueDrawCalls")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.valueDrawCalls)
        self.lblLuaCount = QtGui.QLabel(self.dockWidgetContents)
        self.lblLuaCount.setObjectName("lblLuaCount")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblLuaCount)
        self.valueLuaCount = QtGui.QLabel(self.dockWidgetContents)
        self.valueLuaCount.setObjectName("valueLuaCount")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.valueLuaCount)
        self.lblLuaMemory = QtGui.QLabel(self.dockWidgetContents)
        self.lblLuaMemory.setObjectName("lblLuaMemory")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lblLuaMemory)
        self.valueLuaMemory = QtGui.QLabel(self.dockWidgetContents)
        self.valueLuaMemory.setObjectName("valueLuaMemory")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.valueLuaMemory)
        self.lblTextureMemory = QtGui.QLabel(self.dockWidgetContents)
        self.lblTextureMemory.setObjectName("lblTextureMemory")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.lblTextureMemory)
        self.valeuTextureMemory = QtGui.QLabel(self.dockWidgetContents)
        self.valeuTextureMemory.setObjectName("valeuTextureMemory")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.valeuTextureMemory)
        statsdock.setWidget(self.dockWidgetContents)

        self.retranslateUi(statsdock)
        QtCore.QMetaObject.connectSlotsByName(statsdock)

    def retranslateUi(self, statsdock):
        statsdock.setWindowTitle(QtGui.QApplication.translate("statsdock", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.lblFps.setText(QtGui.QApplication.translate("statsdock", "FPS:", None, QtGui.QApplication.UnicodeUTF8))
        self.valueFps.setText(QtGui.QApplication.translate("statsdock", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDrawCount.setText(QtGui.QApplication.translate("statsdock", "Draw Calls:", None, QtGui.QApplication.UnicodeUTF8))
        self.valueDrawCalls.setText(QtGui.QApplication.translate("statsdock", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLuaCount.setText(QtGui.QApplication.translate("statsdock", "Lua Object Count:", None, QtGui.QApplication.UnicodeUTF8))
        self.valueLuaCount.setText(QtGui.QApplication.translate("statsdock", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLuaMemory.setText(QtGui.QApplication.translate("statsdock", "Lua Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.valueLuaMemory.setText(QtGui.QApplication.translate("statsdock", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTextureMemory.setText(QtGui.QApplication.translate("statsdock", "Texture Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.valeuTextureMemory.setText(QtGui.QApplication.translate("statsdock", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

