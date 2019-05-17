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
                             QSizePolicy as _QSizePolicy,
                             QHBoxLayout as _QHBoxLayout)

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

class TableModelLines(_AbstractTableModelMpl):
    """
    
    Signals
    -------
    dataSeleted : int, int
        Row, id of plot
    """
    _HEADERS = ['Color',
                'Alpha',
                'LineWidth',
                'LineStyle',
                'Marker',
                'Marker Size',
                'Label',
                'Delete']

    _COL_COLOR = _HEADERS.index('Color')
    _COL_ALPHA = _HEADERS.index('Alpha')
    _COL_LINEWIDTH = _HEADERS.index('LineWidth')
    _COL_LINESTYLE = _HEADERS.index('LineStyle')
    _COL_MARKER = _HEADERS.index('Marker')
    _COL_MARKERSIZE = _HEADERS.index('Marker Size')
    _COL_LABEL = _HEADERS.index('Label')
    _COL_DELETE = _HEADERS.index('Delete')
#    _COL_ID = _HEADERS.index('ID')

    dataDeleted = _pyqtSignal(int, float)

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
        if col == TableModelLines._COL_COLOR:  # Color
            self.changeColor(index)
        elif col == TableModelLines._COL_DELETE:  # Delete?
            self.deleteData(index)

    def deleteData(self, index):
            self.setData(index, True)

    def changeColor(self, index):
        row = index.row()
        color = self._model_data[row]['color']
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
            if col == TableModelLines._COL_COLOR:
                return str(round_list(self._model_data[row]['color']))
            elif col == TableModelLines._COL_ALPHA:
                return str(self._model_data[row]['alpha'])
            elif col == TableModelLines._COL_LINEWIDTH:
                return str(self._model_data[row]['linewidth'])
            elif col == TableModelLines._COL_LINESTYLE:
                ls = self._model_data[row]['linestyle']
                return str(MplLines.LINESTYLE_DICT[ls])
            elif col == TableModelLines._COL_MARKER:
                mk = self._model_data[row]['marker']
                return str(MplMarkers.MARKER_DICT[mk])
            elif col == TableModelLines._COL_MARKERSIZE:
                return str(self._model_data[row]['markersize'])
            elif col == TableModelLines._COL_LABEL:
                return str(self._model_data[row]['label'])
            elif col == TableModelLines._COL_DELETE:
                return ''

        elif role == _Qt.DecorationRole:
            if col == TableModelLines._COL_COLOR:
                color = self._model_data[row]['color']
                color_256 = [color[0]*255, color[1]*255, color[2]*255]
                qcolor = _QColor(color_256[0], color_256[1], color_256[2])
                pm = _QPixmap(20, 20)
                pm.fill(qcolor)
                icon = _QIcon(pm)
                return icon
            elif col == TableModelLines._COL_DELETE:
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

            if col == TableModelLines._COL_COLOR:
                color_255 = value[0:-1]
                color = [round(color_255[0]/255, 2),
                         round(color_255[1]/255, 2),
                         round(color_255[2]/255, 2)]
                self._model_data[row]['color'] = color
#                self.colorChanged.emit(row)
            elif col == TableModelLines._COL_ALPHA:
                self._model_data[row]['alpha'] = float(value)
            elif col == TableModelLines._COL_LINEWIDTH:
                self._model_data[row]['linewidth'] = float(value)
            elif col == TableModelLines._COL_LINESTYLE:
                self._model_data[row]['linestyle'] = value
            elif col == TableModelLines._COL_MARKER:
                self._model_data[row]['marker'] = value
            elif col == TableModelLines._COL_MARKERSIZE:
                self._model_data[row]['markersize'] = float(value)
            elif col == TableModelLines._COL_LABEL:
                self._model_data[row]['label'] = value
            elif col == TableModelLines._COL_DELETE:
                if value:
                    out = self._model_data.pop(row)
                    self.layoutChanged.emit()
                    self.dataDeleted.emit(row, out['id'])

            self.dataChanged.emit(index, index)

    def flags(self, index):
            flag = super(_QAbstractTableModel, self).flags(index)
            return flag | _Qt.ItemIsEditable


class EditDelegateLines(_AbstractEditDelegateMpl):
    def createEditor(self, parent, option, index):
            col = index.column()
            if col == TableModelLines._COL_COLOR:
                # Color handled by doubleClicked SIGNAL
                pass
            # LineWidth or Marker size or Alpha
            elif (col == TableModelLines._COL_LINEWIDTH or
                  col == TableModelLines._COL_ALPHA or
                  col == TableModelLines._COL_MARKERSIZE):
                spinBoxSize = _QDoubleSpinBox(parent)
                spinBoxSize.setMinimum(0)
                spinBoxSize.setMaximum(20)
                spinBoxSize.setSingleStep(.5)
                return spinBoxSize
            elif col == TableModelLines._COL_LINESTYLE:  # LineStyle
                comboBoxLineStyle = _QComboBox(parent)
                for line_style in MplLines.LINESTYLE_DESC:
                    comboBoxLineStyle.addItem(line_style)
                return comboBoxLineStyle
            elif col == TableModelLines._COL_MARKER:  # Marker
                comboBoxMarker = _QComboBox(parent)
                for marker_style in MplMarkers.MARKER_DESC:
                    comboBoxMarker.addItem(marker_style)
                return comboBoxMarker
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
        if col == TableModelLines._COL_COLOR:
            # Color handled by doubleClick SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelLines._COL_LINEWIDTH or
              col == TableModelLines._COL_ALPHA or
              col == TableModelLines._COL_MARKERSIZE):
            item_float = float(item)
            editor.setValue(item_float)
        elif col == TableModelLines._COL_LINESTYLE:  # LineStyle
            style_index = MplLines.index(item)
            editor.setCurrentIndex(style_index)
        elif col == TableModelLines._COL_MARKER:  # Marker
            style_index = MplMarkers.index(item)
            editor.setCurrentIndex(style_index)
        elif col == TableModelLines._COL_LABEL:  # Label
            editor.setText(item)
        else:
            pass

    def setModelData(self, editor, model, index):
        col = index.column()
        if col == TableModelLines._COL_COLOR:
            # Color handled by doubleClick SIGNAL
            pass
        # LineWidth or MarkerSize or Alpha
        elif (col == TableModelLines._COL_LINEWIDTH or
              col == TableModelLines._COL_ALPHA or
              col == TableModelLines._COL_MARKERSIZE):
            value = editor.value()
            model.setData(index, value)
        elif col == TableModelLines._COL_LINESTYLE:  # LineStyle
            style_index = editor.currentIndex()
            style = MplLines.LINESTYLE_SYMBOL[style_index]
            model.setData(index, style)
        elif col == TableModelLines._COL_MARKER:  # Marker
            style_index = editor.currentIndex()
            style = MplMarkers.MARKER_SYMBOL[style_index]
            model.setData(index, style)
        elif col == TableModelLines._COL_LABEL:  # Label
            label = editor.text()
            model.setData(index, label)
