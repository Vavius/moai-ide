''' ps_QAbstractTableModel_solvents.py
use PySide's QTableView and QAbstractTableModel for tabular data
sort columns by clicking on the header title

here applied to solvents commonly used in Chemistry

PySide is the official LGPL-licensed version of PyQT
tested with PySide112 and Python27/Python33 by vegaseat  15feb2013
'''

import operator
from PySide.QtCore import *
from PySide.QtGui import *
from widgets.propertyitemmodel import PropertyItemModel, ComboDelegate


class MyWindow(QWidget):
    def __init__(self, items, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 570, 450)

        tree_model = PropertyItemModel(self)
        tree_model.setModelData(items)
        
        tree_view = QTreeView()

        tree_view.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        tree_view.setAlternatingRowColors(True)
        tree_view.setIndentation(20)
        tree_view.setTabKeyNavigation(True)

        tree_view.setModel(tree_model)

        self.itemDelegate = ComboDelegate(self)
        tree_view.setItemDelegate(self.itemDelegate)

        # set font
        # font = QFont("Courier New", 14)
        # tree_view.setFont(font)
        # set column width to fit contents (set font first!)
        # tree_view.resizeColumnsToContents()
        # enable sorting
        # tree_view.setSortingEnabled(True)

        layout = QVBoxLayout(self)
        layout.addWidget(tree_view)
        self.setLayout(layout)

items = [
    {
        'group' : 'State',
        'items' : [
            { 'type' : "string", 'name' : "Name", 'value' : "state", 'id' : "Name" },
            { 'type' : "float", 'name' : "Damping", 'value' : 0, 'id' : "Damping" },
            { 'type' : "float", 'name' : "Mass min", 'value' : 1, 'id' : "MassMin" },
            { 'type' : "float", 'name' : "Mass max", 'value' : 1, 'id' : "MassMax" },
            { 'type' : "float", 'name' : "Lifetime min", 'value' : 1, 'id' : "TermMin" },
            { 'type' : "float", 'name' : "Lifetime max", 'value' : 1, 'id' : "TermMax" },

        ]
    },
    {
        'group' : 'Force1',
        'items' : [

            { 'type' : "string",  'name' : "Name", 'value' : "Force1", 'id' : "Name" },
            { 'type' : "list",    'name' : "Type", 'value' : 0, 'id' : "Type", 'choices' : ['Force', 'Gravity', 'Offset'] },
            { 'type' : "list",    'name' : "Shape", 'value' : 0, 'id' : "Shape", 'choices' : ['Attractor', 'Basin', 'Linear', 'Radial'] },
            { 'type' : "float",   'name' : "Loc X", 'value' : 0, 'id' : "LocX" },
            { 'type' : "float",   'name' : "Loc Y", 'value' : 0, 'id' : "LocY" },

            { 'type' : "float",   "name" : "Radius", "value" : 0, 'id' : "Radius" },
            { 'type' : "float",   "name" : "Magnitude", "value" : 0, 'id' : "Magnitude" },
        ]
    },
    {
        'group' : 'Force2',
        'items' : [

            { 'type' : "string",  'name' : "Name", 'value' : "Force2", 'id' : "Name" },
            { 'type' : "list",    'name' : "Type", 'value' : 0, 'id' : "Type", 'choices' : ['Force', 'Gravity', 'Offset'] },
            { 'type' : "list",    'name' : "Shape", 'value' : 2, 'id' : "Shape", 'choices' : ['Attractor', 'Basin', 'Linear', 'Radial'] },
            { 'type' : "float",   'name' : "Loc X", 'value' : 0, 'id' : "LocX" },
            { 'type' : "float",   'name' : "Loc Y", 'value' : 0, 'id' : "LocY" },

            { 'type' : "float",   'name' : "Mag X", 'value' : 0, 'id' : "MagX" },
            { 'type' : "float",   'name' : "Mag Y", 'value' : 0, 'id' : "MagY" },
        ]
    },
]

app = QApplication([])
win = MyWindow(items)
win.show()
app.exec_()

