--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local App = require("core.App")

local ParticleEditorScene = class()

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:addGizmo(gizmo)
    gizmo.prop:setLayer(self.layer)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:init(params)
    self:createLayer()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:getBgColor()
    return self.color:getColor()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:getSystem()
    return self.system
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:start()
    RenderMgr:addChild(self.layer)
    self.system:start()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:stop()
    self.system:stop()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:createLayer()
    self.layer = MOAILayer.new()
    self.layer:setViewport(App.viewport)

    self.color = MOAIColor.new()
    self.color:setColor(0, 0, 0, 1)
    self.layer:setClearColor(self.color)

    local system = MOAIParticleSystem.new()
    system:setLayer(self.layer)
    self.system = system
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:setBgColor(r, g, b, a)
    self.color:setColor(r, g, b, a)
end


return ParticleEditorScene
