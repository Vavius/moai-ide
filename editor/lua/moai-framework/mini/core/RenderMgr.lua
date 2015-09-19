----------------------------------------------------------------------------------------------------
-- @type RenderMgr
--
-- This is a singleton class that manages the rendering object.
----------------------------------------------------------------------------------------------------

local RenderMgr = {}

function RenderMgr:initialize()
    self.renderTable = {}
    self.bufferTable = {}
    self.clearColor = MOAIColor.new()
    self.clearColor:setColor(0, 0, 0, 1)

    MOAIGfxDevice.getFrameBuffer():setClearColor(self.clearColor)

    MOAIRenderMgr.setRenderTable(self.renderTable)
    MOAIRenderMgr.setBufferTable(self.bufferTable)
end


function RenderMgr:addChild(render)
    table.insertIfAbsent(self.renderTable, render)
end


function RenderMgr:removeChild(render)
    table.removeElement(self.renderTable, render)
end


function RenderMgr:addBuffer(renderBuffer, index)
    index = index or (1 + #self.bufferTable)
    table.insert(self.bufferTable, index, renderBuffer)
end


function RenderMgr:removeBuffer(renderBuffer)
    table.removeElement(self.bufferTable, renderBuffer)
end


function RenderMgr:setClearColor(r, g, b, a)
    self.clearColor:setColor(r, g, b, a)
end


function RenderMgr:getClearColor()
    return self.clearColor:getColor()
end


return RenderMgr