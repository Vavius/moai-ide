--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local ParticleForce = require("ParticleForce")

local ParticleState = class()

local DATA = {
    { type = "string", name = "Name", value = "state", access = "Name" },
    { type = "float", name = "Damping", value = 0, access = "Damping" },
    { type = "float", name = "Mass min", value = 1, access = "MassMin" },
    { type = "float", name = "Mass max", value = 1, access = "MassMax" },
    { type = "float", name = "Lifetime min", value = 1, access = "TermMin" },
    { type = "float", name = "Lifetime max", value = 1, access = "TermMax" },
}


function ParticleState:addForce()
    local force = ParticleForce()
    table.insert(self.forces, force)
    self:syncForces()
end


function ParticleState:getModelData()
    local stateParams = {}
    for _, p in ipairs(DATA) do
        local getter = 'get' .. p.access
        local value = self[getter]()

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
        }
        table.insert(stateParams, item)
    end

    local data = {
        { group = 'State', items = stateParams }
    }

    if #self.forces > 0 then
        for i, f in ipairs(self.forces) do
            table.insert(data, { group = 'Force'..i, items = f:getData() })
        end
    end

    return data
end


function ParticleState:getParam(paramId)
    local getter = self['get' .. paramId]
    if not getter then
        log.error("No getter for " .. paramId)
        return
    end

    return getter()
end


function ParticleState:init()
    self.state = MOAIParticleState.new()
    self.forces = {}
    self.mass = {0, 0}
    self.term = {0, 0}

    for _, default in ipairs(DATA) do
        local setter = 'set' .. default.access
        self[setter](default.value)
    end
end


function ParticleState:removeForce(idx)
    table.remove()
    self:syncForces()
end


function ParticleState:setParam(paramId, value)
    local setter = self['set' .. paramId]
    if not setter then
        log.error("No setter for " .. paramId)
        return
    end

    setter(value)
end


function ParticleState:syncForces()
    self.state:clearForces()
    for _, f in ipairs(self.forces) do
        self.state:pushForce(f.force)
    end
end


--============================================================================--
-- Attribute accessors
--============================================================================--

function ParticleState:getDamping()
    return self.damping
end

function ParticleState:getMassMax()
    return self.mass[2]
end

function ParticleState:getMassMin()
    return self.mass[1]
end

function ParticleState:getName()
    return self.name
end

function ParticleState:getNext()
    if self.next then
        return require('ParticleEditor').getStateIdx(self.next)
    end
    return 0
end

function ParticleState:getTermMax()
    return self.term[2]
end

function ParticleState:getTermMin()
    return self.term[1]
end

function ParticleState:setDamping(damp)
    self.damping = damp
    self.state:setDamping(damp)
end

function ParticleState:setMassMax(mass)
    self.mass[2] = mass
    self.state:setMass(unpack(self.mass))
end

function ParticleState:setMassMin(mass)
    self.mass[1] = mass
    self.state:setMass(unpack(self.mass))
end

function ParticleState:setName(n)
    self.name = n
end

function ParticleState:setNext(idx)
    local st = require('ParticleEditor').findState(idx)
    self.next = st
    self.state:setNext(st.state)
end

function ParticleState:setTermMax(term)
    self.term[2] = term
    self.state:setMass(unpack(self.term))
end

function ParticleState:setTermMin(term)
    self.term[1] = term
    self.state:setMass(unpack(self.term))
end



return ParticleState
