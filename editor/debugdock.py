import sys, os, types
import PySide
import re

from PySide.QtCore import QSettings
from PySide import QtCore, QtGui
from PySide.QtGui import QDockWidget, QColor, QColorDialog, QPixmap

from debugdock_ui import Ui_debugdock as Ui

import luainterface

MOAIDebugDrawStyles = [
    'partitionCells',
    'partitionPaddedCells',
    'propModelBounds',
    'propWorldBounds',
    'textBox',
    'textBoxBaselines',
    'textBoxLayout'
]

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
 
def camelToUpperSnake(s):
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).upper()

def upperFirstLetter(s):
    return s[0].upper() + s[1:]

class DebugDock(QDockWidget):
    def __init__(self, parent=None):
        super(DebugDock, self).__init__(parent)
        # Store Ui() as class variable self.ui
        self.createSlots()

        ui = Ui()
        self.ui =  ui
        self.ui.setupUi(self)

        floatValidator = PySide.QtGui.QDoubleValidator()
        floatValidator.setRange(0.0, 100.0)
        ui.partitionCellsWidth.setValidator(floatValidator)
        ui.partitionPaddedCellsWidth.setValidator(floatValidator)
        ui.propModelBoundsWidth.setValidator(floatValidator)
        ui.propWorldBoundsWidth.setValidator(floatValidator)
        ui.textBoxWidth.setValidator(floatValidator)
        ui.textBoxBaselinesWidth.setValidator(floatValidator)
        ui.textBoxLayoutWidth.setValidator(floatValidator)

        self.mainWindow = self.parent()
        self.createColors()

    def createColors(self):
        for style in MOAIDebugDrawStyles:
            colorBtn = getattr(self.ui, style + "Color")
            colorBtn.color = QColor(255, 255, 255, 255)
            pixmap = QPixmap(16, 16)
            pixmap.fill(colorBtn.color)

            colorBtn.pixmap = pixmap
            colorBtn.setIcon(pixmap)
            colorBtn.setAutoFillBackground(False)
            colorBtn.setIconSize(QtCore.QSize(16, 16))
            def setColor(self, color):
                self.pixmap.fill(color)
                self.setIcon(self.pixmap)
                self.color = color

            colorBtn.setColor = types.MethodType(setColor, colorBtn)


    def readSettings(self):
        settings = QSettings()

        ui = self.ui
        for style in MOAIDebugDrawStyles:
            checkBox = getattr(ui, style)
            widthEdit = getattr(ui, style + "Width")
            colorBtn = getattr(ui, style + "Color")

            checkBox.setChecked ( bool(settings.value( "debug/" + style + 'DrawEnabled', False )) )
            widthEdit.setText ( str(settings.value( "debug/" + style + 'Width', '1' )) )
            colorBtn.setColor ( settings.value( "debug/" + style + 'Color', QColor(255, 255, 255, 255) ))

        ui.histogram.setChecked ( bool(settings.value( "debug/histogramEnabled", False )) )
        ui.allocLog.setChecked ( bool(settings.value( "debug/allocTrackingEnabled", False )) )
        ui.reportHistogram_btn.setEnabled( ui.histogram.isChecked() )

    def writeSettings(self):
        settings = QSettings()

        ui = self.ui
        for style in MOAIDebugDrawStyles:
            checkBox = getattr(ui, style)
            widthEdit = getattr(ui, style + "Width")
            colorBtn = getattr(ui, style + "Color")

            settings.setValue("debug/" + style + "DrawEnabled", checkBox.isChecked())
            settings.setValue("debug/" + style + "Width", widthEdit.text())
            settings.setValue("debug/" + style + "Color", colorBtn.color)

        settings.setValue ( "debug/histogramEnabled", ui.histogram.isChecked() )
        settings.setValue ( "debug/allocTrackingEnabled", ui.allocLog.isChecked() )

    def createSlots(self):
        for style in MOAIDebugDrawStyles:
            @QtCore.Slot(bool)
            def toggle(flag, style = style):
                self.toggleStyle(style, flag)

            @QtCore.Slot(str)
            def setWidth(width, style = style):
                self.setWidth(style, width)

            @QtCore.Slot()
            def pickColor(style = style):
                self.pickColor(style)

            setattr(self, 'toggle' + upperFirstLetter(style), toggle)
            setattr(self, 'setWidth' + upperFirstLetter(style), setWidth)
            setattr(self, 'pickColor' + upperFirstLetter(style), pickColor)

    @QtCore.Slot(bool)
    def toggleLuaAllocLogEnabled(self, flag):
        self.mainWindow.moaiWidget.runString("MOAISim.setLuaAllocLogEnabled( %s )" % ('true' if flag else 'false'))

    @QtCore.Slot(bool)
    def toggleHistogramEnabled(self, flag):
        self.mainWindow.moaiWidget.runString("MOAISim.setHistogramEnabled( %s )" % ('true' if flag else 'false'))

    @QtCore.Slot()
    def forceGC(self):
        self.mainWindow.moaiWidget.runString("MOAISim.forceGC()")

    @QtCore.Slot()
    def reportHistogram(self):
        self.mainWindow.moaiWidget.runString("MOAISim.reportHistogram()")


    def toggleStyle(self, styleName, flag):
        self.updateDebugDrawValues(styleName)

    def setWidth(self, styleName, width):
        self.updateDebugDrawValues(styleName)

    def pickColor(self, styleName):
        colorBtn = getattr(self.ui, styleName + "Color")
        color = QColorDialog().getColor(colorBtn.color, self, styleName + " Color", QColorDialog.ShowAlphaChannel)

        if color.isValid():
            colorBtn.setColor(color)
            self.updateDebugDrawValues(styleName)

    def updateDebugDrawValues(self, style):
        ui = self.ui
        luaCmd = ""
        checkBox = getattr(ui, style)
        widthEdit = getattr(ui, style + "Width")
        colorBtn = getattr(ui, style + "Color")

        moaiName = camelToUpperSnake(style)
        enabled = bool(checkBox.isChecked())
        width = float(widthEdit.text())
        color = [float(x)/255.0 for x in colorBtn.color.getRgb()]

        showStyle = "MOAIDebugLines.showStyle ( MOAIDebugLines.%s, %s )" % (moaiName, 'true' if enabled else 'false')
        setStyle = "MOAIDebugLines.setStyle ( MOAIDebugLines.%s, %s, %s, %s, %s, %s )" % (moaiName, width, color[0], color[1], color[2], color[3])
        luaCmd += "%s \n%s \n" % (setStyle, showStyle)

        self.mainWindow.moaiWidget.runString(luaCmd)

    def updateAllDebugValues(self):
        ui = self.ui
        luaCmd = ""
        for style in MOAIDebugDrawStyles:
            checkBox = getattr(ui, style)
            widthEdit = getattr(ui, style + "Width")
            colorBtn = getattr(ui, style + "Color")

            moaiName = camelToUpperSnake(style)
            enabled = bool(checkBox.isChecked())
            width = float(widthEdit.text())
            color = [float(x)/255.0 for x in colorBtn.color.getRgb()]

            showStyle = "MOAIDebugLines.showStyle ( MOAIDebugLines.%s, %s )" % (moaiName, 'true' if enabled else 'false')
            setStyle = "MOAIDebugLines.setStyle ( MOAIDebugLines.%s, %s, %s, %s, %s, %s )" % (moaiName, width, color[0], color[1], color[2], color[3])
            luaCmd += "%s \n%s \n" % (setStyle, showStyle)

        luaCmd += "MOAISim.setHistogramEnabled( %s ) \n" % ('true' if ui.histogram.isChecked() else 'false')
        luaCmd += "MOAISim.setLuaAllocLogEnabled( %s ) \n" % ('true' if ui.allocLog.isChecked() else 'false')
        print(luaCmd)
        self.mainWindow.moaiWidget.runString(luaCmd)


