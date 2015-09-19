--------------------------------------------------------------------------------
-- Resource cache
-- 
-- 
--------------------------------------------------------------------------------

local ResourceMgr = { }

local App = require("core.App")
local Font = require("core.Font")

local _createTexture
local _createFont
local _createSkeletonData
local _createStretchRowsOrColumns
local _getNineImageContentPadding
local _spineReadFile
local _spineCreateTexture
--------------------------------------------------------------------------------
-- Texture and Deck cache
--------------------------------------------------------------------------------

ResourceMgr.resourceDirectories = {}
ResourceMgr.filepathCache = {}
ResourceMgr.textureCache = setmetatable({}, {__mode = "v"})
ResourceMgr.skeletonCache = setmetatable({}, {__mode = "v"})
ResourceMgr.fontCache = {}
ResourceMgr.fontSDFCache = {}

ResourceMgr.imageDecks = setmetatable({}, {__mode = "v"})
ResourceMgr.atlasDecks = setmetatable({}, {__mode = "v"})
ResourceMgr.nineImageDecks = setmetatable({}, {__mode = "v"})

-- Internal lookup table to find atlas name for given sprite name
ResourceMgr.spriteFrameAtlases = {}

--- Default Texture filter
ResourceMgr.DEFAULT_TEXTURE_FILTER = MOAITexture.GL_LINEAR

-- Default spine json scale
ResourceMgr.SPINE_JSON_SCALE = 0.5


ResourceMgr.deckParams = {}

---
-- Constructor. 
-- @param path Texture path
-- @param filter Texture filter
function _createTexture(path, filter)
    local texture = MOAITexture.new()
    
    texture.filter = filter or ResourceMgr.DEFAULT_TEXTURE_FILTER
    texture:setFilter(texture.filter)
    
    texture:load(path)
    texture.path = path
    
    return texture
end

---
-- Constructor.
-- @param path Font path
function _createFont(path, sdf)
    if sdf then
        return Font(path, nil, true)
    else
        return Font(path)
    end
end

---
-- Constructor
-- @param json  skeleton json path
-- @param atlas skeleton atlas path
-- @param scale skeleton json scale
function _createSkeletonData(json, atlas, scale)
    scale = scale or 1
    local data = MOAISpineSkeletonData.new()
    data:load(json, atlas, scale)
    return data
end

---
-- Spine callback functions
function _spineReadFile(path)
    local fullPath = ResourceMgr:getResourceFilePath(path)
    assert(fullPath, "Spine: file not found " .. path)
    return fullPath
end

function _spineCreateTexture(path)
    local texture = ResourceMgr:getTexture(path)
    assert(texture, "Spine: failed to create texture " .. path)
    return texture
end

---
-- 
function ResourceMgr:initialize()
    if MOAISpine then
        MOAISpine.setReadFile(_spineReadFile)
        MOAISpine.setCreateTexture(_spineCreateTexture)
    end
end


---
-- Add the resource directory path.
-- You can omit the file path by adding.
-- It is assumed that the file is switched by the resolution and the environment.
-- @param path resource directory path
-- @param scale (option) resolution scale for image files
-- @param threshold (option) when viewport scale is bigger than threshold, this directory will have a priority over another
function ResourceMgr:addResourceDirectory(path, scale, threshold)
    scale = scale or 1
    threshold = threshold or 0
    local dirInfo = {path = path, scale = scale, threshold = threshold}
    
    table.push(self.resourceDirectories, dirInfo)
    table.sort(self.resourceDirectories, function(a, b) return a.threshold > b.threshold end)
end

