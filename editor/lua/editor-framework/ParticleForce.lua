--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Gizmos = require("Gizmos")
local ParticleForce = class()

local T_FORCE = 0
local T_GRAVITY = 1
local T_OFFSET = 2

local A_ATTRACTOR = 0
local A_BASIN = 1
local A_LINEAR = 2
local A_RADIAL = 3

local DATA = {
    { type = "string",  name = "Name", value = "Force", access = "Name" },
    { type = "list",    name = "Type", value = T_FORCE, access = "Type", choices = {'Force', 'Gravity', 'Offset'} },
    { type = "list",    name = "Shape", value = A_ATTRACTOR, access = "Shape", choices = {'Attractor', 'Basin', 'Linear', 'Radial'} },
}

local SHAPE_DATA = {
    [A_ATTRACTOR] = {
        { type = "float",   name = "Loc X", value = 0, access = "LocX" },
        { type = "float",   name = "Loc Y", value = 0, access = "LocY" },
        { type = "float",   name = "Radius", value = 0, access = "Radius", range = {min = 0.01} },
        { type = "float",   name = "Magnitude", value = 0, access = "Magnitude" },
    },

    [A_BASIN] = {
        { type = "float",   name = "Loc X", value = 0, access = "LocX" },
        { type = "float",   name = "Loc Y", value = 0, access = "LocY" },
        { type = "float",   name = "Radius", value = 0, access = "Radius", range = {min = 0.01} },
        { type = "float",   name = "Magnitude", value = 0, access = "Magnitude" },
    },

    [A_LINEAR] = {
        { type = "float",   name = "Mag X", value = 0, access = "MagX" },
        { type = "float",   name = "Mag Y", value = 0, access = "MagY" },
    },

    [A_RADIAL] = {
        { type = "float",   name = "Loc X", value = 0, access = "LocX" },
        { type = "float",   name = "Loc Y", value = 0, access = "LocY" },
        { type = "float",   name = "Magnitude", value = 0, access = "Magnitude" },
    },
}

local TYPES = {
    [T_FORCE] = MOAIParticleForce.FORCE,
    [T_GRAVITY] = MOAIParticleForce.GRAVITY,
    [T_OFFSET] = MOAIParticleForce.OFFSET,
}


function ParticleForce:destroy()
    self.gizmoField:setLayer()
    self.gizmoLoc:setLayer()
    self.gizmoCircle:setLayer()
end

function ParticleForce:getGroupData()
    local data = {}
    for _, p in ipairs(DATA) do
        local getter = 'get' .. p.access
        local value = self[getter](self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
            choices = p.choices,
            range = p.range,
        }
        table.insert(data, item)
    end

    local shape = SHAPE_DATA[self:getShape()]
    for _, p in ipairs(shape) do
        local getter = self['get' .. p.access]
        local value = getter(self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
        }

        table.insert(data, item)
    end

    return { group = self:getName(), items = data }
end


function ParticleForce:getParam(paramId)
    local getter = self['get' .. paramId]
    if not getter then
        log.error("No getter for " .. paramId)
        return
    end

    return getter(self)
end

function ParticleForce:init()
    self.force = MOAIParticleForce.new()

    self.attractor = {0, 0}
    self.basin = {0, 0}
    self.linear = {0, 0}
    self.loc = {0, 0, 0}
    self.radial = 0

    self:initGizmos()

    for _, default in ipairs(DATA) do
        local setter = 'set' .. default.access
        self[setter](self, default.value)
    end

    self:hideGizmos()
end

function ParticleForce:initGizmos()
    local editor = require("ParticleEditor")
    local gizmoCircle = Gizmos.Circle()
    local gizmoField = Gizmos.VectorField()
    local gizmoLoc = Gizmos.Locator()

    gizmoCircle.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.force, MOAITransform.TRANSFORM_TRAIT)
    gizmoField.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.force, MOAITransform.TRANSFORM_TRAIT)
    gizmoLoc.prop:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.force, MOAITransform.TRANSFORM_TRAIT)

    gizmoCircle:setColor(1, 1, 0, 1)
    gizmoCircle:setWidth(2)

    gizmoField:setColor(1, 1, 0, 1)
    gizmoField:setWidth(2)
    
    gizmoLoc:setColor(0, 1, 0, 1)
    gizmoLoc:setWidth(2)

    self.gizmoCircle = gizmoCircle
    self.gizmoField = gizmoField
    self.gizmoLoc = gizmoLoc

    editor.addGizmo(gizmoCircle)
    editor.addGizmo(gizmoField)
    editor.addGizmo(gizmoLoc)
