--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local ParticleForce = require("ParticleForce")
local ParticleComponent = require("ParticleComponent")
local ParticleHelper = require("util.ParticleHelper")

local ParticleState = class()

local DATA = {
    { type = "string", name = "Name", value = "state", access = "Name" },
    { type = "float", name = "Damping", value = 0, access = "Damping", range = {min = 0} },
    { type = "float", name = "Mass min", value = 1, access = "MassMin", range = {min = 0} },
    { type = "float", name = "Mass max", value = 1, access = "MassMax", range = {min = 0} },
    { type = "float", name = "Lifetime min", value = 1, access = "TermMin", range = {min = 0} },
    { type = "float", name = "Lifetime max", value = 1, access = "TermMax", range = {min = 0} },
    { type = "list",  name = "Next", value = 0, access = "Next", choices = {} },
}

local counter = 1

function ParticleState:addComponent(kind)
    if kind == 'Force' then
        self:addForce()
        return
    end

    local clazz = ParticleComponent[kind]
    if not clazz then
        log.error("Particle component not found " .. kind)
        return
    end

    local comp = clazz()
    table.insert(self.components, comp)
    self:syncComponents()
end

function ParticleState:addForce()
    local force = ParticleForce()
    table.insert(self.forces, force)
    self:syncForces()
end

function ParticleState:assignUniqueIds(data, prefix)
    local items = data.items
    if not items then return data end

    for i, info in pairs(items) do
        info.id = prefix .. "$" .. info.id
    end
    return data
end

function ParticleState:getModelData()
    local stateParams = {}
    for _, p in ipairs(DATA) do
        local getter = 'get' .. p.access
        local value = self[getter](self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
            range = p.range,
        }

        if p.access == "Next" then
            item.choices = require('ParticleEditor').listStates()
            table.insert(item.choices, 1, "None")
        end

        table.insert(stateParams, item)
    end

    local data = {
        { group = self:getName(), items = stateParams }
    }

    if #self.forces > 0 then
        for i, f in ipairs(self.forces) do
            local grp = self:assignUniqueIds(f:getGroupData(), 'force' .. i)
            table.insert(data, grp)
        end
    end

    if #self.components > 0 then
        for i, c in ipairs(self.components) do
            local grp = self:assignUniqueIds(c:getGroupData(), 'comp' .. i)
            table.insert(data, grp)
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

    return getter(self)
end

function ParticleState:getRegisterCount()
    local regCount = 0
    for _, comp in pairs(self.components) do
        regCount = regCount + comp:getRegisterCount()
    end
    return regCount
end

function ParticleState:init()
    self.state = MOAIParticleState.new()
    self.forces = {}
    self.components = {}
    self.mass = {0, 0}
    self.term = {0, 0}

    for _, default in ipairs(DATA) do
        local setter = 'set' .. default.access
        self[setter](self, default.value)
    end

    self:setName("State" .. counter)
    counter = counter + 1
end


function ParticleState:destroy()
    for _, f in pairs(self.forces) do
        f:destroy()
    end
end

function ParticleState:hideGizmos()
    for _, force in pairs(self.forces) do
        force:hideGizmos()
    end
end


function ParticleState:removeForce(idx)
    table.remove()
    self:syncForces()
end

function ParticleState:setForceParam(paramId, value)
    local idx, param = string.match(paramId, "force(%d+)%$(.*)")
    if idx and param then
        local force = self.forces[tonumber(idx)]
        if force then
            return force:setParam(param, value)
        end
    end
end

function ParticleState:setComponentParam(paramId, value)
    local idx, param = string.match(paramId, "comp(%d+)%$(.*)")
    if idx and param then
        local comp = self.components[tonumber(idx)]
        if comp then
            local res = comp:setParam(param, value)
            self:syncComponents()
            return res
        end
    end
end

function ParticleState:setParam(paramId, value)
    if string.sub(paramId, 1, #'force') == 'force' then
        return self:setForceParam(paramId, value)
    end
    if string.sub(paramId, 1, #'comp') == 'comp' then
        return self:setComponentParam(paramId, value)
    end

    local setter = self['set' .. paramId]
    if not setter then
        log.error("No setter for " .. paramId)
        return
    end

    return setter(self, value)
end


function ParticleState:syncComponents()
    log.info("SYNC")
    local init = {}
    local sim = {}
    local sprite = {}
    for _, comp in pairs(self.components) do
        table.insert(init, comp:getInitScript() or nil)
        table.insert(sim, comp:getSimScript() or nil)
        table.insert(sprite, comp:getSpriteScript() or nil)
    end

    local initStr = table.concat(init, '\n')
    local renderStr = table.concat(sim, '\n') .. '\nsprite()\n' .. table.concat(sprite, '\n')

    local initFunc = loadstring(initStr)
    local renderFunc = loadstring(renderStr)

    log.debug("Compiling init script:\n" .. initStr)
    log.debug("Compiling render script:\n" .. renderStr)

    local initScript = ParticleHelper.makeParticleScript(initFunc, reg)
    local renderScript = ParticleHelper.makeParticleScript(renderFunc, reg)

    self.state:setInitScript(initScript)
    self.state:setRenderScript(renderScript)
    
    require('ParticleEditor').updateRegCount()
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
    self.state:setNext(st and st.state)
end

function ParticleState:setTermMax(term)
    self.term[2] = term
    self.state:setTerm(unpack(self.term))
end

function ParticleState:setTermMin(term)
    self.term[1] = term
    self.state:setTerm(unpack(self.term))
end



return ParticleState
