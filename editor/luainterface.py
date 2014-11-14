#
# Editor lua interface wrapped into python functions
#

def search(lua):
    deviceList = lua.require("util.LiveReloadServer").search(2)
    pyDevices = []
    for k, v in deviceList.items():
        pyDevices.append({"ip" : v.ip, "name" : v.name})

    return pyDevices

def reloadFile(lua, workingDir, path, deviceIP):
    liveReloadServer = lua.require("util.LiveReloadServer")
    liveReloadServer.onFileChanged(workingDir, path, deviceIP)

def reloadLocalFile(lua, path):
    liveReloadClient = lua.require("util.LiveReloadClient")
    liveReloadClient.updateFile(liveReloadClient, path)

def clearRemoteOverrides(lua, deviceIP):
    liveReloadServer = lua.require("util.LiveReloadServer")
    liveReloadServer.onClearRemoteOverrides(deviceIP)

def runStringRemote(lua, deviceIP, luaStr):
    liveReloadServer = lua.require("util.LiveReloadServer")
    liveReloadServer.onRunString(deviceIP, luaStr)

def runConsoleCommand(lua, cmd):
    console = lua.require("console")
    return console.run(cmd)

def setConsolePrint(lua, func1, func2):
    console = lua.require("console")
    console.setPrint(func1, func2)