---
-- Search in ResourceDirectories for file. 
-- @param fileName name of the file
-- @return filePath, scale  returns full path to file and scale factor of the directory that contain this file
local NOT_FOUND = function() end
function ResourceMgr:getResourceFilePath(fileName)
    local cache = self.filepathCache
    if cache[fileName] then
        if cache[fileName] == NOT_FOUND then
            return nil
        else
            return unpack(cache[fileName])
        end
    end

    if MOAIFileSystem.checkFileExists(fileName) then
        cache[fileName] = {fileName, 1} 
        return fileName, 1
    end

    local scaleFactor = App:getContentScale() or 1
    for i, pathInfo in ipairs(self.resourceDirectories) do
        if pathInfo.threshold <= scaleFactor then
            local filePath = string.pathJoin(pathInfo.path, fileName)
            if MOAIFileSystem.checkFileExists(filePath) then
                cache[fileName] = {filePath, pathInfo.scale}
                return filePath, pathInfo.scale
            end
        end
    end

    cache[fileName] = NOT_FOUND
    return nil
end

---
-- Clear cached filename aliases
function ResourceMgr:clearFilenameCache()
    for k, v in pairs(self.filepathCache) do
        self.filepathCache[k] = nil
    end

end

---
-- Loads (or obtains from its cache) a texture and returns it.
-- Textures are cached.
-- @param path The path of the texture
-- @return Texture instance
function ResourceMgr:getTexture(path, filter)
    if type(path) == "userdata" then
        return path
    end
    
    local cache = self.textureCache
    local filepath, scale = self:getResourceFilePath(path)
    
    if not filepath then
        return nil
    end
    
    filter = filter or ResourceMgr.DEFAULT_TEXTURE_FILTER
    local texture = cache[filepath]
    if texture == nil then
        texture = _createTexture(filepath, filter)
        texture.scale = scale
        texture.name = path
        cache[filepath] = texture
    end
    return texture
end

---
-- Add texture to cache manually
function ResourceMgr:setTexture(texture, key, scale)
    texture.name = key
    texture.scale = scale or 1
    self.textureCache[key] = texture
end

---
-- Removes texture from internall cache. It will not be released until someone uses it,
-- but call to getTexture will allocate a new instance. 
function ResourceMgr:removeTexture(path)
    local filepath, scale = self:getResourceFilePath(path)
    self.textureCache[filepath] = nil
end

---
-- Loads (or obtains from its cache) a font and returns it.
-- @param path The path of the font.
-- @param sdf   return sdf version of font
-- @return Font instance
function ResourceMgr:getFont(path, sdf)
    if type(path) == "userdata" then
        return path
    end

    local cache = sdf and self.fontSDFCache or self.fontCache
    local fullPath = self:getResourceFilePath(path)

    assert(fullPath, "Font not found: " .. path)

    if cache[fullPath] == nil then
        local font = _createFont(fullPath, sdf)
        cache[fullPath] = font
    end
    return cache[fullPath]
end

---
-- Loads (or obtains from its cache) a spine skeleton data and returns it.
-- @param json  skeleton json path. 
-- @param atlas spine atlas path. 
-- @param scale Skeleton json scale. This value is the convertion ratio from pixels (in spine editor) to
--              moai viewport coordinates. Most commonly, this is 0.5 (the default), since viewport scale
--              is set up so we use the same units for retina and non-retina devices. 
-- @return MOAISpineSkeleton
function ResourceMgr:getSpineSkeletonData(json, atlas, scale)
    local cache = self.skeletonCache

    scale = scale or ResourceMgr.SPINE_JSON_SCALE
    local jsonPath = self:getResourceFilePath(json)
    local atlasPath = self:getResourceFilePath(atlas)
    
    assert(jsonPath, "Skeleton json not found: " .. json)
    assert(atlasPath, "Skeleton atlas not found: " .. atlas)

    local key = jsonPath .. "@" .. atlasPath
    if cache[key] == nil then
        local skeletonData = _createSkeletonData(jsonPath, atlasPath, scale)
        cache[key] = skeletonData
    end
    return cache[key]
end

