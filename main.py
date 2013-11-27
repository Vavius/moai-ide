#!/usr/bin/python
 
# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *
 

# # Create a Qt application
# app = QApplication(sys.argv)

# # Create a Label and show it
# label = QLabel("Hello World")
# label.show()

# # Enter Qt application main loop
# app.exec_()
# sys.exit()


# lupa test
import lupa
from lupa import LuaRuntime

lua = LuaRuntime()

print(lua.eval('1+1'))

lua_func = lua.eval('function(f, n) return f(n) end')

def py_add1(n): 
    return n+1

print(lua_func(py_add1, 2))


print(lua.eval('python.eval(" 2 ** 2 ")') == 4)
print(lua.eval('python.builtins.str(4)') == '4')
