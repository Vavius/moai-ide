
# MOAI OpenGL qt widget
#

import sys
import lupa
import moaipy

from PySide import QtCore, QtGui, QtOpenGL
from lupa import LuaRuntime
from moaipy import *
from OpenGL.GL import *
from OpenGL.GLU import *


class MOAIWidget(QtOpenGL.QGLWidget):
    contextInitialized = QtCore.Signal()

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)

        AKUCreateContext()
        AKUInitializeUtil()
        AKUInitializeSim()
        AKUInitializeCallbacks()
        AKULoadLuaHeaders()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateGL)
        timer.timeout.connect(self.simStep)
        timer.start(1000 * AKUGetSimStep())
        self.timer = timer

        moaipy.callback_SetSimStep = self.setSimStep

    # Qt callbacks and overrides
    def sizeHint(self):
        return QtCore.QSize(640, 480)

    def resizeGL(self, w, h):
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

    def initializeGL(self):
        AKUDetectGfxContext()

        w = self.size().width()
        h = self.size().height()
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

        self.luaRuntime = LuaRuntime(luastate = AKUGetLuaState())
        self.contextInitialized.emit()

    def paintGL(self):
        AKURender()

    def simStep(self):
        AKUUpdate()

    def setSimStep(self, step):
        timer.setInterval(step * 1000)

    # Game Management API
    def runScript(self, fileName):
        AKURunScript(fileName)

    def runString(self, luaStr):
        AKURunString(luaStr)




