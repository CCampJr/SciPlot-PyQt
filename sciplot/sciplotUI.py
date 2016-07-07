# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 22:37:39 2016

@author: chc
"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../'))

import numpy as _np

# Generic imports for QT-based programs
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
                          QModelIndex as _QModelIndex,
                          QVariant as _QVariant,
                          Qt as _Qt,
                          pyqtSignal as _pyqtSignal,
                          QObject as _QObject)

from PyQt5.QtGui import (QPixmap as _QPixmap,
                         QIcon as _QIcon,
                         QColor as _QColor)

# Import from Designer-based GUI
from sciplot.ui.qt_Plotter import Ui_MainWindow as Ui_Plotter
from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas
from sciplot.utils.mplstyle import MplStyleSheets, MplMarkers, MplLines
from sciplot.ui.models.lines import (TableModelLines as _TableModelLines,
                                     EditDelegateLines as _EditDelegateLines)

from sciplot.data.lines import DataLine as _DataLine
# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')


class SciPlotUI(_QMainWindow):
    def __init__(self, parent=None):
        super(SciPlotUI, self).__init__(parent)
        self.ui = Ui_Plotter()
        self.ui.setupUi(self)

        self._plot_data = []

        self.mpl_widget = _MplCanvas(height=6, dpi=100)
        self.mpl_widget.axes.hold(True)
        self.setSizePolicy(_QSizePolicy.Expanding,
                           _QSizePolicy.Expanding)

        self.ui.verticalLayout.insertWidget(0, self.mpl_widget)
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget.toolbar)

        self.tableViewLine = _QTableView()

        self.ui.verticalLayout.insertWidget(-1, self.tableViewLine)

        self.modelLine = _TableModelLines()
        self.delegateLine = _EditDelegateLines()
    #
        self.tableViewLine.setModel(self.modelLine)
        self.tableViewLine.setItemDelegate(self.delegateLine)
        self.tableViewLine.show()

        self.tableViewLine.doubleClicked.connect(
            self.modelLine.doubleClickCheck)

        self.modelLine.dataChanged.connect(self.updatePlotDataStyle)
        self.modelLine.dataDeleted.connect(self.updatePlotDataDelete)

        self.mpl_widget.draw()

    def plot(self, x, y, label=None, x_units=None, y_units=None, **kwargs):
        plot_data = _DataLine()
        plot_data.x = x
        plot_data.y = y
        plot_data.label = label
        plot_data.units['x_units'] = x_units
        plot_data.units['y_units'] = y_units

        line_out = self.mpl_widget.axes.plot(x, y, label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')
        self.mpl_widget.axes.set_xlabel(plot_data.units['x_units'])
        self.mpl_widget.axes.set_ylabel(plot_data.units['y_units'])
        self.mpl_widget.fig.tight_layout()

        plot_data.retrieve_style_from_line(line_out[0])
        self._plot_data.append(plot_data)

        self.modelLine._model_data.append(plot_data.model_style)
        self.modelLine.layoutChanged.emit()

    def updatePlotDataStyle(self):
        for num, style_info in enumerate(self.modelLine._model_data):
            self._plot_data[num].model_style = style_info
        self.refreshPlots()

    def updatePlotDataDelete(self, row):
        self._plot_data.pop(row)
        self.refreshPlots()

    def refreshPlots(self):
        self.mpl_widget.axes.clear()
        if len(self._plot_data) > 0:
            self.mpl_widget.axes.hold(True)
            for itm in self._plot_data:
                self.mpl_widget.axes.plot(itm.x, itm.y, label=itm.label,
                                          color=itm.style_dict['color'],
                                          alpha=itm.style_dict['alpha'],
                                          linewidth=itm.style_dict['linewidth'],
                                          linestyle=itm.style_dict['linestyle'],
                                          marker=itm.style_dict['marker'],
                                          markersize=itm.style_dict['markersize'])

            self.mpl_widget.axes.legend(loc='best')

        self.mpl_widget.draw()

if __name__ == '__main__':

    app = _QApplication(_sys.argv)

    winPlotter = SciPlotUI()

    x = _np.arange(100)
    y = x**2

    winPlotter.plot(x, y, label='Test1')
    winPlotter.plot(x, y**1.1, label='Test2')
    winPlotter.show()



#    print('Here: {}'.format(winPlotter._data.spectra_list[0].meta_dict['label']))
    _sys.exit(app.exec_())