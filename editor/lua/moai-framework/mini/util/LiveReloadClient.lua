--------------------------------------------------------------------------------
-- Just import this script to enable live reload of code and assets on device
-- 
-- 
--------------------------------------------------------------------------------

local M = {}

local ResourceMgr = require("core.ResourceMgr")
local SceneMgr = require("core.SceneMgr")
local Runtime = require("core.Runtime")
local Scene = require("core.Scene")

local socket = require "socket"
local ltn12 = require "ltn12"
local PORT = 8970
local CMD_PORT = 8971
local MAGIC_HEADER = "MOAI_REMOTE:"
local PING = MAGIC_HEADER.."PING"
local PONG = MAGIC_HEADER.."PONG:"
local UPDATE = MAGIC_HEADER.."UPDATE:"
local UPDATE_SUCCESS = MAGIC_HEADER.."UPDATE_SUCCESS:"
local RESTART = MAGIC_HEADER.."RESTART"
local CLEAR = MAGIC_HEADER.."CLEAR"
local RUN_STRING = MAGIC_HEADER.."RUN_STRING"

local IMAGE_EXTENSIONS = {[".jpg"] = true, [".png"] = true}
local LUA_EXTENSIONS = {[".lua"] = true}

local LIVE_UPDATE_PATH = string.pathJoin(MOAIEnvironment.documentDirectory, "live_update")

local function try(func)
    return xpcall(func, 
        function(err) 
            print(err) 
            print(debug.traceback())
        end)
end

---
-- If reloaded file is currently running scene - then restart it
-- Files with scenes determined by their directory
local function restartScene(requirePath)
    -- remove current scene from cache, so it can be reloaded
    print("Live Reload Client: ", SceneMgr.currentScene, SceneMgr.currentScene.name, SceneMgr.currentScene.onPointClick)
    if SceneMgr.currentScene.name then
        package.loaded[SceneMgr.currentScene.name] = nil
        try(function() SceneMgr:replaceScene(SceneMgr.currentScene.name) end)
    end
end

---
--
local function runString(str)
    local f = loadstring(str)
    try(f)
end

---
-- 
local function receiveStr(ip)
    local sock = assert(socket.tcp())
    sock:settimeout(10)
    sock:setoption('reuseaddr', true)
    local result, err = sock:bind('*', CMD_PORT)
    if result == 0 then
        sock:close()
        return
    end

    sock:listen()
    local client, err = sock:accept()
    if client then
        data = client:receive('*a')
        if data then
            runString(data)
        end
    end
    sock:close()
end

---
-- Reload texture in the cache
-- All props and decks will be updated automatically
local function reloadTexture(texturePath)
    local shortest = texturePath
    -- remove possible resourceDir prefix from path
    for _, info in pairs(ResourceMgr.resourceDirectories) do
        local path = string.gsub(texturePath, '^' .. info.path, '')
        if #path < #shortest then
            shortest = path
        end
    end
    local sep = package.config:sub(1, 1)
    if shortest:sub(1, 1) == sep then
        shortest = shortest:sub(2)
    end

    log.info("PATH AFTER TRIM", shortest)
    local filepath = ResourceMgr:getResourceFilePath(shortest)
    local texture = ResourceMgr.textureCache[filepath]
    if texture then
        log.info('reloading', filepath)
        texture:load(filepath)
        texture:purge()
    end
end

---
-- Update decks for all sprites that were created with this texturePath
local function updateSprites(texturePath)
    local list = M.sprites[texturePath]
    if not list then return end
    local deck = ResourceMgr:getDeck(texturePath)
    for i, v in ipairs(list) do
        v:setDeck(deck)
        v.deck = deck
        v:setIndexByName(texturePath)
    end
end

