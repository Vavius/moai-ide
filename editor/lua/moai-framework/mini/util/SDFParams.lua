--------------------------------------------------------------------------------
-- SDFParams.lua
-- 
-- Default SDF settings. Tuned by hand for optimal appearance on mobile devices
--------------------------------------------------------------------------------

local App = require("core.App")
local SDFParams = {}


local FONT_SIZE = 16



function SDFParams.padding()
    return 0.5 * FONT_SIZE * App:getContentScale()
end

function SDFParams.threshold()
    return 1 / SDFParams.padding()
end

function SDFParams.fontSize()
    return FONT_SIZE * App:getContentScale()
end

function SDFParams.outlineWidth(points, embolden)
    embolden = embolden or 0.5
    return embolden - 0.5 * points / 16
end

function SDFParams.smoothFactor()
    return 0.4 * SDFParams.threshold()
end


return SDFParams