---
-- Returns the file data.
-- @param fileName file name
-- @return file data
function ResourceMgr:readFile(fileName)
    local path = self:getResourceFilePath(fileName)
    local input = assert(io.input(path))
    local data = input:read("*a")
    input:close()
    return data
end

---
-- Returns the result of executing the dofile.
-- Browse to the directory of the resource.
-- @param fileName lua file name
-- @return results of running the dofile
function ResourceMgr:dofile(fileName)
    local filePath = self:getResourceFilePath(fileName)
    return dofile(filePath)
end

---
-- Load table from lua file. Sets environment to empty table to prevent any code from execution
-- @param fileName
-- @return table
function ResourceMgr:loadTable(fileName)

    local filePath = self:getResourceFilePath(fileName)
    assert(filePath, 'File not found: ' .. tostring(fileName))
    --print("filePath", filePath)
    local tbl = assert(loadfile(filePath))
    setfenv(tbl, {})
    return tbl()
end

---
-- Traverse all decks and reload their texture if they now available with new path. 
-- Can be used after mounting new directory with updated content. 
function ResourceMgr:syncDecks()
    -- This should collect any unused textures by ResourceMgr. 
    -- They still can be cached somewhere out of ResourceMgr, then reloading won't work
    MOAISim.forceGC()

    self:clearFilenameCache()

    for _, deck in pairs(self.imageDecks) do
        local textureName = deck.texture.name
        local path = self:getResourceFilePath(textureName)
        if deck.texture.path ~= path then
            log.info(string.format("Reloading texture %s (old path: %s)", path, deck.texture.path))

            self:removeTexture(textureName)
            local texture = self:getTexture(textureName)
            deck:setTexture(texture)
            deck.texture = texture
        end
    end

    for _, deck in pairs(self.atlasDecks) do
        local textureName = deck.atlas.texture
        local path = self:getResourceFilePath(textureName)
        if deck.texture.path ~= path then
            log.info(string.format("Reloading atlas texture %s (old path: %s)", path, deck.texture.path))

            self:removeTexture(textureName)
            local texture = self:getTexture(textureName)
            deck:setTexture(texture)
            deck.texture = texture

            -- Reloading rects and UV's doesn't work with current Display.Sprite implementation. 
            -- Sprite uses prop:setScl to adjust for proper size, but should use deck:setRect instead. 
            -- However, decks are shared objects and altering rect will affect all props using this deck. 
            -- self:initAtlasDeck(deck, deck.luaAtlasPath)
        end
    end
end


function ResourceMgr:softReleaseResources(age)
    MOAIGfxResourceMgr.purgeResources(age)
end

--------------------------------------------------------------------------------
-- MOAIDeck cache
--------------------------------------------------------------------------------

---
-- Return proper Deck based on frame name. Lookup priorities: 
--   1) if image has extension in format .9.ext (ext can be any: png, jpg, etc) then
--      nine-patch deck is returned
--   2) if single image texture is found in resource directories it is returned
--   3) image is searched in known atlas decks
--   4) assert is invoked
-- 
-- @param fileName  name of the texture, atlas sprite frame, nine-patch
-- @return deck
function ResourceMgr:getDeck(fileName)
    local deck
    
    if string.find(fileName, "%.9%.[^%.]+$") then
        deck = ResourceMgr:getNineImageDeck(fileName)
    else
        deck = ResourceMgr:getImageDeck(fileName)
    end

    if not deck then
        local atlas = ResourceMgr:getAtlasName(fileName)
        assert(atlas, "Image not found: " .. fileName)
        deck = ResourceMgr:getAtlasDeck(atlas)
    end
    
    return deck
end


---
-- Return the Deck for texture.
-- @return deck
function ResourceMgr:getImageDeck(texture)
    texture = self:getTexture(texture)
    
    if not texture then
        return nil
    end

    local tw, th = texture:getSize()
    local scale = texture.scale
    local width = tw / scale
    local height = th / scale

    local key = texture.path
    local cache = self.imageDecks

    if not cache[key] then
        -- tile images should have rect of (1, 1)
        if string.find(texture.name, "%.tile%.[^%.]+$") then
            width, height = 1, 1
        end
        cache[key] = self:createImageDeck(texture, width, height)
    end
    return cache[key]