end

function ParticleForce:hideGizmos()
    self.gizmoCircle.prop:setVisible(false)
    self.gizmoField.prop:setVisible(false)
    self.gizmoLoc.prop:setVisible(false)
end

function ParticleForce:showGizmos()
    self:hideGizmos()

    if self.shape == A_ATTRACTOR then
        self.gizmoLoc.prop:setVisible(true)
        self.gizmoCircle.prop:setVisible(true)
        self.gizmoCircle:setRadius(self.attractor[1])

    elseif self.shape == A_BASIN then
        self.gizmoLoc.prop:setVisible(true)
        self.gizmoCircle.prop:setVisible(true)
        self.gizmoCircle:setRadius(self.basin[1])

    elseif self.shape == A_LINEAR then
        self.gizmoField.prop:setVisible(true)
        self.gizmoField:setSize(unpack(self.linear))

    elseif self.shape == A_RADIAL then
        self.gizmoLoc.prop:setVisible(true)

    end
end

function ParticleForce:setParam(paramId, value)
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

function ParticleForce:getLocX()
    return self.loc[1]
end

function ParticleForce:getLocY()
    return self.loc[2]
end

function ParticleForce:getMagnitude()
    if self.shape == A_ATTRACTOR then
        return self.attractor[2]
    elseif self.shape == A_BASIN then
        return self.basin[2]
    elseif self.shape == A_RADIAL then
        return self.radial
    end
    return 0
end

function ParticleForce:getMagX()
    return self.linear[1]    
end

function ParticleForce:getMagY()
    return self.linear[2]
end

function ParticleForce:getName()
    return self.name
end

function ParticleForce:getRadius()
    if self.shape == A_ATTRACTOR then
        return self.attractor[1]
    elseif self.shape == A_BASIN then
        return self.basin[1]
    end
    return 0
end

function ParticleForce:getShape()
    return self.shape
end

function ParticleForce:getType()
    return self.type
end


function ParticleForce:setLocX(value)
    self.loc[1] = value
    self.force:setLoc(unpack(self.loc))
    self:showGizmos()
end

function ParticleForce:setLocY(value)
    self.loc[2] = value
    self.force:setLoc(unpack(self.loc))
    self:showGizmos()
end

function ParticleForce:setMagnitude(value)
    if self.shape == A_ATTRACTOR then
        self.attractor[2] = value
        self.force:initAttractor(unpack(self.attractor))

    elseif self.shape == A_BASIN then
        self.basin[2] = value
        self.force:initBasin(unpack(self.basin))

    elseif self.shape == A_RADIAL then
        self.radial = value
        self.force:initRadial(self.radial)
    end
end

function ParticleForce:setMagX(value)
    self.linear[1] = value
    self.force:initLinear(unpack(self.linear))
    self:showGizmos()
end

function ParticleForce:setMagY(value)
    self.linear[2] = value
    self.force:initLinear(unpack(self.linear))
    self:showGizmos()
end

function ParticleForce:setName(value)
    self.name = value
end

function ParticleForce:setRadius(value)
    if self.shape == A_ATTRACTOR then
        self.attractor[1] = value
        self.force:initAttractor(unpack(self.attractor))

    elseif self.shape == A_BASIN then
        self.basin[1] = value
        self.force:initBasin(unpack(self.basin))
    end
    self:showGizmos()
end

function ParticleForce:setShape(value)
    self.shape = value

    if self.shape == A_ATTRACTOR then
        self.force:initAttractor(unpack(self.attractor))
    elseif self.shape == A_BASIN then
        self.force:initBasin(unpack(self.basin))
    elseif self.shape == A_RADIAL then
        self.force:initRadial(self.radial)
    elseif self.shape == A_LINEAR then
        self.force:initLinear(unpack(self.linear))
    end

    self:showGizmos()
    -- request view reload
    return true
end

function ParticleForce:setType(value)
    self.type = value
    self.force:setType(TYPES[value])
end



return ParticleForce
