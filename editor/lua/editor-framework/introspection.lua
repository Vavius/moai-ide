--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------


CLASS = {}
setmetatable(CLASS, CLASS)

---
-- Create a new type definition
-- @params table 
--      available parameters: 
--          inherit = {base1, base2}
--          parameters = {'loc', 'color', 'scl', 'rot'}
--          name = 'button'
--          constructor = function() local str = "MOAIProp.new()" return str end
function CLASS:__call(params)
    local clazz = table.dup(self)
    local bases = {...}
    for i = #bases, 1, -1 do
        table.merge(clazz, bases[i])
    end
    clazz.__super = bases[1]
    clazz.__call = function(self, ...)
        return self:__new(...)
    end
    return setmetatable(clazz, clazz)
end


---
-- Returns the new object.
-- @return object
function class:__object_factory()
    local moai_class = self.__moai_class

    if moai_class then
        local obj = moai_class.new()
        obj.__class = self
        obj:setInterface(self)
        return obj
    end

    local obj = {__index = self, __class = self}
    return setmetatable(obj, obj)
end
