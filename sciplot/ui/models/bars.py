# -*- coding: utf-8 -*-
"""

ModelViewDelegate for an MPL Line object

Created on Thu Jul  7 10:01:23 2016

@author: chc
"""

from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QMainWindow as _QMainWindow,
                             QColorDialog as _QColorDialog,
                             QDoubleSpinBox as _QDoubleSpinBox,
                             QComboBox as _QComboBox,
                             QLineEdit as _QLineEdit,
                             QStyledItemDelegate as _QStyledItemDelegate,
                             QTableView as _QTableView,
                             QSizePolicy as _QSizePolicy)

from PyQt5.QtCore import (QAbstractTableModel as _QAbstractTableModel,
                          QVariant as _QVariant,
                          QObject as _QObject,
                          pyqtSignal as _pyqtSignal,
                          QModelIndex as _QModelIndex,
                          Qt as _Qt)

from PyQt5.QtGui import (QPixmap as _QPixmap,
                         QIcon as _QIcon,
                         QColor as _QColor)


from sciplot.ui.models.abstract import (AbstractTableModelMpl as
                                        _AbstractTableModelMpl,
                                        AbstractEditDelegateMpl as
                                        _AbstractEditDelegateMpl)

class TableModelBars(_AbstractTableModelMpl):
    _HEADERS = ['Facecolor',
                'Alpha',
                'Edgecolor',
                'Line Width',
                'Width Factor',
                'Label',
                'Delete']

    _COL_FACECOLOR = _HEADERS.index('Facecolor')
    _COL_ALPHA = _HEADERS.index('Alpha')
    _COL_EDGECOLOR = _HEADERS.index('Edgecolor')
    _COL_LINEWIDTH = _HEADERS.index('Line Width')
    _COL_WIDTH_FACTOR = _HEADERS.index('Width Factor')
    _COL_LABEL = _HEADERS.index('Label')
    _COL_DELETE = _HEADERS.index('Delete')

    dataDeleted = _pyqtSignal(int)

    def __init__(self, parent=None):

        super(_QAbstractTableModel, self).__init__(parent)
        self.headers = TableModelBars._HEADERS
        self._model_data = []

    def rowCount(self, parent=_QModelIndex()):
            return len(self._model_data)

    def columnCount(self, parent=_QModelIndex()):
        return len(self.headers)

    def headerData(self, col, orientation, role):
        if orientation == _Qt.Horizontal and role == _Qt.DisplayRole:
            return self.headers[col]
        return _QVariant()

    def doubleClickCheck(self, index):
        col = index.column()
        if (col == TableModelBars._COL_FACECOLOR or
                col == TableModelBars._COL_EDGECOLOR):  # Colors
            self.changeColor(index)
        elif col == TableModelBars._COL_DELETE:  # Delete?
            self.deleteData(index)

    def deleteData(self, index):
            self.setData(index, True)

    def changeColor(self, index):
        row = index.row()
        col = index.column()

        if col == TableModelBars._COL_FACECOLOR:
            color = self._model_data[row]['facecolor']
        elif col == TableModelBars._COL_EDGECOLOR:
            color = self._model_data[row]['edgecolor']
        color_256 = [color[0]*255, color[1]*255, color[2]*255]
        qcolor = _QColor(color_256[0], color_256[1], color_256[2])

        result = _QColorDialog.getColor(qcolor)
        if _QColor.isValid(result):
            self.setData(index, result.getRgb())
        else:
            return None

    def data(self, index, role=_Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return _QVariant()

        row = index.row()
        col = index.column()

        if role == _Qt.DisplayRole:
            if col == TableModelBars._COL_FACECOLOR:
                return str(self._model_data[row]['facecolor'])
            elif col == TableModelBars._COL_ALPHA:
                return str(self._model_data[row]['alpha'])
            elif col == TableModelBars._COL_EDGECOLOR:
                return str(self._model_data[row]['edgecolor'])
            elif col == TableModelBars._COL_LINEWIDTH:
                return str(self._model_data[row]['linewidth'])
            elif col == TableModelBars._COL_WIDTH_FACTOR:
                return str(self._model_data[row]['width_factor'])
            elif col == TableModelBars._COL_LABEL:
                return str(self._model_data[row]['label'])
            elif col == TableModelBars._COL_DELETE:
                return ''
        elif role == _Qt.DecorationRole:
            if col == TableModelBars._COL_FACECOLOR:
                color = self._model_data[row]['facecolor']
            elif col == TableModelBars._COL_EDGECOLOR:
                color = self._model_data[row]['edgecolor']
            if (col == TableModelBars._COL_FACECOLOR or
                    col == TableModelBars._COL_EDGECOLOR):
                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
            elif col == TableModelBars._COL_DELETE:
                color = [1, 0, 0]
                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
            else:
                pass
        else:
            return _QVariant()

    def setData(self, index, value, role=_Qt.EditRole):
        if role == _Qt.EditRole:
            row = index.row()
            col = index.column()

            if (col == TableModelBars._COL_FACECOLOR or
                    col == TableModelBars._COL_EDGECOLOR):
                color_255 = value[0:-1]
                color = [round(color_255[0]/255, 2),
                         round(color_255[1]/255, 2),
                         round(color_255[2]/255, 2)]
                if col == TableModelBars._COL_FACECOLOR:
                    self._model_data[row]['facecolor'] = color
                if col == TableModelBars._COL_EDGECOLOR:
                    self._model_data[row]['edgecolor'] = color
            elif col == TableModelBars._COL_ALPHA:
                self._model_data[row]['alpha'] = float(value)
            elif col == TableModelBars._COL_LINEWIDTH:
                self._model_data[row]['linewidth'] = float(value)
            elif col == TableModelBars._COL_WIDTH_FACTOR:
                self._model_data[row]['width_factor'] = float(value)
            elif col == TableModelBars._COL_LABEL:
                self._model_data[row]['label'] = value
            elif col == TableModelBars._COL_DELETE:
                if value:
                    self._model_data.pop(row)
                    self.layoutChanged.emit()
                    self.dataDeleted.emit(row)

            self.dataChanged.emit(index, index)

    def flags(self, index):
            flag = super(_QAbstractTableModel, self).flags(index)
            return flag | _Qt.ItemIsEditable


class EditDelegateBars(_AbstractEditDelegateMpl):
    def createEditor(self, parent, option, index):
            col = index.column()
            if col == TableModelBars._COL_FACECOLOR:
                # Color handled by doubleClicked SIGNAL
                pass
            elif col == TableModelBars._COL_EDGECOLOR:
                # Color handled by doubleClicked SIGNAL
                pass
            # Alpha
            elif col == TableModelBars._COL_ALPHA:
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(1)
                spinBoxSize.setSingleStep(.1)
                return spinBoxSize
            # Width Fraction
            elif col == TableModelBars._COL_WIDTH_FACTOR:
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(1000000000)
                spinBoxSize.setSingleStep(.1)
                return spinBoxSize

            # LineWidth
            elif col == TableModelBars._COL_LINEWIDTH:
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(20)
                spinBoxSize.setSingleStep(.5)
                return spinBoxSize
            elif col == TableModelBars._COL_LABEL:  # Label
                lineEditLabel = _QLineEdit(parent)
                return lineEditLabel
            elif col == TableModelBars._COL_DELETE:  # Delete?
                pass
            else:
                return _QVariant()

    def setEditorData(self, editor, index):
        col = index.column()
        item = index.data(_Qt.DisplayRole)
        if (col == TableModelBars._COL_FACECOLOR or
                col == TableModelBars._COL_EDGECOLOR):
            # Color handled by doubleClick SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelBars._COL_LINEWIDTH or
              col == TableModelBars._COL_ALPHA or
              col == TableModelBars._COL_WIDTH_FACTOR):
            item_float = float(item)
            editor.setValue(item_float)
        elif col == TableModelBars._COL_LABEL:  # Label
            editor.setText(item)
        else:
            pass

    def setModelData(self, editor, model, index):
        col = index.column()
        if col == TableModelBars._COL_FACECOLOR:
            # Color handled by doubleClick SIGNAL
            pass
        elif col == TableModelBars._COL_EDGECOLOR:
            # Color handled by doubleClick SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelBars._COL_LINEWIDTH or
              col == TableModelBars._COL_ALPHA or
              col == TableModelBars._COL_WIDTH_FACTOR):
            value = editor.value()
            model.setData(index, value)
        elif col == TableModelBars._COL_LABEL:  # Label
            label = editor.text()
            model.setData(index, label)
