import sys, os
import platform
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from PySide import QtCore
import luainterface

class FileChangedHandler(PatternMatchingEventHandler):
    callback = None

    def on_modified(self, event):
        # print("file modified:",event.src_path)
        src_path = event.src_path
        if self.callback:
            self.callback(src_path)

    def on_created(self, event):
        src_path = event.src_path
        if self.callback:
            self.callback(src_path)

    def on_moved(self, event):
        dest_path = event.dest_path
        if self.callback:
            self.callback(dest_path)


class LiveReload:
    fileWatcher = None
    eventHandler = None
    lua = None
    fullReloadFunc = None
    directory = None
    deviceIP = None
    changedFiles = set()

    def __init__(self):
        self.eventHandler = FileChangedHandler(patterns = ["*.lua", "*.png", "*.jpg", "*.ttf", "*.otf", "*.pvr"], ignore_directories=True)
        self.eventHandler.callback = self.onFileChanged

    def watchDirectory(self, directory):
        if self.directory == directory:
            return

        if self.fileWatcher:
            self.fileWatcher.stop()
            self.fileWatcher.unschedule_all()

        self.changedFiles.clear()
        self.directory = directory
        self.fileWatcher = Observer()
        self.fileWatcher.schedule(self.eventHandler, path=directory, recursive=True)
        self.fileWatcher.start()

    def searchDevices(self):
        if self.lua:
            pass

    def onFileChanged(self, filePath):
        self.changedFiles.add(filePath)

    def update(self):
        if self.changedFiles:
            if self.local:
                if self.full:
                    self.fullReloadFunc()
                # else:
                    # self.reloadLocal()
            if self.remote:
                self.reloadRemote()

            self.changedFiles.clear()

    def reloadLocal(self):
        if not self.lua:
            return
        
        for f in self.changedFiles:
            # ensure we have a trailing slash in dirname
            wDir = os.path.join(self.directory, '')
            if f.startswith(wDir):
                localPath = f[len(wDir):]
                luainterface.reloadLocalFile(self.lua, localPath)

    def reloadRemote(self):
        if not self.lua or not self.deviceIP:
            return

        for f in self.changedFiles:
            wDir = os.path.join(self.directory, '')
            localPath = f[len(wDir):]
            luainterface.reloadFile(self.lua, wDir, localPath, self.deviceIP)

    def runStringRemote(self, luaStr):
        if not self.deviceIP:
            return
        luainterface.runStringRemote(self.lua, self.deviceIP, luaStr)

    def clearRemoteOverrides(self):
        if not self.deviceIP:
            return
        luainterface.clearRemoteOverrides(self.lua, self.deviceIP)


    def setCurrentDeviceIP(self, deviceIP):
        self.deviceIP = deviceIP

    def setAutoreloadDevice(self, flag):
        self.remote = flag

    def setAutoreloadHost(self, flag):
        self.local = flag

    def setAutoreloadFull(self, flag):
        self.full = flag