local function updateFile(relPath)
    local requirePath
    local ext = string.sub(relPath, -4)
    if LUA_EXTENSIONS[ext] then
        requirePath = string.gsub(relPath, ".lua", "")
        requirePath = string.gsub(requirePath, "/", ".")
        package.loaded[requirePath] = nil

        restartScene(requirePath)
        -- end
    end

    log.info("UPDATE FILE")
    if IMAGE_EXTENSIONS[ext] then
        log.info("This is image", relPath)
        reloadTexture(relPath)
        updateSprites(relPath)
    end
end


local function runnerFunc()
    local sock = assert(socket.udp())
    assert(sock:setsockname("*", PORT))
    assert(sock:settimeout(0))
    M.socket = sock
    while true do
        local data, ip, port = sock:receivefrom()
        if data then
            if data:sub(1, #PING) == PING then
                local name = MOAIEnvironment.devName or "unknown device"
                sock:sendto(PONG .. name, ip, port)

            elseif data:sub(1, #CLEAR) == CLEAR then
                M:clearOverrides()

            elseif data:sub(1, #RUN_STRING) == RUN_STRING then
                print("received RUN_STRING")
                receiveStr(ip)

            elseif data:sub(1, #UPDATE) == UPDATE then
                local dataPort = data:sub(#UPDATE + 1, #UPDATE + 5)
                local localPath = data:sub(#UPDATE + 6)

                local dataSock = assert(socket.tcp())
                assert(dataSock:connect(ip, tonumber(dataPort)))
                local source = socket.source("until-closed", dataSock)
                local archivePath = string.pathJoin(LIVE_UPDATE_PATH, localPath)
                MOAIFileSystem.affirmPath(string.pathDir(archivePath))
                local file = assert(io.open(archivePath, "wb"))
                local sink = ltn12.sink.file(file)
                while ltn12.pump.step(source, sink) do
                    coroutine.yield()
                end

                dataSock:close()

                updateFile(localPath)
            end
        end
        coroutine.yield()
    end
    M.socket = nil
    sock:close()
end

---
-- @param table sourcePath Custom src path
function M:init(sourcePath)
    if MOAIEnvironment.documentDirectory then
        local paths = ""
        for i, v in ipairs(sourcePath) do
            paths = paths .. string.pathJoin(LIVE_UPDATE_PATH, v) .. ';'
        end
        package.path = paths .. package.path

        -- resource directories are sorted in descending order by scale threshold 
        -- here we increase threshold slightly to force lookup of live_update assets before the main assets
        local newResources = {}
        for k, v in pairs(ResourceMgr.resourceDirectories) do
            local path = string.pathJoin(LIVE_UPDATE_PATH, v.path) 
            newResources[#newResources+1] = {path, v.scale, v.threshold + 0.001}
        end

        for k, v in pairs(newResources) do
            ResourceMgr:addResourceDirectory(unpack(v))
        end
    end

    local function onSessionEnd()
        self:stop()
    end

    local function onSessionStart()
        self:start()
    end

    Runtime:addEventListener(Event.SESSION_START, onSessionStart)
    Runtime:addEventListener(Event.SESSION_END, onSessionEnd)

    self.sprites = {}
    self:start()
end

function M:start()
    if not self.runner then
        local runner = MOAICoroutine.new()
        runner:run(runnerFunc)
        self.runner = runner
    end
end

function M:stop()
    if self.runner then
        self.runner:stop()
        self.runner = nil
        if self.socket then
            self.socket:close()
            self.socket = nil
        end
    end
end

function M:updateFile(localPath)
    updateFile(localPath)
end

function M:clearOverrides()
    MOAIFileSystem.deleteDirectory(LIVE_UPDATE_PATH, true)
    MOAIFileSystem.affirmPath(LIVE_UPDATE_PATH)
end

---
-- Add sprite to watch list
-- When its texture is updated a new deck will be set
function M:addSprite(prop, texturePath)
    local list = self.sprites[texturePath]
    if not list then
        list = setmetatable({}, {__mode = "v"})
        self.sprites[texturePath] = list
    end

    table.insert(list, prop)
end

return M

