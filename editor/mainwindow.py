#!/usr/bin/python

import sys
import platform

import qdarkstyle
import PySide
from PySide.QtGui import QApplication, QMainWindow
from PySide import QtCore, QtGui

from ui_mainWindow import Ui_MainWindow as Ui
from moaiwidget import MOAIWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Store Ui() as class variable self.ui
        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        # Scroll view for moai gl widget
        # ui.scrollArea = QtGui.QScrollArea(ui.centralwidget)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(ui.scrollArea.sizePolicy().hasHeightForWidth())
        # ui.scrollArea.setSizePolicy(sizePolicy)
        # ui.scrollArea.setMinimumSize(QtCore.QSize(200, 200))
        # ui.scrollArea.setWidgetResizable(True)
        # ui.scrollArea.setObjectName("scrollArea")
        # ui.horizontalLayout.addWidget(ui.scrollArea)

        self.glWidget = MOAIWidget(ui.centralwidget)
        # ui.scrollArea.setWidget(self.glWidget)

        actionPropertyEditor = ui.propertyEditor.toggleViewAction()
        actionObjectPallete = ui.objectPallete.toggleViewAction()
        
        ui.menuWindow.addAction(actionPropertyEditor)
        ui.menuWindow.addAction(actionObjectPallete)

        intValidator = PySide.QtGui.QIntValidator()
        intValidator.setRange(128, 4096)
        ui.widthEdit.setValidator(intValidator)
        ui.heightEdit.setValidator(intValidator)
        ui.widthEdit.textEdited.connect(self.viewSizeEditingFinished)
        ui.heightEdit.textEdited.connect(self.viewSizeEditingFinished)

        glSize = self.glWidget.sizeHint()
        ui.widthEdit.setText(str(glSize.width()))
        ui.heightEdit.setText(str(glSize.height()))
    
    def viewSizeEditingFinished(self):
        width = int(self.ui.widthEdit.text())
        height = int(self.ui.heightEdit.text())
        
        self.resizeMoaiView(width, height)

    def resizeMoaiView(self, width, height):
        self.glWidget.resize(QtCore.QSize(width, height))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet())

    frame.show()
    app.exec_()




# print(lua.eval('python.eval(" 2 ** 2 ")') == 4)
# print(lua.eval('python.builtins.str(4)') == '4')