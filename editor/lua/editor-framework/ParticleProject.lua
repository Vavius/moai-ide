--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local ParticleProject = class()
ParticleProject.__className = "ParticleProject"


function ParticleProject:init()

end

function ParticleProject:serializeIn(serializer, data)
    self.particleLimit = data.particleLimit
    self.spriteLimit = data.spriteLimit
    self.wrapParticles = data.wrapParticles
    self.wrapSprites = data.wrapSprites
    self.bgColor = data.bgColor
    self.reverseDraw = data.reverseDraw
    self.texture = data.texture

    self.emitters = {}
    self.states = {}

    for _, id in pairs(data.emitters) do
        table.insert(self.emitters, serializer:getObjectById(id))
    end

    for _, id in pairs(data.states) do
        table.insert(self.states, serializer:getObjectById(id))
    end
end

function ParticleProject:serializeOut(serializer, out)
    out.particleLimit = self.particleLimit
    out.spriteLimit = self.spriteLimit
    out.wrapParticles = self.wrapParticles
    out.wrapSprites = self.wrapSprites
    out.bgColor = self.bgColor
    out.reverseDraw = self.reverseDraw
    out.texture = self.texture

    out.emitters = {}
    out.states = {}

    for _, v in pairs(self.emitters) do
        table.insert(out.emitters, serializer:affirmObjectId(v))
    end

    for _, v in pairs(self.states) do
        table.insert(out.states, serializer:affirmObjectId(v))
    end
end


return ParticleProject
