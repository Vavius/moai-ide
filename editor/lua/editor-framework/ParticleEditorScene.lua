--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Scene = require("core.Scene")

local ParticleEditorScene = class(Scene)

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:init(params)
    Scene.init(self, params)

    self:addEventListener(Event.ENTER, self.onEnter, self)
    self:addEventListener(Event.EXIT, self.onExit, self)
    self:addEventListener(Event.DID_EXIT, self.onDidExit, self)
    self:addEventListener(Event.WILL_ENTER, self.onWillEnter, self)

    self:createLayer()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- called before transition
function ParticleEditorScene:onWillEnter(event)

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- called after transition
function ParticleEditorScene:onEnter()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- called before transition
function ParticleEditorScene:onExit()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- called after transition
function ParticleEditorScene:onDidExit()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleEditorScene:createLayer()
    local layer = Display.Layer()

    layer:setTouchEnabled(true)
    self:addLayer(layer)
end


return ParticleEditorScene
