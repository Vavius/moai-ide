--------------------------------------------------------------------------------
-- Live-reload implementation for MOAI SDK
-- Folder-watcher script + socket file transport
-- 
-- @author vavius <Vasiliy Yanushevich>
--------------------------------------------------------------------------------

local socket = require("socket")
local ltn12 = require "ltn12"

local DATA_SEND_TIMEOUT = 2
local PORT = 8970
local CMD_PORT = 8971
local DATA_PORT_START = 51198
local MAGIC_HEADER = "MOAI_REMOTE:"
local PING = MAGIC_HEADER.."PING"
local PONG = MAGIC_HEADER.."PONG:"
local UPDATE = MAGIC_HEADER.."UPDATE:"
local UPDATE_SUCCESS = MAGIC_HEADER.."UPDATE_SUCCESS:"
local RESTART = MAGIC_HEADER.."RESTART"
local CLEAR = MAGIC_HEADER.."CLEAR"
local RUN_STRING = MAGIC_HEADER.."RUN_STRING"

local sendFile
local onFileChanged
local search

local dataPort = DATA_PORT_START
local skip = false


-- Listen and find available deployment devices on local network that run liveReload app
-- returns ip address
function search(timeout)
    local deviceList = {}
    timeout = timeout or 2
    local sock = assert(socket.udp())
    assert(sock:settimeout(timeout))
    assert(sock:setoption("broadcast", true))
    sock:sendto(PING, "255.255.255.255", PORT)
    while true do
        local data, ip, port = sock:receivefrom()
        if data then
            if data:sub(1, #PONG) == PONG then
                print("Pong", ip)
                deviceList[#deviceList + 1] = {ip = ip, name = data:sub(#PONG + 1)}
                skip = false
            end
        else
            break
        end
    end

    return deviceList
end

function sendFile(workingDir, path, address, attempts)
    attempts = attempts or 3
    if attempts < 0 or skip then
        skip = true
        return
    end

    print('changed', path)

    local file = assert(io.open(workingDir .. path, "rb"))
    local cmdSock = assert(socket.udp())
    local dataSock = assert(socket.tcp())

    local tryCmd = socket.newtry(function() cmdSock:close() end)

    dataSock:settimeout(DATA_SEND_TIMEOUT)
    dataSock:bind("*", dataPort)
    assert(dataSock:listen(1))
    
    tryCmd(cmdSock:sendto(UPDATE .. dataPort .. path, address, PORT))

    local client, err = dataSock:accept()

    if client == nil then
        print('waiting for client failed: ' .. err)
        dataSock:close()
        cmdSock:close()
        sendFile(workingDir, path, address, attempts - 1)
    else
        dataPort = dataPort + 1
        local sink = socket.sink("close-when-done", client)
        local source = ltn12.source.file(file)
        if ltn12.pump.all(source, sink) then
            print('file sent successfully', path)
        else
            print('error sending file', path)
            dataSock:close()
            cmdSock:close()
            sendFile(workingDir, path, address, attempts - 1)
        end
    end

    dataSock:close()
    cmdSock:close()
end

function sendCommand(address, cmd)
    local cmdSock = assert(socket.udp())
    cmdSock:sendto(cmd, address, PORT)
    cmdSock:close()
end

function onFileChanged(workingDir, path, address)
    if not workingDir or not path or not address then
        return
    end
    sendFile(workingDir, path, address, 5)
end

function onClearRemoteOverrides(address)
    sendCommand(address, CLEAR)
end

function onRunString(address, string)
    sendCommand(address, RUN_STRING)
    -- sleep some time so client have chance to open socket
    socket.sleep(1)

    for i = 1, 3 do
        local stringSock = assert(socket.tcp())
        stringSock:settimeout(1)
        local result, err = stringSock:connect(address, CMD_PORT)
        if result then
            stringSock:send(string)
            stringSock:close()
            break
        else
            socket.sleep(0.5)
        end
        stringSock:close()
    end
end


-- Module
local M = {
    search = search,
    onFileChanged = onFileChanged,
    onClearRemoteOverrides = onClearRemoteOverrides,
    onRunString = onRunString,
}

return M