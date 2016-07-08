# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:11:40 2016

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

from sciplot.ui.models.abstract import (AbstractTableModelMpl as
                                        _AbstractTableModelMpl,
                                        AbstractEditDelegateMpl as
                                        _AbstractEditDelegateMpl)

class TableModelImages(_AbstractTableModelMpl):
    _HEADERS = ['Cmap',
                'Alpha',
                'Clim Low',
                'Clim High',
                'Label',
                'Delete']

    _COL_CMAP = _HEADERS.index('Cmap')
    _COL_ALPHA = _HEADERS.index('Alpha')
    _COL_CLIM_LOW = _HEADERS.index('Clim Low')
    _COL_CLIM_HIGH = _HEADERS.index('Clim High')
    _COL_LABEL = _HEADERS.index('Label')
    _COL_DELETE = _HEADERS.index('Delete')

    dataDeleted = _pyqtSignal(int)

    def __init__(self, parent=None):

        super(_QAbstractTableModel, self).__init__(parent)
        self.headers = TableModelLines._HEADERS
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
#        if col == TableModelLines._COL_CMAP:  # CMAP
#            self.changeColor(index)
        if col == TableModelLines._COL_DELETE:  # Delete?
            self.deleteData(index)

    def deleteData(self, index):
            self.setData(index, True)

#    def changeColor(self, index):
#        row = index.row()
#        color = self._model_data[row]['color']
#        color_256 = [color[0]*255, color[1]*255, color[2]*255]
#        qcolor = _QColor(color_256[0], color_256[1], color_256[2])
#
#        result = _QColorDialog.getColor(qcolor)
#        if _QColor.isValid(result):
#            self.setData(index, result.getRgb())
#        else:
#            return None

    def data(self, index, role=_Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return _QVariant()

        row = index.row()
        col = index.column()

        if role == _Qt.DisplayRole:
            if col == TableModelLines._COL_CMAP:
                return str(self._model_data[row]['cmap_name'])
            elif col == TableModelLines._COL_ALPHA:
                return str(self._model_data[row]['alpha'])
            elif col == TableModelLines._COL_CMAP_LOW:
                return str(self._model_data[row]['cmap_low'])
            elif col == TableModelLines._COL_CMAP_HIGH:
                return str(self._model_data[row]['cmap_high'])
            elif col == TableModelLines._COL_LABEL:
                return str(self._model_data[row]['label'])
            elif col == TableModelLines._COL_DELETE:
                return '<Dbl-Click to Delete>'
        elif role == _Qt.DecorationRole:
            pass
        else:
            return _QVariant()

    def setData(self, index, value, role=_Qt.EditRole):
        if role == _Qt.EditRole:
            row = index.row()
            col = index.column()

            if col == TableModelLines._COL_CMAP:
                self._model_data[row]['cmap_name'] = value
            elif col == TableModelLines._COL_ALPHA:
                self._model_data[row]['alpha'] = float(value)
            elif col == TableModelLines._COL_CMAP_LOW:
                self._model_data[row]['cmap_low'] = float(value)
            elif col == TableModelLines._COL_CMAP_HIGH:
                self._model_data[row]['smap_high'] = float(value)
            elif col == TableModelLines._COL_LABEL:
                self._model_data[row]['label'] = value
            elif col == TableModelLines._COL_DELETE:
                if value:
                    self._model_data.pop(row)
                    self.layoutChanged.emit()
                    self.dataDeleted.emit(row)

            self.dataChanged.emit(index, index)

    def flags(self, index):
            flag = super(_QAbstractTableModel, self).flags(index)
            return flag | _Qt.ItemIsEditable


class EditDelegateImages(_AbstractEditDelegateMpl):
    def createEditor(self, parent, option, index):
            col = index.column()

            if col == TableModelLines._COL_ALPHA:
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(1)
                spinBoxSize.setSingleStep(.1)
                return spinBoxSize
            # cmap_low, cmap_high
            elif (col == TableModelLines._COL_CMAP_LOW or
                  col == TableModelLines._COL_SMAP_HIGH):
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(-1e10)
                spinBoxSize.setMaximum(1e10)
                spinBoxSize.setSingleStep(.5)
                return spinBoxSize
            elif col == TableModelLines._COL_CMAP:  # cmaps
                comboBoxCmapNames = _QComboBox(parent)
                list_cmaps = _mpl.cm.cmap_d.keys()
                list_cmaps.sort()
                for cmap_name in list_cmaps:
                    comboBoxCmapNames.addItem(cmap_name)
                return comboBoxCmapNames
            elif col == TableModelLines._COL_LABEL:  # Label
                lineEditLabel = _QLineEdit(parent)
                return lineEditLabel
            elif col == TableModelLines._COL_DELETE:  # Delete?
                pass
            else:
                return _QVariant()

    def setEditorData(self, editor, index):
        col = index.column()
        item = index.data(_Qt.DisplayRole)
        if (col == TableModelLines._COL_ALPHA or
              col == TableModelLines._COL_CMAP_LOW or
              col == TableModelLines._COL_CMAP_HIGH):
            item_float = float(item)
            editor.setValue(item_float)
        elif col == TableModelLines._COL_LABEL:  # Label
            editor.setText(item)
        else:
            pass

    def setModelData(self, editor, model, index):
        col = index.column()

        # Alpha or clim's
        if (col == TableModelLines._COL_ALPHA or
                col == TableModelLines._COL_CMAP_LOW or
                col == TableModelLines._COL_CMAP_HIGH):
            value = editor.value()
            model.setData(index, value)
        elif col == TableModelLines._COL_CMAP:  # cmap
            list_cmaps = _mpl.cm.cmap_d.keys()
            list_cmaps.sort()
            idx = editor.currentIndex()
            cmap_name = list_cmaps[idx]
            model.setData(index, cmap_name)
        elif col == TableModelLines._COL_LABEL:  # Label
            label = editor.text()
            model.setData(index, label)
