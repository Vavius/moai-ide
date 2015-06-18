import PySide

from PySide import QtCore, QtGui
from PySide.QtCore import QAbstractTableModel, Qt


class ComboDelegate(QtGui.QStyledItemDelegate):
    IndexRole = Qt.UserRole + 1

    def __init__(self, parent):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        if index.data(ComboDelegate.IndexRole) is None:
            return super(ComboDelegate, self).createEditor(parent, option, index)

        data = index.data(Qt.EditRole)
        combo = QtGui.QComboBox(parent)
        combo.addItems(data)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return combo
        
    def setEditorData(self, editor, index):
        idx = index.data(ComboDelegate.IndexRole)
        if idx is None:
            return super(ComboDelegate, self).setEditorData(editor, index)

        editor.blockSignals(True)
        editor.setCurrentIndex(int(idx))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        if index.data(ComboDelegate.IndexRole) is None:
            return super(ComboDelegate, self).setModelData(editor, model, index)

        model.setData(index, editor.currentIndex())
        
    @QtCore.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class TreeItem(object):
    def __init__(self, model, parent=None):
        self.parentItem = parent
        self.itemData = list(range(0, 2))
        self.setModel(model)
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return 2

    def data(self, column, role=Qt.DisplayRole):
        if column < 0 or column > len(self.itemData):
            return None

        if self.model.get('type') == 'list':
            if role == Qt.EditRole:
                return self.model.get('choices')
            if column == 1:
                if role == ComboDelegate.IndexRole:
                    return self.itemData[column]
                if role == Qt.DisplayRole:
                    return self.model.get('choices')[self.itemData[column]]

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.itemData[column]

        return None
        
    def editable(self, column):
        if column == 1 and self.model.get('type') != 'header':
            return True
        return False

    def insertChildren(self, position, count):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            item = TreeItem({}, self)
            self.childItems.insert(position, item)

        return True

    def insertChild(self, position, data):
        if position < 0 or position > len(self.childItems):
            return False

        item = TreeItem(data, self)
        self.childItems.insert(position, item)
        return item

    def parent(self):
        return self.parentItem

    def removeAllChildren(self):
        self.removeChildren(0, self.childCount())

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def setData(self, column, data):
        if column < 0 or column > len(self.itemData):
            return False

        self.itemData[column] = data
        return True

    def setModel(self, model):
        self.model = model
        self.itemData[0] = model.get('name')
        self.itemData[1] = model.get('value')


class PropertyItemModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(PropertyItemModel, self).__init__(parent)
        self.rootItem = TreeItem({'type' : 'header', 'name' : 'Property', 'value' : 'Value'})

    def buddy(self, index):
        row = index.row()
        col = index.column()
        if col == 0:
            return index.sibling(row, 1)
        else:
            return index

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self.getItem(index)

        # if role == Qt.BackgroundRole:
            # return item.color(index.row(), index.column())

        return item.data(index.column(), role)

    def flags(self, index):
        if not index.isValid():
            return 0

        item = self.getItem(index)
        if item.editable(index.column()):
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows, self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, rowCount())

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setModelData(self, data):
        self.beginResetModel()
        self.rootItem.removeAllChildren()

        columns = self.rootItem.columnCount()
        parent = self.rootItem
        self.items = {}

        for group in data:
            section = parent.insertChild(parent.childCount(), {'type' : 'header', 'name' : group['group']})
            for item in group['items']:
                child = section.insertChild(section.childCount(), item)
                self.items[item['id']] = child

        self.endResetModel()
