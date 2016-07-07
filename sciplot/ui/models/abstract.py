# -*- coding: utf-8 -*-
"""

Abstract ModelViewDelegate for MPL objects

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


class AbstractTableModelMpl(_QAbstractTableModel, _QObject):

    def rowCount(self, parent=_QModelIndex()):
        return len(self._model_data)

    def columnCount(self, parent=_QModelIndex()):
        return len(self.headers)

    def headerData(self, col, orientation, role):
        if orientation == _Qt.Horizontal and role == _Qt.DisplayRole:
            return self.headers[col]
        return _QVariant()

    def doubleClickCheck(self, index):
        raise NotImplementedError

    def deleteData(self, index):
            self.setData(index, True)

    def data(self, index, role=_Qt.DisplayRole):
        raise NotImplementedError

    def setData(self, index, value, role=_Qt.EditRole):
        raise NotImplementedError

    def flags(self, index):
            flag = super(_QAbstractTableModel, self).flags(index)
            return flag | _Qt.ItemIsEditable


class AbstractEditDelegateMpl(_QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        raise NotImplementedError

    def setEditorData(self, editor, index):
        raise NotImplementedError

    def setModelData(self, editor, model, index):
        raise NotImplementedError
