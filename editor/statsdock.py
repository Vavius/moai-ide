import sys
import PySide
import os

from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget

from colorama import Fore, Back, Style
from time import strftime

from layout.statsdock_ui import Ui_statsdock as Ui



class StatsDock(QDockWidget):
    def __init__(self, parent=None):
        super(StatsDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        self.mainWindow = self.parent()
        self.statsFunc = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateStats)

    def setLuaState(self, lua):
        self.statsFunc = lua.eval("""function()
            local fps = MOAISim.getPerformance()
            local drawcalls = MOAIGfxDevice.getFrameBuffer():getPerformanceDrawCount()
            local luaCount = MOAISim.getLuaObjectCount()
            local mem = MOAISim.getMemoryUsage()
            return math.round(fps, 0.1), drawcalls, luaCount, mem.lua, mem.texture
        end""")

    def startTimer(self):
        self.timer.start(600)

    def stopTimer(self):
        self.timer.stop()
        self.statsFunc = None

    def updateStats(self):
        if self.statsFunc:
            fps, drawcalls, luaCount, luaMem, textureMem = self.statsFunc()
            self.ui.valueFps.setText(str(fps))
            self.ui.valueDrawCalls.setText(str(drawcalls))
            self.ui.valueLuaCount.setText( '{:,}'.format(int(luaCount)) )
            self.ui.valueLuaMemory.setText( '{:,}'.format(int(luaMem)) )
            self.ui.valeuTextureMemory.setText( '{:,}'.format(int(textureMem)) )