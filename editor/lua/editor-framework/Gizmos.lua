--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Gizmo = class()

function Gizmo:init()
    self.color = {1, 1, 1, 1}
    self.width = 1

    self.prop = MOAIProp.new()
    local deck = MOAIScriptDeck.new()
    deck:setRectCallback(function() return self:rect() end)
    deck:setTotalRectCallback(function() return self:rect() end)
    deck:setDrawCallback(function() self:draw() end)

    self.deck = deck
    self.prop:setDeck(deck)
end

function Gizmo:setColor(r, g, b, a)
    self.color = {r, g, b, a}
end

function Gizmo:setWidth(w)
    self.width = w
end

function Gizmo:rect()
    return 0, 0, 0, 0
end

function Gizmo:draw()
    MOAIGfxDevice.setPenColor(unpack(self.color))
    MOAIGfxDevice.setPenWidth(self.width)

    self:onDraw()
end

function Gizmo:onDraw()

end



--------------------------------------------------------------------------------
local Circle = class(Gizmo)

function Circle:init()
    Gizmo.init(self)

    self.r = 10
    self.x = 0
    self.y = 0
end

function Circle:setCenter(x, y)
    self.x = x
    self.y = y
end

function Circle:setRadius(r)
    self.r = r
end

function Circle:rect()
    local x, y, r = self.x, self.y, self.r
    return x - r, y - r, x + r, y + r
end

function Circle:onDraw()
    MOAIDraw.drawCircle(self.x, self.y, self.r)
end

--------------------------------------------------------------------------------
local Rect = class(Gizmo)

function Rect:init()
    Gizmo.init(self)

    self.verts = {0, 0, 0, 0}
end

function Rect:setVerts(xMin, yMin, xMax, yMax)
    self.verts = {xMin, yMin, xMax, yMax}
end

function Rect:rect()
    return unpack(self.verts)
end

function Rect:onDraw()
    MOAIDraw.drawRect(unpack(self.verts))
end

return {
    Circle = Circle,
    Rect = Rect
}
