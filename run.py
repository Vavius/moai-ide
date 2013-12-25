#!/usr/bin/python
 
import sys
from PySide.QtGui import QMainWindow, QPushButton, QApplication 
from ui_quitter import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()





# # moaipy
# from moaipy import *

# AKUCreateContext()
# AKUInitializeSim()


# moaiLuaState = AKUGetLuaState()

# # lupa test
# import lupa
# from lupa import LuaRuntime

# lua = LuaRuntime(luastate = moaiLuaState)

# # prop = lua.eval('''MOAIProp.new()''')




# print(lua.eval('python.eval(" 2 ** 2 ")') == 4)
# print(lua.eval('python.builtins.str(4)') == '4')
