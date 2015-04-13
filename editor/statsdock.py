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
            local node = STATS and STATS.nodeMgr or 0
            local action = STATS and STATS.actionTree or 0
            return math.round(fps, 0.1), drawcalls, luaCount, mem.lua, mem.texture, math.round(node, 0.01), math.round(action, 0.01)
        end""")

        self.mean = lua.eval("""function()
            STATS = {}
            local coro = MOAICoroutine.new()

            local nIdx = 0
            local node = {0}
            local action = {0}
            local buffer = 10
            coro:run(function()
                while true do
                    local _, a, n = MOAISim.getPerformance()
                    nIdx = (nIdx + 1) % buffer
                    action[nIdx + 1] = a
                    node[nIdx + 1] = n

                    local nodeMgrTime = 0
                    local actionTreeTime = 0
                    for i = 1, #action do
                        nodeMgrTime = nodeMgrTime + node[i]
                        actionTreeTime = actionTreeTime + action[i]
                    end
                    STATS.nodeMgr = 1000 * nodeMgrTime / buffer
                    STATS.actionTree = 1000 * actionTreeTime / buffer
                    coroutine.yield()
                end
            end)
        end""")
        self.mean()

    def startTimer(self):
        self.timer.start(600)

    def stopTimer(self):
        self.timer.stop()
        self.statsFunc = None

    def updateStats(self):
        if self.statsFunc:
            fps, drawcalls, luaCount, luaMem, textureMem, actionTree, nodeMgr = self.statsFunc()
            self.ui.valueFps.setText(str(fps))
            self.ui.valueDrawCalls.setText(str(drawcalls))
            self.ui.valueLuaCount.setText( '{:,}'.format(int(luaCount)) )
            self.ui.valueLuaMemory.setText( '{:,}'.format(int(luaMem)) )
            self.ui.valeuTextureMemory.setText( '{:,}'.format(int(textureMem)) )
            self.ui.valueNodeMgr.setText(str(actionTree))
            self.ui.valueActionTree.setText(str(nodeMgr))