end

---
-- Create the Deck to be used in the Image.
-- @param width width
-- @param height height
-- @param flipX (Optional)flipX
-- @param flipY (Optional)flipY
-- @return deck
function ResourceMgr:createImageDeck(texture, width, height, flipX, flipY)
    local u0 = flipX and 1 or 0
    local v0 = flipY and 0 or 1
    local u1 = flipX and 0 or 1
    local v1 = flipY and 1 or 0
    local deck = MOAIGfxQuad2D.new()
    deck:setUVRect(u0, v0, u1, v1)
    deck:setRect(-0.5 * width, -0.5 * height, 0.5 * width, 0.5 * height)
    deck:setTexture(texture)
    deck.texture = texture
    deck.flipX = flipX
    deck.flipY = flipY
    return deck
end


---
-- Find atlas name for given sprite frame name
-- @param spriteFrameName sprite name
-- @return string atlas lua file name
function ResourceMgr:getAtlasName(spriteFrameName)
    return ResourceMgr.spriteFrameAtlases[spriteFrameName]
end

---
-- Assign atlas name for sprite frame
function ResourceMgr:setAtlasForSprite(luaFilePath, spriteFrameName)
    local existing = self.spriteFrameAtlases[spriteFrameName]

    assert(existing == nil or existing == luaFilePath, 
        string.format("Duplicate sprite frame name %s in different atlases: %s and %s", spriteFrameName, luaFilePath, existing or ""))

    self.spriteFrameAtlases[spriteFrameName] = luaFilePath
end

function ResourceMgr:cacheSpriteFrames(luaFilePath, shader)
    local frames = self:loadTable(luaFilePath).frames
    for i, frame in ipairs(frames) do
        self:setAtlasForSprite(luaFilePath, frame.name)
    end
    self.deckParams[luaFilePath] = {shader = shader}
end

---
-- Return the Deck for displaying TextureAtlas.
-- @param luaFilePath TexturePacker lua file path
-- @param flipX (option)flipX
-- @param flipY (option)flipY
-- @return Texture atlas deck
function ResourceMgr:getAtlasDeck(luaFilePath)
    -- local key = luaFilePath .. "$" .. tostring(flipX) .. "$" .. tostring(flipY)
    local key = luaFilePath
    local cache = self.atlasDecks

    if not cache[key] then
        cache[key] = self:createAtlasDeck(luaFilePath)
    end
    return cache[key]
end

---
-- Create the Deck for displaying TextureAtlas.
-- Images ending with extension ".tile.*" treated as Grid tiles
-- @param luaFilePath TexturePacker lua file path
-- @return Texture atlas deck
function ResourceMgr:createAtlasDeck(luaFilePath)
    local boundsDeck = MOAIBoundsDeck.new()
    local deck = MOAIGfxQuadDeck2D.new()
    deck:setBoundsDeck(boundsDeck)
    deck.boundsDeck = boundsDeck
    self:initAtlasDeck(deck, luaFilePath)

    local params = self.deckParams[luaFilePath]
    if params then
        if params.shader then
            deck:setShader(params.shader)
        end
    end

    return deck
end

