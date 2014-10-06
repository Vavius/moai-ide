from PySide import QtCore, QtGui
import luainterface

# Lua interface to native file open/save dialogs
# 

def openFile(parent, caption = "Open file", directory = None, filter = None):
    fileName, filt = QtGui.QFileDialog.getOpenFileName(parent, caption, directory, filter)
    return fileName


def saveFile(parent, caption = "Save file", directory = None, filter = None):
    fileName, filt = QtGui.QFileDialog.getSaveFileName(parent, caption, directory, filter)
    return fileName


class FileDialog():
    def __init__(self, lua, parent):
        self.lua = lua
        self.parent = parent
        self.registerLuaFuncs()


    def registerLuaFuncs(self):
        openFunc = self.lua.eval("""function(pyFunc, parent)
            OpenFileDialog = function(caption, dir, filter)
                return pyFunc(parent, caption, dir, filter)
            end
        end
        """)

        saveFunc = self.lua.eval("""function(pyFunc, parent)
            SaveFileDialog = function(caption, dir, filter)
                return pyFunc(parent, caption, dir, filter)
            end
        end
        """)

        openFunc(openFile, self.parent)
        saveFunc(saveFile, self.parent)
