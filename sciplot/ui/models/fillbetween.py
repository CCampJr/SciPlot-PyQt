# -*- coding: utf-8 -*-
"""
This entire model is for fill-between type of plots, which actually uses
polycollections. In the future, this may become a polycollections model,
but for now K.I.S.S.

Created on Thu Jul  7 15:25:08 2016

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

from sciplot.utils.mplstyle import MplMarkers, MplLines
from sciplot.utils.general import round_list

from sciplot.ui.models.abstract import (AbstractTableModelMpl as
                                        _AbstractTableModelMpl,
                                        AbstractEditDelegateMpl as
                                        _AbstractEditDelegateMpl)

class TableModelFillBetween(_AbstractTableModelMpl):
    _HEADERS = ['Facecolor',
                'Alpha',
                'Edgecolor',
                'LineWidth',
                'Label',
                'Delete']

    _COL_FACECOLOR = _HEADERS.index('Facecolor')
    _COL_ALPHA = _HEADERS.index('Alpha')
    _COL_EDGECOLOR = _HEADERS.index('Edgecolor')
    _COL_LINEWIDTH = _HEADERS.index('LineWidth')
    _COL_LABEL = _HEADERS.index('Label')
    _COL_DELETE = _HEADERS.index('Delete')

    dataDeleted = _pyqtSignal(int, float)

    def __init__(self, parent=None):

        super(_QAbstractTableModel, self).__init__(parent)
        self.headers = TableModelFillBetween._HEADERS
        self._model_data = []

    def rowCount(self, parent=_QModelIndex()):
        """
        Return row count of table view
        """
        return len(self._model_data)

    def columnCount(self, parent=_QModelIndex()):
        """
        Return col count of table view
        """
        return len(self.headers)

    def headerData(self, col, orientation, role):
        """
        Basic horizontal header with no special role
        """
        if orientation == _Qt.Horizontal and role == _Qt.DisplayRole:
            return self.headers[col]
        return _QVariant()

    def doubleClickCheck(self, index):
        """
        Double-clicking certain columns has special effects. In this case,
        the color change columns and the delete column
        """
        col = index.column()
        if (col == TableModelFillBetween._COL_FACECOLOR or
                col == TableModelFillBetween._COL_EDGECOLOR):
            # Face- or EdgeColor
            self.changeColor(index)
        elif col == TableModelFillBetween._COL_DELETE:  # Delete?
            self.deleteData(index)

    def deleteData(self, index):
            self.setData(index, True)

    def changeColor(self, index):
        row = index.row()
        col = index.column()

        if col == TableModelFillBetween._COL_FACECOLOR:
            color = self._model_data[row]['facecolor']
        else:
            color = self._model_data[row]['edgecolor']

        # from [0,1] -> [0,255] color scale
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
            if col == TableModelFillBetween._COL_FACECOLOR:
                return str(round_list(self._model_data[row]['facecolor']))
            elif col == TableModelFillBetween._COL_ALPHA:
                return str(self._model_data[row]['alpha'])
            elif col == TableModelFillBetween._COL_EDGECOLOR:
                return str(round_list(self._model_data[row]['edgecolor']))
            elif col == TableModelFillBetween._COL_LINEWIDTH:
                return str(self._model_data[row]['linewidth'])
            elif col == TableModelFillBetween._COL_LABEL:
                return str(self._model_data[row]['label'])
            elif col == TableModelFillBetween._COL_DELETE:
                return ''
        elif role == _Qt.DecorationRole:
            if (col == TableModelFillBetween._COL_FACECOLOR or
                    col == TableModelFillBetween._COL_EDGECOLOR):
                if col == TableModelFillBetween._COL_FACECOLOR:
                    color = self._model_data[row]['facecolor']
                elif col == TableModelFillBetween._COL_EDGECOLOR:
                    color = self._model_data[row]['edgecolor']

                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
            elif col == TableModelFillBetween._COL_DELETE:
                color = [1, 0, 0]
                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
            else:
                return _QVariant()
        else:
            return _QVariant()

    def setData(self, index, value, role=_Qt.EditRole):
        if role == _Qt.EditRole:
            row = index.row()
            col = index.column()

            if col == TableModelFillBetween._COL_FACECOLOR:
                color_255 = value[0:-1]
                color = [round(color_255[0]/255, 2),
                         round(color_255[1]/255, 2),
                         round(color_255[2]/255, 2)]
                self._model_data[row]['facecolor'] = color
            elif col == TableModelFillBetween._COL_EDGECOLOR:
                color_255 = value[0:-1]
                color = [round(color_255[0]/255, 2),
                         round(color_255[1]/255, 2),
                         round(color_255[2]/255, 2)]
                self._model_data[row]['edgecolor'] = color
            elif col == TableModelFillBetween._COL_ALPHA:
                self._model_data[row]['alpha'] = float(value)
            elif col == TableModelFillBetween._COL_LINEWIDTH:
                self._model_data[row]['linewidth'] = float(value)
            elif col == TableModelFillBetween._COL_LABEL:
                self._model_data[row]['label'] = value
            elif col == TableModelFillBetween._COL_DELETE:
                if value:
                    out = self._model_data.pop(row)
                    self.layoutChanged.emit()
                    self.dataDeleted.emit(row, out['id'])

            self.dataChanged.emit(index, index)

    def flags(self, index):
            flag = super(_QAbstractTableModel, self).flags(index)
            return flag | _Qt.ItemIsEditable


class EditDelegateFillBetween(_AbstractEditDelegateMpl):
    def createEditor(self, parent, option, index):
            col = index.column()
            if (col == TableModelFillBetween._COL_FACECOLOR or
                    col == TableModelFillBetween._COL_EDGECOLOR):
                # Color handled by doubleClicked SIGNAL
                pass
            # LineWidth or Marker size or Alpha
            elif (col == TableModelFillBetween._COL_LINEWIDTH or
                  col == TableModelFillBetween._COL_ALPHA):
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(20)
                spinBoxSize.setSingleStep(.5)
                return spinBoxSize
            elif col == TableModelFillBetween._COL_LABEL:  # Label
                lineEditLabel = _QLineEdit(parent)
                return lineEditLabel
            elif col == TableModelFillBetween._COL_DELETE:  # Delete?
                pass
            else:
                return _QVariant()

    def setEditorData(self, editor, index):
        col = index.column()
        item = index.data(_Qt.DisplayRole)
        if (col == TableModelFillBetween._COL_FACECOLOR or
                col == TableModelFillBetween._COL_EDGECOLOR):
                # Color handled by doubleClicked SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelFillBetween._COL_LINEWIDTH or
              col == TableModelFillBetween._COL_ALPHA):
            item_float = float(item)
            editor.setValue(item_float)
        elif col == TableModelFillBetween._COL_LABEL:  # Label
            editor.setText(item)
        else:
            pass

    def setModelData(self, editor, model, index):
        col = index.column()
        if (col == TableModelFillBetween._COL_FACECOLOR or
                col == TableModelFillBetween._COL_EDGECOLOR):
                # Color handled by doubleClicked SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelFillBetween._COL_LINEWIDTH or
              col == TableModelFillBetween._COL_ALPHA):
            value = editor.value()
            model.setData(index, value)
        elif col == TableModelFillBetween._COL_LABEL:  # Label
            label = editor.text()
            model.setData(index, label)
