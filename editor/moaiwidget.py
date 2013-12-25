
# MOAI OpenGL qt widget
#

import sys
from PySide import QtCore, QtGui, QtOpenGL

import lupa
from lupa import LuaRuntime
from moaipy import *

from OpenGL import GL

def test_lupa():
    moaiLuaState = AKUGetLuaState()
    lua = LuaRuntime(luastate = moaiLuaState)
    initSample = lua.eval("""
        function()
            viewport = MOAIViewport.new ()
            viewport:setSize ( 640, 480 )
            viewport:setScale ( 640, 480 )

            layer = MOAILayer.new ()
            layer:setViewport ( viewport )
            -- MOAIGfxDevice.getFrameBuffer ():setRenderTable( {layer} )
            MOAIRenderMgr.setRenderTable( {layer} )

            gfxQuad = MOAIGfxQuad2D.new ()
            gfxQuad:setTexture ( "moai.png" )
            gfxQuad:setRect ( -128, -128, 128, 128 )
            gfxQuad:setUVRect ( 0, 1, 1, 0 )

            prop = MOAIProp.new ()
            prop:setDeck ( gfxQuad )
            layer:insertProp ( prop )

            prop:moveRot ( 0, 0, 360, 1.5 )
        end
        """)
    initSample()

class MOAIWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        AKUCreateContext()
        AKUInitializeUtil()
        AKUInitializeSim()
        AKULoadLuaHeaders()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateGL)
        timer.timeout.connect(self.simStep)
        timer.start(1000 * AKUGetSimStep())

    # Qt callbacks and overrides
    def minimumSizeHint(self):
        return QtCore.QSize(640, 480)
 
    def sizeHint(self):
        return QtCore.QSize(640, 480)

    def resizeEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

    def initializeGL(self):
        # self.qglClearColor(self.trolltechPurple.darker())
        AKUDetectGfxContext()

        w = self.size().width()
        h = self.size().height()
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

        self.runString("""
            function onResize(width, height)
                viewport:setSize(width, height)
                viewport:setScale(width, height)
            end
            MOAIGfxDevice.setListener(MOAIGfxDevice.EVENT_RESIZE, onResize)

            viewport = MOAIViewport.new ()
            viewport:setSize ( 640, 480 )
            viewport:setScale ( 640, 480 )

            layer = MOAILayer.new ()
            layer:setViewport ( viewport )
            -- MOAIGfxDevice.getFrameBuffer ():setRenderTable( {layer} )
            MOAIRenderMgr.setRenderTable( {layer} )

            gfxQuad = MOAIGfxQuad2D.new ()
            gfxQuad:setTexture ( "moai.png" )
            gfxQuad:setRect ( -128, -128, 128, 128 )
            gfxQuad:setUVRect ( 0, 1, 1, 0 )

            prop = MOAIProp.new ()
            prop:setDeck ( gfxQuad )
            layer:insertProp ( prop )

            prop:moveRot ( 0, 0, 360, 1.5 )
        """)
 
    def paintGL(self):
        AKURender()

    def simStep(self):
        AKUUpdate()

    # Game Management API
    def runScript(self, fileName):
        AKURunScript(fileName)

    def runString(self, luaStr):
        AKURunString(luaStr)




