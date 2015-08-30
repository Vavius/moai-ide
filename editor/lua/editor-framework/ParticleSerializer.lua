--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Serpent = require("util.Serpent")
local ParticleSerializer = class()


function ParticleSerializer:init()
    self.objectCache = {}

    self.objects = {}
    self.initializers = {}
end

function ParticleSerializer:add(object)
    if not object.__className then
        log.error("Cannot serialize object without class name")
        return
    end

    return self:affirmObjectId(object)
end

function ParticleSerializer:affirmObjectId(obj)
    if not self.objectCache[obj] then
        table.insert(self.objects, obj.__className)
        local id = #self.objects
        self.objectCache[obj] = id

        local init = {}
        obj:serializeOut(self, init)
        self.initializers[id] = init
    end
    return self.objectCache[obj]
end

function ParticleSerializer:getObjectById(id)
    return self.objectCache[id]
end

function ParticleSerializer:createObject(id, clazz)
    if self.objectCache[id] then return end
    self.objectCache[id] = clazz()
end

function ParticleSerializer:getObjectTable()
    return self.objects
end

function ParticleSerializer:getInitializerTable()
    return self.initializers
end


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- Class functions
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

function ParticleSerializer.save(file, ...)
    local serializer = ParticleSerializer()
    for _, v in pairs({...}) do
        serializer:add(v)
    end

    local res = {
        objects = serializer:getObjectTable(),
        init = serializer:getInitializerTable()
    }

    MOAIFileSystem.saveFile(file, Serpent.block(res))
end

function ParticleSerializer.load(file, classes)
    local success, input = Serpent.load ( MOAIFileSystem.loadFile(file) )
    local output = {}

    local serializer = ParticleSerializer()
    for id, name in pairs(input.objects) do
        local clazz = classes and classes[name] or require(name)
        serializer:createObject(id, clazz)
    end

    for id, t in pairs(input.init) do
        local obj = serializer:getObjectById(id)
        obj:serializeIn(serializer, t)
        table.insert(output, obj)
    end

    return unpack(output)
end


return ParticleSerializer
