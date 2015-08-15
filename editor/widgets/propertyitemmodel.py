import PySide, math

from PySide import QtCore, QtGui
from PySide.QtCore import QAbstractTableModel, Qt

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

class ComboDelegate(QtGui.QStyledItemDelegate):
    IndexRole = Qt.UserRole + 1
    ValidatorRole = Qt.UserRole + 2

    def __init__(self, parent):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        if index.data(ComboDelegate.IndexRole) is None:
            # add validation for spinbox widgets
            validRange = index.data(ComboDelegate.ValidatorRole)
            widget = super(ComboDelegate, self).createEditor(parent, option, index)

            if validRange:
                if hasattr(widget, 'setMinimum') and 'min' in validRange:
                    widget.setMinimum(validRange['min'])
                if hasattr(widget, 'setMaximum') and 'max' in validRange:
                    widget.setMaximum(validRange['max'])

            # remove blue focus border
            widget.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)
            return widget

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
    
    def updateEditorGeometry(self, editor, option, index):
        minHeight = 20
        rect = option.rect
        offset = 0.5 * (minHeight - rect.height())
        editor.setGeometry(rect.left(), rect.top() - offset, rect.width(), minHeight)

    @QtCore.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class TreeItem(object):
    def __init__(self, model, parent=None):
        self.parentItem = parent
        self.itemData = list(range(0, 2))
        self.setModel(model)
        self.childItems = []
        self.smoothSwitch = 0

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

        if role == ComboDelegate.ValidatorRole:
            return self.model.get('range')

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

    def getId(self):
        return self.id

    def getValue(self):
        return self.itemData[1]

    def getValueAfterIncrement(self, diff):
        model = self.model
        if model['type'] == 'float':
            return self.validate ( self.itemData[1] + diff )

        if model['type'] == 'int':
            self.smoothSwitch += diff
            if abs(self.smoothSwitch) > 1:
                res = self.itemData[1] + int(math.copysign(1, self.smoothSwitch))
                self.smoothSwitch = 0
                return self.validate(res)

        if model['type'] == 'list':
            self.smoothSwitch += diff
            if abs(self.smoothSwitch) > 1:
                res = self.itemData[1] + int(math.copysign(1, self.smoothSwitch))
                total = len(model['choices'])
                self.smoothSwitch = 0
                return max(min(res, total - 1), 0)

        if model['type'] == 'bool':
            self.smoothSwitch += diff
            if abs(self.smoothSwitch) > 1:
                res = self.smoothSwitch > 0
                self.smoothSwitch = 0
                return res

        return None

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
        self.id = model.get('id')
        
        value = model.get('value')
        if model['type'] == 'int':
            self.itemData[1] = int(value)
        
        elif model['type'] == 'float':
            self.itemData[1] = float(value)

        elif model['type'] == 'bool':
            self.itemData[1] = bool(value)

        elif model['type'] in ('string', 'header'):
            self.itemData[1] = str(value)
        
        elif model['type'] == 'list':
            model['choices'] = model['choices'] or list()
            # convert lua 1-based dict to array
            if 0 not in model['choices']:
                l = list()
                for k in sorted(model['choices']):
                    l.append(model['choices'][k])
                model['choices'] = l

            self.itemData[1] = int(value)

        else:
            self.itemData[1] = value

    def validate(self, val):
        validRange = self.model.get('range')
        result = val
        if validRange:
            if 'min' in validRange:
                result = max(result, validRange['min'])
            if 'max' in validRange:
                result = min(result, validRange['max'])
        return result


class PropertyItemModel(QtCore.QAbstractItemModel):
    itemDataChanged = QtCore.Signal(object, object)

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

    def applyOffset(self, index, offset):
        if not index.isValid(): return

        # index must point to value
        if index.column() != 1:
            index = index.sibling(index.row(), 1)

        item = self.getItem(index)
        val = item.getValueAfterIncrement(offset)
        if val is not None:
            self.setData(index, val)

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
            # SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            # QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)"), index, index)
            # self.dataChanged.emit(index)
            # self.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            self.dataChanged.emit(index, index)
            self.itemDataChanged.emit(item.getId(), item.getValue())

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

        if data:
            for i, group in data.items():
                section = parent.insertChild(parent.childCount(), {'type' : 'header', 'name' : group['group'], 'value' : ''})
                for j, item in group['items'].items():
                    child = section.insertChild(section.childCount(), item)
                    self.items[item['id']] = child

        self.endResetModel()
