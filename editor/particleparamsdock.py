import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget, QAbstractItemView
from PySide.QtCore import QObject, Qt, QEvent

from layout.particleparams_ui import Ui_particleParams as Ui

from widgets.propertyitemmodel import PropertyItemModel, ComboDelegate
import luainterface


class MiddleDragFilter(QObject):
    midTracking = False
    midLast = 0
    callback = None

    speed = 0.1
    speedSlow = 0.01
    speedFast = 1

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                self.midTracking = True
                self.midLast = event.x()
                return True

        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.MiddleButton:
                self.midTracking = False
                return True

        if event.type() == QEvent.MouseMove:
            if self.midTracking:
                self.onDrag(event.x() - self.midLast)
                self.midLast = event.x()
                return True

        return QObject.eventFilter(self, obj, event)

    def onDrag(self, x):
        modif = QtGui.QApplication.keyboardModifiers()
        diff = x

        if modif == Qt.CTRL:
            diff *= self.speedSlow

        elif modif == Qt.SHIFT:
            diff *= self.speedFast

        else:
            diff *= self.speed

        if self.callback:
            self.callback(diff)

    def setCallback(self, func):
        self.callback = func


class ParticleParamsDock(QDockWidget):
    def __init__(self, parent=None):
        super(ParticleParamsDock, self).__init__(parent)

        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)
        self.mainWindow = self.parent()

        self.treeModel = PropertyItemModel(self)
        self.treeView = ui.paramsView
        ui.paramsView.setModel(self.treeModel)

        self.itemDelegate = ComboDelegate(self)
        ui.paramsView.setItemDelegate(self.itemDelegate)

        dragFilt = MiddleDragFilter(self)
        dragFilt.setCallback(self.dragParam)
        ui.paramsView.viewport().installEventFilter(dragFilt)

    def dragParam(self, diff):
        self.treeModel.applyOffset(self.treeView.currentIndex(), diff)

    def getModel(self):
        return self.treeModel

    def getTreeView(self):
        return self.ui.paramsView
