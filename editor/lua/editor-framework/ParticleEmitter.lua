--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local ParticleEmitter = class()

local SHAPE_RECT = 0
local SHAPE_CIRCLE = 1

local COMMON = {
    { type = "string",  name = "Name", value = "emitter", access = "Name" },
    { type = "int",     name = "Emission min", value = 1, access = "EmissionMin" },
    { type = "int",     name = "Emission max", value = 1, access = "EmissionMax" },
    { type = "list",    name = "State", value = 0, access = "State", choices = {} },
    -- { type = "list",    name = "Type",      value = 0, choices = {'Timed', 'Distance'}, access = "Type" },
    { type = "float",   name = "Frequency min", value = 1, access = "FrequencyMin" },
    { type = "float",   name = "Frequency max", value = 1, access = "FrequencyMax" },
    { type = "float",   name = "Angle min", value = 0, access = "AngleMin" },
    { type = "float",   name = "Angle max", value = 0, access = "AngleMax" },
    { type = "float",   name = "Velocity min", value = 0, access = "MagnitudeMin" },
    { type = "float",   name = "Velocity max", value = 0, access = "MagnitudeMax" },
    { type = "list",    name = "Shape", value = SHAPE_RECT, choices = {'Rect', 'Circle'}, access = "Shape" },
}

local CIRCLE = {
    { type = "float",   name = "Radius min", value = 10, access = "RadiusMin" },
    { type = "float",   name = "Radius max", value = 10, access = "RadiusMax" },
}

local RECT = {
    { type = "float",   name = "Left",      value = -10, access = "Left" },
    { type = "float",   name = "Bottom",    value = -10, access = "Bottom" },
    { type = "float",   name = "Right",     value = 10,  access = "Right" },
    { type = "float",   name = "Top",       value = 10,  access = "Top" },
}


function ParticleEmitter:getModelData()
    local data = {}
    for _, p in ipairs(COMMON) do
        local getter = self['get' .. p.access]
        local value = getter()

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
        }

        if p.access == 'State' then
            item.choices = require('ParticleEditor').listStates()
        elseif p.type == 'list' then
            item.choices = p.choices
        end

        table.insert(data, item)
    end

    local shape
    if self:getShape() == SHAPE_RECT then
        shape = RECT
    else
        shape = CIRCLE
    end
    for _, p in ipairs(shape) do
        local getter = self['get' .. p.access]
        local value = getter()

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
        }

        table.insert(data, item)
    end
    
    return { group = 'Emitter', items = data }
end


function ParticleEmitter:getParam(paramId)
    local getter = self['get' .. paramId]
    if not getter then
        log.error("No getter for " .. paramId)
        return
    end

    return getter()
end


function ParticleEmitter:init(system)
    local emitter = MOAIParticleTimedEmitter.new()
    emitter:setSystem(system)

    self.angle = {0, 0}
    self.emission = {0, 0}
    self.freq = {0, 0}
    self.mag = {0, 0}
    self.radius = {0, 0}
    self.rect = {0, 0, 0, 0}

    for _, default in ipairs(COMMON) do
        local setter = 'set' .. default.access
        self[setter](default.value)
    end

    for _, default in ipairs(RECT) do
        local setter = 'set' .. default.access
        self[setter](default.value)
    end
end


function ParticleEmitter:setParam(paramId, value)
    local setter = self['set' .. paramId]
    if not setter then
        log.error("No setter for " .. paramId)
        return
    end

    setter(value)
end


--============================================================================--
-- Attribute accessors
--============================================================================--

function ParticleEmitter:getAngleMax()
    return self.angle[2]
end

function ParticleEmitter:getAngleMin()
    return self.angle[1]
end

function ParticleEmitter:getBottom()
    return self.rect[2]
end

function ParticleEmitter:getEmissionMax()
    return self.emission[2]
end

function ParticleEmitter:getEmissionMin()
    return self.emission[1]
end

function ParticleEmitter:getLeft()
    return self.rect[1]
end

function ParticleEmitter:getMagnitudeMax()
    return self.mag[2]
end

function ParticleEmitter:getMagnitudeMin()
    return self.mag[1]
end

function ParticleEmitter:getName()
    return self.name
end

function ParticleEmitter:getRadiusMax()
    return self.radius[2]
end

function ParticleEmitter:getRadiusMin()
    return self.radius[1]
end

function ParticleEmitter:getRight()
    return self.rect[3]
end

function ParticleEmitter:getShape()
    return self.shape
end

function ParticleEmitter:getState()
    return self.state
end

function ParticleEmitter:getTop()
    return self.rect[4]
end


function ParticleEmitter:setAngleMax(value)
    self.angle[2] = value
    self.emitter:setAngle(unpack(self.angle))
end

function ParticleEmitter:setAngleMin(value)
    self.angle[1] = value
    self.emitter:setAngle(unpack(self.angle))
end

function ParticleEmitter:setBottom(value)
    self.rect[2] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
    end
end

function ParticleEmitter:setEmissionMax(value)
    self.emission[2] = value
    self.emitter:setEmission(unpack(self.emission))
end

function ParticleEmitter:setEmissionMin(value)
    self.emission[1] = value
    self.emitter:setEmission(unpack(self.emission))
end

function ParticleEmitter:setLeft(value)
    self.rect[1] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
    end
end

function ParticleEmitter:setMagnitudeMax(value)
    self.mag[2] = value
    self.emitter:setMagnitude(unpack(self.mag))
end

function ParticleEmitter:setMagnitudeMin(value)
    self.mag[1] = value
    self.emitter:setMagnitude(unpack(self.mag))
end

function ParticleEmitter:setName(name)
    self.name = name
end

function ParticleEmitter:setRight(value)
    self.rect[3] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
    end
end

function ParticleEmitter:setRadiusMax(value)
    self.radius[2] = value
    if self.shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
    end
end

function ParticleEmitter:setRadiusMin(value)
    self.radius[1] = value
    if self.shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
    end
end

function ParticleEmitter:setShape(shape)
    self.shape = shape

    if shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
    elseif shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
    end
end

function ParticleEmitter:setState(value)
    self.state = value
    self.emitter:setState(value + 1)
end

function ParticleEmitter:setTop(value)
    self.rect[4] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
    end
end


return ParticleEmitter
