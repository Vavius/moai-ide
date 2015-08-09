--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Gizmos = require("Gizmos")
local ParticleEmitter = class()

local SHAPE_RECT = 0
local SHAPE_CIRCLE = 1

-- some big number
local STATE_NONE = 0x0fffffff

local COMMON = {
    { type = "string",  name = "Name", value = "emitter", access = "Name" },
    { type = "float",   name = "Position X", value = 0, access = "LocX" },
    { type = "float",   name = "Position Y", value = 0, access = "LocY" },
    { type = "float",   name = "Rotation",   value = 0, access = "Rot" },
    { type = "int",     name = "Emission min", value = 1, access = "EmissionMin", range = {min = 0, max = 10000}},
    { type = "int",     name = "Emission max", value = 1, access = "EmissionMax", range = {min = 0, max = 10000}},
    { type = "list",    name = "State", value = 0, access = "State", choices = {} },
    -- { type = "list",    name = "Type",      value = 0, choices = {'Timed', 'Distance'}, access = "Type" },
    { type = "float",   name = "Frequency min", value = 1, access = "FrequencyMin", range = {min = 0}},
    { type = "float",   name = "Frequency max", value = 1, access = "FrequencyMax", range = {min = 0}},
    { type = "float",   name = "Angle min", value = 0, access = "AngleMin" },
    { type = "float",   name = "Angle max", value = 0, access = "AngleMax" },
    { type = "float",   name = "Velocity min", value = 0, access = "MagnitudeMin" },
    { type = "float",   name = "Velocity max", value = 0, access = "MagnitudeMax" },
    { type = "list",    name = "Shape", value = SHAPE_RECT, choices = {'Rect', 'Circle'}, access = "Shape" },
}

local CIRCLE = {
    { type = "float",   name = "Radius min", value = 10, access = "RadiusMin", range = {min = 0} },
    { type = "float",   name = "Radius max", value = 10, access = "RadiusMax", range = {min = 0} },
}

local RECT = {
    { type = "float",   name = "Left",      value = -10, access = "Left" },
    { type = "float",   name = "Bottom",    value = -10, access = "Bottom" },
    { type = "float",   name = "Right",     value = 10,  access = "Right" },
    { type = "float",   name = "Top",       value = 10,  access = "Top" },
}

local counter = 1

function ParticleEmitter:getModelData()
    local data = {}
    for _, p in ipairs(COMMON) do
        local getter = self['get' .. p.access]
        local value = getter(self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
            range = p.range
        }

        if p.access == 'State' then
            item.choices = require('ParticleEditor').listStates()
            table.insert(item.choices, 1, 'None')
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
        local value = getter(self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
            range = p.range,
        }

        table.insert(data, item)
    end
    
    return {{ group = 'Emitter', items = data }}
end


function ParticleEmitter:getParam(paramId)
    local getter = self['get' .. paramId]
    if not getter then
        log.error("No getter for " .. paramId)
        return
    end

    return getter(self)
end


function ParticleEmitter:init(system)
    local emitter = MOAIParticleTimedEmitter.new()
    emitter:setSystem(system)
    emitter:start()
    self.emitter = emitter

    self.angle = {0, 0}
    self.loc = {0, 0}
    self.emission = {0, 0}
    self.freq = {0, 0}
    self.mag = {0, 0}
    self.radius = {0, 0}
    self.rect = {0, 0, 0, 0}

    self:initGizmos()

    for _, default in ipairs(COMMON) do
        local setter = 'set' .. default.access
        self[setter](self, default.value)
    end

    for _, default in ipairs(RECT) do
        local setter = 'set' .. default.access
        self[setter](self, default.value)
    end

    self:setName("Emitter" .. counter)
    counter = counter + 1

    self:hideGizmos()
end

