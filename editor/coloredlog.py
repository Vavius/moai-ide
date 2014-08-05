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
        setFunc = self.lua.eval("""function(before, after) 
            _%(name)s = %(name)s
            %(name)s = function(...)
                before()
                _%(name)s(...)
                after()
            end
        end""" % {'name' : name})
        setFunc(before, after)


    def enableColoredLog(self):
        setColoredPrintFunc('log.debug',    coloredBeforePrint(Fore.WHITE, Style.NORMAL), afterPrint)
        setColoredPrintFunc('log.info',     coloredBeforePrint(Fore.CYAN, Style.NORMAL), afterPrint)
        setColoredPrintFunc('log.warning',  coloredBeforePrint(Fore.YELLOW, Style.NORMAL), afterPrint)
        setColoredPrintFunc('log.error',    coloredBeforePrint(Fore.RED, Style.NORMAL), afterPrint)
        setColoredPrintFunc('log.critical', coloredBeforePrint(Fore.RED, Style.BRIGHT), afterPrint)
