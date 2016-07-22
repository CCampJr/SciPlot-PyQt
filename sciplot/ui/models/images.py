# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:11:40 2016

@author: chc
"""

import matplotlib as _mpl

from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QMainWindow as _QMainWindow,
                             QColorDialog as _QColorDialog,
                             QCheckBox as _QCheckBox,
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
                'Colorbar',
                'Delete']

    _COL_CMAP = _HEADERS.index('Cmap')
    _COL_ALPHA = _HEADERS.index('Alpha')
    _COL_CLIM_LOW = _HEADERS.index('Clim Low')
    _COL_CLIM_HIGH = _HEADERS.index('Clim High')
    _COL_CBAR = _HEADERS.index('Colorbar')
    _COL_LABEL = _HEADERS.index('Label')
    _COL_DELETE = _HEADERS.index('Delete')

    dataDeleted = _pyqtSignal(int)

    def __init__(self, parent=None):

        super(_QAbstractTableModel, self).__init__(parent)
        self.headers = TableModelImages._HEADERS
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
#        if col == TableModelImages._COL_CMAP:  # CMAP
#            self.changeColor(index)
        if col == TableModelImages._COL_DELETE:  # Delete?
            self.deleteData(index)

    def deleteData(self, index):
            self.setData(index, True)

    def data(self, index, role=_Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return _QVariant()

        row = index.row()
        col = index.column()

        if role == _Qt.DisplayRole:
            if col == TableModelImages._COL_CMAP:
                return str(self._model_data[row]['cmap_name'])
            elif col == TableModelImages._COL_ALPHA:
                return str(self._model_data[row]['alpha'])
            elif col == TableModelImages._COL_CLIM_LOW:
                return str(self._model_data[row]['clim_low'])
            elif col == TableModelImages._COL_CLIM_HIGH:
                return str(self._model_data[row]['clim_high'])
            elif col == TableModelImages._COL_CBAR:
#                print('1')
                return str(self._model_data[row]['colorbar'])
            elif col == TableModelImages._COL_LABEL:
                return str(self._model_data[row]['label'])
            elif col == TableModelImages._COL_DELETE:
                return ''
        elif role == _Qt.DecorationRole:
            if col == TableModelImages._COL_DELETE:
                color = [1, 0, 0]
                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
        else:
            return _QVariant()

    def setData(self, index, value, role=_Qt.EditRole):
        if role == _Qt.EditRole:
            row = index.row()
            col = index.column()

            if col == TableModelImages._COL_CMAP:
                self._model_data[row]['cmap_name'] = value
            elif col == TableModelImages._COL_ALPHA:
                self._model_data[row]['alpha'] = float(value)
            elif col == TableModelImages._COL_CLIM_LOW:
                self._model_data[row]['clim_low'] = float(value)
            elif col == TableModelImages._COL_CLIM_HIGH:
                self._model_data[row]['clim_high'] = float(value)
            elif col == TableModelImages._COL_CBAR:
#                print('2')
                self._model_data[row]['colorbar'] = bool(value)
            elif col == TableModelImages._COL_LABEL:
                self._model_data[row]['label'] = value
            elif col == TableModelImages._COL_DELETE:
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

            if col == TableModelImages._COL_ALPHA:
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(1)
                spinBoxSize.setSingleStep(.1)
                return spinBoxSize
            # clim_low, clim_high
            elif (col == TableModelImages._COL_CLIM_LOW or
                  col == TableModelImages._COL_CLIM_HIGH):
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(-1e10)
                spinBoxSize.setMaximum(1e10)
                spinBoxSize.setSingleStep(.5)
                return spinBoxSize
            elif col == TableModelImages._COL_CBAR:  # colorbar
#                print('3')
                comboBoxTrueFalse = _QComboBox(parent)
                comboBoxTrueFalse.addItems(['True','False'])
                return comboBoxTrueFalse
            elif col == TableModelImages._COL_CMAP:  # cmaps
                comboBoxCmapNames = _QComboBox(parent)
                list_cmaps = list(_mpl.cm.cmap_d.keys())
                list_cmaps.sort()
                for cmap_name in list_cmaps:
                    comboBoxCmapNames.addItem(cmap_name)
                return comboBoxCmapNames
            elif col == TableModelImages._COL_LABEL:  # Label
                lineEditLabel = _QLineEdit(parent)
                return lineEditLabel
            elif col == TableModelImages._COL_DELETE:  # Delete?
                pass
            else:
                return _QVariant()

    def setEditorData(self, editor, index):
        col = index.column()
        item = index.data(_Qt.DisplayRole)
        if (col == TableModelImages._COL_ALPHA or
              col == TableModelImages._COL_CLIM_LOW or
              col == TableModelImages._COL_CLIM_HIGH):
            item_float = float(item)
            editor.setValue(item_float)
        elif col == TableModelImages._COL_LABEL:  # Label
            editor.setText(item)
        elif (col == TableModelImages._COL_CBAR or
              col == TableModelImages._COL_CMAP): # colorbar or cmap
            loc = editor.findText(item)
            if loc < 0:
                loc = 0
            editor.setCurrentIndex(loc)
        else:
            pass

    def setModelData(self, editor, model, index):
        col = index.column()

        # Alpha or clim's
        if (col == TableModelImages._COL_ALPHA or
                col == TableModelImages._COL_CLIM_LOW or
                col == TableModelImages._COL_CLIM_HIGH):
            value = editor.value()
            model.setData(index, value)
        elif col == TableModelImages._COL_CMAP:  # cmap
            list_cmaps = list(_mpl.cm.cmap_d.keys())
            list_cmaps.sort()
            idx = editor.currentIndex()
            cmap_name = list_cmaps[idx]
            model.setData(index, cmap_name)
        elif col == TableModelImages._COL_CBAR:  # Colorbar
#            print('5')
            cbar = editor.currentText() == 'True'
            model.setData(index, cbar)
        elif col == TableModelImages._COL_LABEL:  # Label
            label = editor.text()
            model.setData(index, label)
