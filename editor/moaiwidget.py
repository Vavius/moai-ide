
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

# input sensors IDs
KEYBOARD, POINTER, MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, TOTAL = range(0, 6)

class MOAIWidget(QtOpenGL.QGLWidget):
    contextInitialized = QtCore.Signal()

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        AKUCreateContext()
        AKUInitializeUtil()
        AKUInitializeSim()
        AKUInitializeCallbacks()
        AKULoadLuaHeaders()

        AKUSetInputConfigurationName ( "AKUQtEditor" );

        AKUReserveInputDevices          ( 1 );
        AKUSetInputDevice               ( 0, "device" );
        
        AKUReserveInputDeviceSensors    ( 0, TOTAL );
        AKUSetInputDeviceKeyboard       ( 0, KEYBOARD,     "keyboard" );
        AKUSetInputDevicePointer        ( 0, POINTER,      "pointer" );
        AKUSetInputDeviceButton         ( 0, MOUSE_LEFT,   "mouseLeft" );
        AKUSetInputDeviceButton         ( 0, MOUSE_MIDDLE, "mouseMiddle" );
        AKUSetInputDeviceButton         ( 0, MOUSE_RIGHT,  "mouseRight" );

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

        self.contextInitialized.emit()

    def paintGL(self):
        AKURender()

    def simStep(self):
        AKUUpdate()

    def setSimStep(self, step):
        timer.setInterval(step * 1000)

    def getLuaRuntime(self):
        return LuaRuntime(luastate = AKUGetLuaState())

    # Input
    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        AKUEnqueuePointerEvent ( 0, POINTER, x, y )

    def mousePressEvent(self, event):
        button = event.button()

        if button == QtCore.Qt.LeftButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_LEFT, True)

        elif button == QtCore.Qt.RightButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_RIGHT, True)

        elif button == QtCore.Qt.MidButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_MIDDLE, True)

    def mouseReleaseEvent(self, event):
        button = event.button()

        if button == QtCore.Qt.LeftButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_LEFT, False)

        elif button == QtCore.Qt.RightButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_RIGHT, False)

        elif button == QtCore.Qt.MidButton:
            AKUEnqueueButtonEvent ( 0, MOUSE_MIDDLE, False)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Shift:
            AKUEnqueueKeyboardShiftEvent(0, KEYBOARD, True)

        elif key == QtCore.Qt.Key_Control:
            AKUEnqueueKeyboardControlEvent(0, KEYBOARD, True)

        elif key == QtCore.Qt.Key_Alt:
            AKUEnqueueKeyboardAltEvent(0, KEYBOARD, True)

        else:
            AKUEnqueueKeyboardEvent(0, KEYBOARD, key, True)


    def keyReleaseEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Shift:
            AKUEnqueueKeyboardShiftEvent(0, KEYBOARD, False)

        elif key == QtCore.Qt.Key_Control:
            AKUEnqueueKeyboardControlEvent(0, KEYBOARD, False)

        elif key == QtCore.Qt.Key_Alt:
            AKUEnqueueKeyboardAltEvent(0, KEYBOARD, False)

        else:
            AKUEnqueueKeyboardEvent(0, KEYBOARD, key, False)

    # Game Management API
    def runScript(self, fileName):
        AKURunScript(fileName)

    def runString(self, luaStr):
        AKURunString(luaStr)