function ParticleEmitter:initGizmos()
    local editor = require("ParticleEditor")
    local gizmoCircleMin = Gizmos.Circle()
    local gizmoCircleMax = Gizmos.Circle()
    local gizmoRect = Gizmos.Rect()

    gizmoCircleMin.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.emitter, MOAITransform.TRANSFORM_TRAIT)
    gizmoCircleMax.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.emitter, MOAITransform.TRANSFORM_TRAIT)
    gizmoRect.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.emitter, MOAITransform.TRANSFORM_TRAIT)

    gizmoCircleMin:setColor(1, 0, 1, 1)
    gizmoCircleMin:setWidth(2)
    gizmoCircleMax:setColor(0, 1, 1, 1)
    gizmoCircleMax:setWidth(2)
    
    gizmoRect:setColor(1, 1, 0, 1)
    gizmoRect:setWidth(2)

    self.gizmoCircleMin = gizmoCircleMin
    self.gizmoCircleMax = gizmoCircleMax
    self.gizmoRect = gizmoRect

    editor.addGizmo(gizmoCircleMin)
    editor.addGizmo(gizmoCircleMax)
    editor.addGizmo(gizmoRect)
end

function ParticleEmitter:destroy()
    self.emitter:stop()

    self.gizmoCircleMin.prop:setLayer()
    self.gizmoCircleMax.prop:setLayer()
    self.gizmoRect.prop:setLayer()
end


function ParticleEmitter:hideGizmos()
    self.gizmoCircleMin.prop:setVisible(false)
    self.gizmoCircleMax.prop:setVisible(false)
    self.gizmoRect.prop:setVisible(false)
end

function ParticleEmitter:showGizmos()
    self:hideGizmos()

    if self.shape == SHAPE_RECT then
        self.gizmoRect.prop:setVisible(true)
        self.gizmoRect:setVerts(unpack(self.rect))
    else
        self.gizmoCircleMin.prop:setVisible(true)
        self.gizmoCircleMax.prop:setVisible(true)
        
        self.gizmoCircleMin:setRadius(self.radius[1])
        self.gizmoCircleMax:setRadius(self.radius[2])
    end
end

function ParticleEmitter:setParam(paramId, value)
    local setter = self['set' .. paramId]
    if not setter then
        log.error("No setter for " .. paramId)
        return
    end

    return setter(self, value)
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

function ParticleEmitter:getFrequencyMax()
    return self.freq[2]
end

function ParticleEmitter:getFrequencyMin()
    return self.freq[1]
end

function ParticleEmitter:getLeft()
    return self.rect[1]
end

function ParticleEmitter:getLocX()
    return self.loc[1]
end

function ParticleEmitter:getLocY()
    return self.loc[2]
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

function ParticleEmitter:getRot()
    local _, _, r = self.emitter:getRot()
    return r
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
        self:showGizmos()
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

function ParticleEmitter:setFrequencyMax(value)
    self.freq[2] = value
    self.emitter:setFrequency(unpack(self.freq))
end

function ParticleEmitter:setFrequencyMin(value)
    self.freq[1] = value
    self.emitter:setFrequency(unpack(self.freq))
end

function ParticleEmitter:setLeft(value)
    self.rect[1] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
        self:showGizmos()
    end
end

function ParticleEmitter:setLocX(value)
    self.loc[1] = value
    self.emitter:setLoc(unpack(self.loc))
    self:showGizmos()
end

function ParticleEmitter:setLocY(value)
    self.loc[2] = value
    self.emitter:setLoc(unpack(self.loc))
    self:showGizmos()
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

function ParticleEmitter:setRadiusMax(value)
    self.radius[2] = value
    if self.shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
        self:showGizmos()
    end
end

function ParticleEmitter:setRadiusMin(value)
    self.radius[1] = value
    if self.shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
        self:showGizmos()
    end
end

function ParticleEmitter:setRight(value)
    self.rect[3] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
        self:showGizmos()
    end
end

function ParticleEmitter:setRot(value)
    self.emitter:setRot(0, 0, value)
    self:showGizmos()
end

function ParticleEmitter:setShape(shape)
    self.shape = shape

    if shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))        
    elseif shape == SHAPE_CIRCLE then
        self.emitter:setRadius(unpack(self.radius))
    end

    -- request params view reload
    return true
end

function ParticleEmitter:setState(value)
    self.state = value
    if value == 0 then
        self.emitter:setState(STATE_NONE)
    else
        self.emitter:setState(value)
    end
end

function ParticleEmitter:setTop(value)
    self.rect[4] = value
    if self.shape == SHAPE_RECT then
        self.emitter:setRect(unpack(self.rect))
        self:showGizmos()
    end
end


return ParticleEmitter
