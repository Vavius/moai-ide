#!/usr/bin/python

import sys
import platform
import PySide

from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtGui import QApplication, QMainWindow

from ui_mainWindow import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget

class MainWindow(QMainWindow):
    luaRuntime = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.moaiWidget = MOAIWidget()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.moaiWidget)
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)

        actionPropertyEditor = ui.propertyEditor.toggleViewAction()
        actionObjectPallete = ui.objectPallete.toggleViewAction()
        
        ui.menuWindow.addAction(actionPropertyEditor)
        ui.menuWindow.addAction(actionObjectPallete)

        intValidator = PySide.QtGui.QIntValidator()
        intValidator.setRange(128, 4096)
        ui.widthEdit.setValidator(intValidator)
        ui.heightEdit.setValidator(intValidator)
        ui.widthEdit.textEdited.connect(self.viewSizeEditingFinished)
        ui.heightEdit.textEdited.connect(self.viewSizeEditingFinished)

        glSize = self.moaiWidget.sizeHint()
        ui.widthEdit.setText(str(glSize.width()))
        ui.heightEdit.setText(str(glSize.height()))

        self.moaiWidget.contextInitialized.connect(self.onContextInitialized)
    
    def onContextInitialized(self):
        self.luaRuntime = self.moaiWidget.getLuaRuntime()
        self.loadLuaFramework()
        self.runSample()

    def viewSizeEditingFinished(self):
        width = int(self.ui.widthEdit.text())
        height = int(self.ui.heightEdit.text())

        self.resizeMoaiView(width, height)

    def resizeMoaiView(self, width, height):
        self.moaiWidget.resize(width, height)

    # live reload
    def getRemoteDeviceList(self):
        self.luaRuntime.eval()

    def reloadFile(self, file):
        pass

    def loadLuaFramework(self):
        self.moaiWidget.runString("package.path = 'lua/moai-framework/src/?.lua;' .. package.path")
        self.moaiWidget.runScript("lua/moai-framework/src/include.lua")

    def runSample(self):
        self.moaiWidget.runString("""
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()

    # app.setStyleSheet(qdarkstyle.load_stylesheet())

    frame.show()
    app.exec_()




# print(lua.eval('python.eval(" 2 ** 2 ")') == 4)
# print(lua.eval('python.builtins.str(4)') == '4')