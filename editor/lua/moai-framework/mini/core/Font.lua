--------------------------------------------------------------------------------
-- Font.lua
-- 
-- 
--------------------------------------------------------------------------------

local SDFParams = require("util.SDFParams")

local Font = class()
Font.__index = MOAIFont.getInterfaceTable()
Font.__moai_class = MOAIFont


Font.DEFAULT_FILTER = MOAITexture.GL_LINEAR
-- Font.DEFAULT_PADDING = 12
-- Font.DEFAULT_THRESHOLD = 0.16


---
-- The constructor.
-- @param path      path to font file. ttf or fnt
-- @param filter    texture filter
-- @param sdf       boolean, whether to use sdf for rendering ttf files
-- @param padding   sdf padding
-- @param threshold for sdf generation
function Font:init(path, filter, sdf, padding, threshold)
    path = ResourceMgr:getResourceFilePath(path)
    self:setFilter(filter or Font.DEFAULT_FILTER)

    if string.endswith(path, ".fnt") then
        self:loadFromBMFont(path)
        font.bmFont = true
    else
        self:load(path)
    end
    self.path = path

    if sdf then
        self:setListener(MOAIFont.EVENT_RENDER_GLYPH, self.onGlyph)
        self.padding = padding or SDFParams.padding()
        self.threshold = threshold or SDFParams.threshold()
        self.usesSDF = true
        local cache = self:getCache()
        cache:setPadding(self.padding)
    end
end


function Font:onGlyph(reader, image, code, x, y, xMin, yMin, xMax, yMax)
    local pad = 0.5 * self.padding
    reader:renderGlyph(image, x, y)
    image:generateSDFAA(xMin - pad, yMin - pad, xMax + pad, yMax + pad, self.threshold)
    self.cacheWidth, self.cacheHeight = image:getSize()
end


return Font