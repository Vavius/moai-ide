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
            %(tmpName)s = %(name)s
            %(name)s = function(...)
                before()
                %(tmpName)s(...)
                after()
            end
            log.setLogLevel(log.WARNING)
        end""" % {'name' : name, 'tmpName' : tmpName})
        setFunc(before, after)


    def enableColoredLog(self):
        self.setColoredPrintFunc('log.__debug',    coloredBeforePrint(Fore.WHITE, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__info',     coloredBeforePrint(Fore.CYAN, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__warning',  coloredBeforePrint(Fore.YELLOW, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__error',    coloredBeforePrint(Fore.RED, Style.NORMAL), afterPrint)
        self.setColoredPrintFunc('log.__critical', coloredBeforePrint(Fore.RED, Style.BRIGHT), afterPrint)
