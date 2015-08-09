--------------------------------------------------------------------------------
-- 
-- 
-- 
--------------------------------------------------------------------------------

local ParticleComponent = class()

--============================================================================--
-- Base class
--============================================================================--

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:copyFrom(component)
    for _, data in ipairs(self.data) do
        self:setParam(data.access, component:getParam(data.access))
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:destroy()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getParam(id)
    return self.storage[id]
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getInitScript()
    -- virtual
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getGroupData()
    local data = {}
    for _, p in ipairs(self.data) do
        local value = self:getParam(p.access)

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

    return { group = self:getParam('Name') or 'Noname', items = data }
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getRegisterCount()
    -- virtual
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getSimScript()
    -- virtual
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:getSpriteScript()
    -- virtual
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:init(attributes)
    self.data = attributes
    self.storage = {}
    
    for _, def in pairs(self.data) do
        self:setParam(def.access, def.value)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ParticleComponent:setParam(id, value)
    self.storage[id] = value
end

--============================================================================--
-- Presets
--============================================================================--

--------------------------------------------------------------------------------
local Sprite = class(ParticleComponent)

local SPRITE = {
    { type = "string",  name = "Name", value = "sprite", access = "Name" },
    { type = "int",     name = "Index", value = 1, access = "Index", range = {min = 0} },
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Sprite:init()
    ParticleComponent.init(self, SPRITE)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Sprite:getRegisterCount()
    return 0
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Sprite:getSpriteScript()
    local idx = self:getParam("Index") or 0
    idx = math.floor(math.max(0, idx))
    
    return "sp.idx = " .. tostring(idx)
end

--------------------------------------------------------------------------------
local SpriteAnim = class(ParticleComponent)

local SPRITE_ANIM = {
    { type = "string",  name = "Name", value = "sprite animation", access = "Name" },
    { type = "int",     name = "Index Min", value = 1, access = "IndexMin", range = {min = 0} },
    { type = "int",     name = "Index Max", value = 1, access = "IndexMax", range = {min = 0} },
    { type = "float",   name = "Delay (lifetime %)", value = 10, access = "Delay", range = {min = 0} },
    { type = "list",    name = "Animation type", value = 0, access = "Anim", choices = {"Random", "Sequential", "Ping pong"}},
}

local lessOne = 1 - 1e-5

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function SpriteAnim:init()
    ParticleComponent.init(self, SPRITE_ANIM)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function SpriteAnim:getRegisterCount()
    return 1
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function SpriteAnim:getInitScript()
    if self:getParam("Anim") == 0 then
        -- random
        local lo = self:getParam("IndexMin")
        local hi = self:getParam("IndexMax")
        lo = math.floor(math.max(0, lo))

        -- Add 'slightly less than 1' value to hi.
        -- hi index is included in distribution while (hi + 1) is not
        hi = math.floor(math.max(0, hi)) + lessOne
        return string.format("index = %d + rand(0, %f)", lo, hi - lo)

    else
        -- sequential & ping pong
        local delay = 0.01 * self:getParam("Delay")
        local multiplier = 1.0 / delay
        return "mult = " .. tostring(multiplier)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function SpriteAnim:getSimScript()
    if self:getParam("Anim") == 0 then return end

    local lo = self:getParam("IndexMin")
    local hi = self:getParam("IndexMax")
    lo = math.floor(math.max(0, lo))
    hi = math.floor(math.max(0, hi)) + lessOne

    -- index is temporary reg here

    if self:getParam("Anim") == 1 then 
        return string.format("index = %d + wrap(mult * time, 0, %f)", lo, hi - lo)
    end

    if self:getParam("Anim") == 2 then 
        return string.format("index = %d + cycle(mult * time, 0.5, %f)", lo, hi - lo - 0.5)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function SpriteAnim:getSpriteScript()
    return "sp.idx = index"
end

--------------------------------------------------------------------------------
local Color = class(ParticleComponent)

local COLOR = {
    { type = "string",  name = "Name", value = "color", access = "Name" },
    { type = "float",   name = "Red",  value = 1.0,     access = "Red" },
    { type = "float",   name = "Green",  value = 1.0,   access = "Green" },
    { type = "float",   name = "Blue",  value = 1.0,    access = "Blue" },
    { type = "float",   name = "Alpha",  value = 1.0,   access = "Alpha" },
    { type = "float",   name = "Glow",  value = 0.0,    access = "Glow" },
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Color:init()
    ParticleComponent.init(self, COLOR)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Color:getRegisterCount()
    return 0
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Color:getSpriteScript()
    local res = {}
    local r = self:getParam("Red")
    local g = self:getParam("Green")
    local b = self:getParam("Blue")
    local a = self:getParam("Alpha")
    local glow = self:getParam("Glow")
    if r ~= 1.0 then
        table.insert(res, "sp.r = " .. tostring(r))
    end
    if g ~= 1.0 then
        table.insert(res, "sp.g = " .. tostring(g))
    end
    if b ~= 1.0 then
        table.insert(res, "sp.b = " .. tostring(b))
    end
    if a ~= 1.0 then
        table.insert(res, "sp.opacity = " .. tostring(a))
    end
    if glow ~= 0.0 then
        table.insert(res, "sp.glow = " .. tostring(glow))
    end
    return table.concat(res, '\n')
end

--------------------------------------------------------------------------------
local ColorAnim = class(ParticleComponent)

local ANIM_TYPES = {
    "None",
    "random",
    "ease in",
    "ease out",
    "sharp in",
    "sharp out",
    "soft in",
    "soft out",
    "linear",
    "soft in + sharp out",
    "sharp in + soft out",
    "soft in + soft out",
    "sharp in + sharp out",
}

local ANIM_TMPL = {
    ['ease in'] = "ease(%[min], %[max], EaseType.EASE_IN)",
    ['ease out'] = "ease(%[min], %[max], EaseType.EASE_OUT)",
    ['sharp in'] = "ease(%[min], %[max], EaseType.SHARP_EASE_IN)",
    ['sharp out'] = "ease(%[min], %[max], EaseType.SHARP_EASE_OUT)",
    ['soft in'] = "ease(%[min], %[max], EaseType.SOFT_EASE_IN)",
    ['soft out'] = "ease(%[min], %[max], EaseType.SOFT_EASE_OUT)",
    
    ['linear'] = "ease(%[min], %[max], EaseType.LINEAR)",
    ['soft in + sharp out'] = "ease(%[min], ease(%[max], %[min], EaseType.SHARP_EASE_OUT), EaseType.SOFT_EASE_IN)",
    ['sharp in + soft out'] = "ease(%[min], ease(%[max], %[min], EaseType.SOFT_EASE_OUT), EaseType.SHARP_EASE_IN)",
    ['soft in + soft out'] = "ease(%[min], ease(%[max], %[min], EaseType.SOFT_EASE_OUT), EaseType.SOFT_EASE_IN)",
    ['sharp in + sharp out'] = "ease(%[min], ease(%[max], %[min], EaseType.EXTRA_SHARP_EASE_OUT), EaseType.EXTRA_SHARP_EASE_IN)",
}

local COLOR_ANIM = {
    { type = "string",  name = "Name", value = "Color animation", access = "Name" },
    { type = "float",   name = "Red Min",  value = 1.0,     access = "RedMin" },
    { type = "float",   name = "Red Max",  value = 1.0,     access = "RedMax" },
    { type = "list",    name = "Red anim", value = 0,       access = "RedAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Green Min",  value = 1.0,   access = "GreenMin" },
    { type = "float",   name = "Green Max",  value = 1.0,   access = "GreenMax" },
    { type = "list",    name = "Green anim", value = 0,     access = "GreenAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Blue Min",  value = 1.0,    access = "BlueMin" },
    { type = "float",   name = "Blue Max",  value = 1.0,    access = "BlueMax" },
    { type = "list",    name = "Blue anim", value = 0,      access = "BlueAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Alpha Min",  value = 1.0,   access = "AlphaMin" },
    { type = "float",   name = "Alpha Max",  value = 1.0,   access = "AlphaMax" },
    { type = "list",    name = "Alpha anim", value = 0,     access = "AlphaAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Glow Min",  value = 0.0,    access = "GlowMin" },
    { type = "float",   name = "Glow Max",  value = 0.0,    access = "GlowMax" },
    { type = "list",    name = "Glow anim", value = 0,      access = "GlowAnim", choices = ANIM_TYPES },
}

local COLOR_REGS = {
    red = 'r', green = 'g', blue = 'b', alpha = 'opacity', glow = 'glow'
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:init()
    ParticleComponent.init(self, COLOR_ANIM)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:getRegisterCount()
    local c = 0
    for _, t in pairs{'RedAnim', 'GreenAnim', 'BlueAnim', 'AlphaAnim', 'GlowAnim'} do
        -- random initial state
        if self:getParam(t) == 1 then
            c = c + 1
        end
    end
    return c
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:getInitScript()
    local result = {}
    for _, t in pairs{'Red', 'Green', 'Blue', 'Alpha', 'Glow'} do
        if self:getParam(t .. 'Anim') == 1 then
            local reg = string.lower(t)
            local lo = self:getParam(t .. 'Min')
            local hi = self:getParam(t .. 'Max')
            table.insert(result, string.format("%s = rand(%s, %s)", reg, tostring(lo), tostring(hi)))
        end
    end
    return table.concat(result, '\n')
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:getSimScript()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:getSpriteScript()
    local result = {}
    for _, t in pairs{'Red', 'Green', 'Blue', 'Alpha', 'Glow'} do
        if self:getParam(t .. 'Anim') > 0 then
            table.insert(result, self:getAnimExpr(t))
        end
    end
    return table.concat(result, '\n')
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ColorAnim:getAnimExpr(param)
    local anim = self:getParam(param .. 'Anim')
    if anim == 0 then return '' end

    local lo = self:getParam(param .. 'Min')
    local hi = self:getParam(param .. 'Max')
    local reg = string.lower(param)
    local spreg = COLOR_REGS[reg]

    if anim == 1 then
        return string.format("sp.%s = %s", spreg, reg)
    end
    local tmpl = ANIM_TMPL[ANIM_TYPES[anim + 1]]
    if tmpl then
        local ease = tmpl % {min = lo, max = hi}
        return string.format("sp.%s = %s", spreg, ease)
    end
    return ''
end

--------------------------------------------------------------------------------
local Transform = class(ParticleComponent)

local TRANSFORM = {
    { type = "string",  name = "Name", value = "Transform", access = "Name" },
    { type = "float",   name = "X",  value = 0.0,       access = "LocX" },
    { type = "float",   name = "Y",  value = 0.0,       access = "LocY" },
    { type = "float",   name = "Rotation",  value = 0.0,  access = "Rot" },
    { type = "float",   name = "Scale X",  value = 1.0,   access = "SclX" },
    { type = "float",   name = "Scale Y",  value = 1.0,   access = "SclY" },
}

local XFORM_EXPR = {
    locx = 'sp.x = p.x + %s', 
    locy = 'sp.y = p.y + %s', 
    rot  = 'sp.rot = %s', 
    sclx = 'sp.sx = %s', 
    scly = 'sp.sy = %s'
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Transform:init()
    ParticleComponent.init(self, TRANSFORM)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Transform:getRegisterCount()
    return 0
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Transform:getSpriteScript()
    local result = {}
    for _, t in pairs{'LocX', 'LocY', 'Rot', 'SclX', 'SclY'} do
        local default = table.detect(TRANSFORM, function(x) return x.access == t end)
        local val = self:getParam(t)
        if val ~= default.value then
            local reg = string.lower(t)
            table.insert(result, string.format(XFORM_EXPR[reg], val))
        end
    end
    return table.concat(result, '\n')
end

--------------------------------------------------------------------------------
local TransformAnim = class(ParticleComponent)

local TRANSFORM_ANIM = {
    { type = "string",  name = "Name", value = "Transform animation", access = "Name" },

    { type = "float",   name = "X Min",  value = 0.0,       access = "LocXMin" },
    { type = "float",   name = "X Max",  value = 0.0,       access = "LocXMax" },
    { type = "list",    name = "X anim", value = 0,         access = "LocXAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Y Min",  value = 0.0,       access = "LocYMin" },
    { type = "float",   name = "Y Max",  value = 0.0,       access = "LocYMax" },
    { type = "list",    name = "Y anim", value = 0,         access = "LocYAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Rot Min",  value = 0.0,     access = "RotMin" },
    { type = "float",   name = "Rot Max",  value = 0.0,     access = "RotMax" },
    { type = "list",    name = "Rot anim", value = 0,       access = "RotAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Scale X Min",  value = 1.0,   access = "SclXMin" },
    { type = "float",   name = "Scale X Max",  value = 1.0,   access = "SclXMax" },
    { type = "list",    name = "Scale X anim", value = 0,     access = "SclXAnim", choices = ANIM_TYPES },

    { type = "float",   name = "Scale Y Min",  value = 1.0,   access = "SclYMin" },
    { type = "float",   name = "Scale Y Max",  value = 1.0,   access = "SclYMax" },
    { type = "list",    name = "Scale Y anim", value = 0,     access = "SclYAnim", choices = ANIM_TYPES },
}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:init()
    ParticleComponent.init(self, TRANSFORM_ANIM)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:getRegisterCount()
    local c = 0
    for _, t in pairs{'LocXAnim', 'LocYAnim', 'RotAnim', 'SclXAnim', 'SclYAnim'} do
        -- random initial state
        if self:getParam(t) == 1 then
            c = c + 1
        end
    end
    return c
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:getInitScript()
    local result = {}
    for _, t in pairs{'LocX', 'LocY', 'Rot', 'SclX', 'SclY'} do
        if self:getParam(t .. 'Anim') == 1 then
            local reg = string.lower(t)
            local lo = self:getParam(t .. 'Min')
            local hi = self:getParam(t .. 'Max')
            table.insert(result, string.format("%s = rand(%s, %s)", reg, tostring(lo), tostring(hi)))
        end
    end
    return table.concat(result, '\n')
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:getSimScript()

end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:getSpriteScript()
    local result = {}
    for _, t in pairs{'LocX', 'LocY', 'Rot', 'SclX', 'SclY'} do
        if self:getParam(t .. 'Anim') > 0 then
            table.insert(result, self:getAnimExpr(t))
        end
    end
    return table.concat(result, '\n')
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function TransformAnim:getAnimExpr(param)
    local anim = self:getParam(param .. 'Anim')
    if anim == 0 then return '' end

    local lo = self:getParam(param .. 'Min')
    local hi = self:getParam(param .. 'Max')
    local reg = string.lower(param)

    if anim == 1 then
        return string.format(XFORM_EXPR[reg], reg)
    end
    local tmpl = ANIM_TMPL[ANIM_TYPES[anim + 1]]
    if tmpl then
        local ease = tmpl % {min = lo, max = hi}
        return string.format(XFORM_EXPR[reg], ease)
    end
    return ''
end



return {
    -- ParticleComponent = ParticleComponent,
    Sprite = Sprite,
    SpriteAnim = SpriteAnim,
    Color = Color,
    ColorAnim = ColorAnim,
    Transform = Transform,
    TransformAnim = TransformAnim
}

