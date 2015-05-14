#!/usr/bin/python

import sys

from colorama import Fore, Back, Style
from time import strftime

import luainterface


def coloredBeforePrint(color, brightness):
    def beforePrint():
        style = strftime("%H:%M:%S")
        style = style + Style.RESET_ALL + color + brightness
        style = style + '  '
        print style,
    return beforePrint
    
def afterPrint():
    style = Style.RESET_ALL + Style.DIM
    sys.stdout.write(style)


class ColoredLog():
    def __init__(self, lua):
        self.lua = lua
        self.enableColoredLog()

    def setColoredPrintFunc(self, name, before, after):
        tmpName = name.replace('.', '')
        setFunc = self.lua.eval("""function(before, after)
            local logfunc = %(name)s
            %(name)s = function(...)
                before()

                -- 1 itself, 2 the caller
                local info = debug.getinfo(2, 'Sln')
                local dbg
                if info and info.what == 'Lua' and info.source:sub(1, 1) == "@" then
                    local src = string.pathFile(info.source)
                    dbg = string.format('(%%s %%s:%%d) \t', src, info.name or 'unknown', info.currentline or 0)
                    logfunc(dbg, ...)
                else
                    logfunc(...)
                end
                after()
            end
            log.setLogLevel(log.DEBUG)
        end""" % {'name' : name})
        setFunc(before, after)


    def enableColoredLog(self):
        self.setColoredPrintFunc('log.__debug',    coloredBeforePrint(Fore.WHITE, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__info',     coloredBeforePrint(Fore.CYAN, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__warning',  coloredBeforePrint(Fore.YELLOW, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__error',    coloredBeforePrint(Fore.RED, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__critical', coloredBeforePrint(Fore.RED, Style.BRIGHT), afterPrint)
