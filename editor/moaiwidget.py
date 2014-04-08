
# MOAI OpenGL qt widget
#

import os, sys
import moaipy

from PySide import QtCore, QtGui, QtOpenGL
from moaipy import *
from OpenGL.GL import *
from OpenGL.GLU import *

import luainterface

# input sensors IDs
KEYBOARD, POINTER, MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, TOTAL = range(0, 6)


class MOAIWidget(QtOpenGL.QGLWidget):
    windowReady = False

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.refreshContext()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateGL)
        timer.timeout.connect(self.simStep)
        timer.start(1000 * AKUGetSimStep())
        self.timer = timer


    # Qt callbacks and overrides
    def sizeHint(self):
        return QtCore.QSize(640, 480)

    def resizeGL(self, w, h):
        if self.windowReady:
            AKUSetScreenSize(w, h)
            AKUSetViewSize(w, h)

    def initializeGL(self):
        glReady = True
        glClearColor(0, 0, 0, 1)
        

    def paintGL(self):
        if self.windowReady:
            AKURender()
        else:
            glClear(GL_COLOR_BUFFER_BIT)

    def simStep(self):
        if self.windowReady:
            AKUUpdate()


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
    def refreshContext(self):
        context = AKUGetContext ()
        if context:
            AKUDeleteContext ( context )

        AKUAppInitialize ()
        AKUModulesAppInitialize ()

        AKUCreateContext ()
        AKUModulesContextInitialize ()

        AKUInitializeCallbacks ()

        AKUSetInputConfigurationName ( "AKUQtEditor" );

        AKUReserveInputDevices          ( 1 );
        AKUSetInputDevice               ( 0, "device" );
        
        AKUReserveInputDeviceSensors    ( 0, TOTAL );
        AKUSetInputDeviceKeyboard       ( 0, KEYBOARD,     "keyboard" );
        AKUSetInputDevicePointer        ( 0, POINTER,      "pointer" );
        AKUSetInputDeviceButton         ( 0, MOUSE_LEFT,   "mouseLeft" );
        AKUSetInputDeviceButton         ( 0, MOUSE_MIDDLE, "mouseMiddle" );
        AKUSetInputDeviceButton         ( 0, MOUSE_RIGHT,  "mouseRight" );

        AKULoadLuaHeaders ()
        self.runString("MOAIEnvironment.setValue('horizontalResolution', %d) MOAIEnvironment.setValue('verticalResolution', %d)" %
            ( int ( self.size().width() ), int ( self.size().height()) ) )
        # AKUSetWorkingDirectory()
        luaFrameworkPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lua/moai-framework/src/?.lua")
        self.runString("package.path = '%s;' .. package.path" % luaFrameworkPath)
        self.runString("require('include')")
        # self.runString("print(class)")

        self.lua = LuaRuntime()
        self.lua.init()

        moaipy.callback_SetSimStep = self.setSimStep
        moaipy.callback_OpenWindow = self.openWindow

        self.windowReady = False

    def openWindow(self, title, width, height):
        AKUDetectGfxContext()

        w = self.size().width()
        h = self.size().height()
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

        self.windowReady = True

    def setSimStep(self, step):
        timer.setInterval(step * 1000)

    def setWorkingDirectory(self, path):
        AKUSetWorkingDirectory(path)

    def runScript(self, fileName):
        AKURunScript(fileName)

    def runString(self, luaStr):
        AKURunString(luaStr)

    def setTraceback(self, func):
        setFunc = self.lua.eval("function(func) _G.pythonLogFunc = func end")
        setFunc(func)
        self.lua.execute("MOAISim.setTraceback(function(err) _G.pythonLogFunc(debug.traceback(err, 2)) return 'hello from python' end)")

    def setPrint(self, before, after):
        setFunc = self.lua.eval("""function(before, after) 
            _print = print
            print = function(...)
                before()
                _print(...)
                after()
            end
        end""")
        setFunc(before, after)


