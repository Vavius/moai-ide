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
        self.stopFunc = None
        self.startFunc = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateStats)

    def setLuaState(self, lua):
        self.statsFunc = lua.eval("""function()
            local round = function(x, snap) return snap * math.floor(x / snap + 0.5) end

            local fps = MOAISim.getPerformance()
            local drawcalls = MOAIGfxDevice.getFrameBuffer():getPerformanceDrawCount()
            local luaCount = MOAISim.getLuaObjectCount()
            local mem = MOAISim.getMemoryUsage()
            local lua, texture = mem.lua, mem.texture
            local node = STATS and STATS.nodeMgr or 0
            local action = STATS and STATS.actionTree or 0
            local sim = STATS and STATS.simTime or 0
            local render = STATS and STATS.renderTime or 0
            return round(fps, 0.1), drawcalls, luaCount, lua, texture, 
                    round(node, 0.01), round(action, 0.01), round(sim, 0.01), round(render, 0.01)
        end""")

        self.startFunc = lua.eval("""function()
            STATS = {}
            STATS.thread = MOAICoroutine.new()

            local nIdx = 0
            local node = {0}
            local action = {0}
            local sim = {0}
            local render = {0}
            local buffer = 10
            STATS.thread:run(function()
                while true do
                    local _, a, n, s, r = MOAISim.getPerformance()
                    nIdx = (nIdx + 1) % buffer
                    action[nIdx + 1] = a
                    node[nIdx + 1] = n
                    sim[nIdx + 1] = s
                    render[nIdx + 1] = r
                    
                    local nodeMgrTime = 0
                    local actionTreeTime = 0
                    local simTime = 0
                    local renderTime = 0
                    for i = 1, #action do
                        nodeMgrTime = nodeMgrTime + node[i]
                        actionTreeTime = actionTreeTime + action[i]
                        simTime = simTime + sim[i]
                        renderTime = renderTime + render[i]
                    end
                    STATS.nodeMgr = 1000 * nodeMgrTime / buffer
                    STATS.actionTree = 1000 * actionTreeTime / buffer
                    STATS.simTime = 1000 * simTime / buffer
                    STATS.renderTime = 1000 * renderTime / buffer
                    coroutine.yield()
                end
            end)
        end""")

        self.stopFunc = lua.eval("""function()
            if STATS and STATS.thread then
                STATS.thread:stop()
                STATS.thread = nil
            end
        end""")

    def startTimer(self):
        self.timer.start(600)
        self.statsFunc()
        if self.startFunc:
            self.startFunc()

    def stopTimer(self):
        self.timer.stop()
        if self.stopFunc:
            self.stopFunc()

        self.statsFunc = None
        self.startFunc = None
        self.stopFunc = None


    def updateStats(self):
        if self.statsFunc:
            fps, drawcalls, luaCount, luaMem, textureMem, actionTree, nodeMgr, sim, render = self.statsFunc()
            self.ui.valueFps.setText(str(fps))
            self.ui.valueDrawCalls.setText(str(drawcalls))
            self.ui.valueLuaCount.setText( '{:,}'.format(int(luaCount)) )
            self.ui.valueLuaMemory.setText( '{:,}'.format(int(luaMem)) )
            self.ui.valeuTextureMemory.setText( '{:,}'.format(int(textureMem)) )
            self.ui.valueNodeMgr.setText(str(actionTree))
            self.ui.valueActionTree.setText(str(nodeMgr))
            self.ui.valueSim.setText(str(sim))
            self.ui.valueRender.setText(str(render))