---
-- Parse lua file generated by TexturePacker and initialize deck quads
-- Images ending with extension ".tile.*" treated as Grid tiles
-- @param MOAIGfxQuadDeck2D deck    deck to set indicies for. Must include boundsDeck as field
-- @param luaFilePath TexturePacker lua file path
-- @return Texture atlas deck
function ResourceMgr:initAtlasDeck(deck, luaFilePath)
    local atlas = self:loadTable(luaFilePath)
    local frames = atlas.frames
    local boundsDeck = deck.boundsDeck
    boundsDeck:reserveBounds(#frames)
    boundsDeck:reserveIndices(#frames)

    deck:setBoundsDeck(boundsDeck)
    deck:reserve(#frames)
    deck.names = {}
    deck.luaAtlasPath = luaFilePath

    local texture = self:getTexture(atlas.texture)
    if not texture then
        local alternatePath = string.pathJoin(string.pathDir(luaFilePath), atlas.texture)
        texture = self:getTexture(alternatePath)
        assert(texture, "ResourceMgr: texture not found for atlas " .. tostring(luaFilePath))
        texture.scale = App:getContentScale()
    end

    local inv_scale = 1 / texture.scale
    deck.texture = texture
    deck.atlas = atlas
    deck:setTexture(texture)

    for i, frame in ipairs(frames) do
        local uvRect = frame.uvRect
        local uv = {uvRect.u0, uvRect.v0, uvRect.u1, uvRect.v0, uvRect.u1, uvRect.v1, uvRect.u0, uvRect.v1}
        local r = frame.spriteColorRect
        local b = frame.spriteSourceSize

        table.every(r, function(v, i) r[i] = inv_scale * v end)
        table.every(b, function(v, i) b[i] = inv_scale * v end)

        if frame.textureRotated then
            uv = {uv[3], uv[4], uv[5], uv[6], uv[7], uv[8], uv[1], uv[2]}
        end

        deck:setUVQuad(i, unpack(uv))
        deck.names[frame.name] = i

        if string.find(frame.name, "%.tile%.[^%.]+$") then
            deck:setRect(i, -0.5, -0.5, 0.5, 0.5)
            boundsDeck:setBounds(i, -0.5, -0.5, 0, 0.5, 0.5, 0)
        else
            deck:setRect(i, r.x - 0.5 * b.width, 0.5 * b.height - r.height - r.y, r.x + r.width - 0.5 * b.width, 0.5 * b.height - r.y)
            boundsDeck:setBounds(i, -0.5 * b.width, -0.5 * b.height, 0, 0.5 * b.width, 0.5 * b.height, 0)
        end
        boundsDeck:setIndex(i, i)

        self:setAtlasForSprite(luaFilePath, frame.name)
    end

    return deck
end

---
-- Returns the Deck to draw NineImage.
-- @param string path 
-- @return MOAIStretchPatch2D instance
function ResourceMgr:getNineImageDeck(filePath)
    local cache = self.nineImageDecks

    if not cache[filePath] then
        cache[filePath] = self:createNineImageDeck(filePath)
    end
    return cache[filePath]
end

---
-- Create the Deck to draw NineImage.
-- It will first try to find single image with the given name with
-- fallback to cached atlas frame. 
-- @param fileName fileName
-- @return MOAIStretchPatch2D instance
function ResourceMgr:createNineImageDeck(fileName)
    local texture = self:getTexture(fileName)
    local atlasDeck = nil
    
    if not texture then
        local atlas = self:getAtlasName(fileName)
        assert(atlas, "Nine Image not found: " .. fileName)
        atlasDeck = self:getAtlasDeck(atlas)
        texture = atlasDeck.texture
    end

    local scale = texture.scale
    local image = MOAIImage.new()
    image:load(texture.path)

    local imageWidth, imageHeight = image:getSize()
    local imageLeft, imageBottom, imageTop, imageRight = 0, imageHeight, 0, imageWidth
    local rotate = false
    if atlasDeck then
        local frame = atlasDeck.atlas.frames[ atlasDeck.names[fileName] ]
        local u0, v1, u1, v0 = frame.uvRect.u0, frame.uvRect.v1, frame.uvRect.u1, frame.uvRect.v0

        imageTop = math.round(imageHeight * v0)
        imageLeft = math.round(imageWidth * u0)
        imageRight = math.round(imageWidth * u1)
        imageBottom = math.round(imageHeight * v1)
    end
    
    local displayWidth, displayHeight = (imageRight - imageLeft - 4) / scale, (imageBottom - imageTop - 4) / scale
    local stretchRows = _createStretchRowsOrColumns(image, imageLeft, imageRight, imageTop, imageBottom, true)
    local stretchColumns = _createStretchRowsOrColumns(image, imageLeft, imageRight, imageTop, imageBottom, false)
    local left, top, right, bottom = _getNineImageContentPadding(image, imageLeft, imageRight, imageTop, imageBottom)
    local uvRect = {(imageLeft + 2) / imageWidth, (imageBottom - 2) / imageHeight, (imageRight - 2) / imageWidth, (imageTop + 2) / imageHeight}

    local deck = MOAIStretchPatch2D.new()
    deck.texture = texture
    deck.imageWidth = imageWidth
    deck.imageHeight = imageHeight
    deck.displayWidth = displayWidth
    deck.displayHeight = displayHeight
    deck.contentPadding = {left / scale, top / scale, right / scale, bottom / scale}
    deck:reserveUVRects(1)
    deck:setTexture(texture)
    deck:setRect(-0.5 * displayWidth, -0.5 * displayHeight, 0.5 * displayWidth, 0.5 * displayHeight)
    deck:setUVRect(1, unpack(uvRect))
    deck:reserveRows(#stretchRows)
    deck:reserveColumns(#stretchColumns)

    for i, row in ipairs(stretchRows) do
        deck:setRow(i, row.weight, row.stretch)
    end
    for i, column in ipairs(stretchColumns) do
        deck:setColumn(i, column.weight, column.stretch)
    end

    return deck
end

function _createStretchRowsOrColumns(image, imageLeft, imageRight, imageTop, imageBottom, isRow)
    local stretchs = {}
    local from = isRow and (imageTop + 1) or (imageLeft + 1)
    local to = isRow and (imageBottom - 1) or (imageRight - 1)
    local distance = to - from
    local stretchSize = 0
    local pr, pg, pb, pa = image:getRGBA(isRow and imageLeft or 1, isRow and 1 or imageTop)

    for i = from, to - 1 do
        local r, g, b, a = image:getRGBA(isRow and imageLeft or i, isRow and i or imageTop)
        stretchSize = stretchSize + 1

        if pa ~= a then
            table.insert(stretchs, {weight = stretchSize / distance, stretch = pa > 0})
            pa, stretchSize = a, 0
        end
    end
    if stretchSize > 0 then
        table.insert(stretchs, {weight = stretchSize / distance, stretch = pa > 0})
    end

    if isRow then 
        stretchs = table.reverse(stretchs) 
    end

    return stretchs
end

function _getNineImageContentPadding(image, imageLeft, imageRight, imageTop, imageBottom)
    local paddingLeft = 0
    local paddingTop = 0
    local paddingRight = 0
    local paddingBottom = 0

    for x = imageLeft, imageRight - 2 do
        local r, g, b, a = image:getRGBA(x + 1, imageBottom - 1)
        if a > 0 then
            paddingLeft = x - 1
            break
        end
    end
    for x = imageLeft, imageRight - 2 do
        local r, g, b, a = image:getRGBA(imageRight - imageLeft - x - 2, imageBottom - 1)
        if a > 0 then
            paddingRight = x - 1
            break
        end
    end
    for y = imageTop, imageBottom - 2 do
        local r, g, b, a = image:getRGBA(imageRight - 1, y + 1)
        if a > 0 then
            paddingTop = y - 1
            break
        end
    end
    for y = imageTop, imageBottom - 2 do
        local r, g, b, a = image:getRGBA(imageRight - 1, imageBottom - imageTop - y - 2)
        if a > 0 then
            paddingBottom = y - 1
            break
        end
    end

    return paddingLeft, paddingTop, paddingRight, paddingBottom
end

return ResourceMgr