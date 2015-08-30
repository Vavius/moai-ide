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
    local segLen = 8
    local r = self.r
    local segCount = math.clamp(2 * math.pi * r / segLen, 8, 64)

    MOAIDraw.drawCircle(self.x, self.y, r, segCount)
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

--------------------------------------------------------------------------------
local Locator = class(Gizmo)

function Locator:init()
    Gizmo.init(self)
    self.size = 10
end

function Locator:setSize(s)
    self.size = s
end

function Locator:rect()
    local s = self.size
    return -s, -s, s, s
end

function Locator:onDraw()
    local s = self.size
    local r = 0.7 * s
    local segLen = 8

    local segCount = math.clamp(2 * math.pi * r / segLen, 8, 32)

    MOAIDraw.drawLine(-s, 0, s, 0)
    MOAIDraw.drawLine(0, -s, 0, s)
    MOAIDraw.drawCircle(0, 0, r, segCount)
end

--------------------------------------------------------------------------------
local VectorField = class(Gizmo)

function VectorField:init()
    Gizmo.init(self)
    self.x = 10
    self.y = 7
end

function VectorField:setSize(x, y)
    self.x = x
    self.y = y
end

function VectorField:rect()
    return -self.x, -self.y, self.x, self.y
end

function VectorField:onDraw()
    local d = math.distance(self.x, self.y)
    local x, y = self.x/d, self.y/d
    local l = 10 + math.sqrt(d)
    local off = 10
    local lArrow = 6
    local a = math.atan2(-y, -x)

    for i = -1, 1 do
        local offX, offY = y * off * i, -x * off * i
        if i == 0 then
            offX = offX + 0.7 * off * x
            offY = offY + 0.7 * off * y
        end

        local x1, y1, x2, y2 = offX - l * x, offY - l * y, offX + l * x, offY + l * y
        MOAIDraw.drawLine(x1, y1, x2, y2)
        MOAIDraw.drawLine(
            x2 + lArrow * math.cos(a - 0.5), y2 + lArrow * math.sin(a - 0.5),
            x2, y2,
            x2 + lArrow * math.cos(a + 0.5), y2 + lArrow * math.sin(a + 0.5))
    end
end



return {
    Circle = Circle,
    Rect = Rect,
    Locator = Locator,
    VectorField = VectorField,
}
