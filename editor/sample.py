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
        'group' : 'Emitter',
        'items' : [
            {'id':1, 'name':'Frequency', 'type':'float', 'value':1.0},
            {'id':2, 'name':'Emission', 'type':'float', 'value':1.0},
        ]
    },
    {
        'group' : 'Forces',
        'items' : [
            {'id':3, 'name':'Type', 'type':'list', 'value':0, 'choices':['radial', 'linear']},
            {'id':4, 'name':'Loc X', 'type':'float', 'value':0.0},
            {'id':5, 'name':'Loc Y', 'type':'float', 'value':0.0},
        ]
    },
    {
        'group' : 'State',
        'items' : [
            {'id':6, 'name':'Frequency', 'type':'float', 'value':1.0},
            {'id':7, 'name':'Emission', 'type':'float', 'value':1.0},
        ]
    }
]

app = QApplication([])
win = MyWindow(items)
win.show()
app.exec_()

