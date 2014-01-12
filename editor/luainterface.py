#
# Editor lua interface wrapped into python functions
#

def search(lua):
    deviceList = lua.require("util.LiveReloadServer").search(2)
    pyDevices = []
    for k, v in deviceList.items():
        pyDevices.append({"ip" : v.ip, "name" : v.name})

    return pyDevices

def reloadFile(lua, path, deviceIP):
    liveReloadServer = lua.require("util.LiveReloadServer")
    liveReloadServer.onFileChanged(liveReloadServer, workingDir, path, deviceIP)

def reloadLocalFile(lua, path):
    liveReloadClient = lua.require("util.LiveReloadClient")
    liveReloadClient.updateFile(liveReloadClient, path)
