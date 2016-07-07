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
                             QSizePolicy as _QSizePolicy,
                             QTabWidget as _QTabWidget)

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

from sciplot.ui.models.fillbetween import (TableModelFillBetween as
                                               _TableModelFillBetween,
                                           EditDelegateFillBetween as
                                           _EditDelegateFillBetween)

from sciplot.data.lines import DataLine as _DataLine
from sciplot.data.special import DataFillBetween as _DataFillBetween

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')


class SciPlotUI(_QMainWindow):
    """
    Scientific plotting user-interface for creating publication-quality plots
    and images

    Methods
    -------
    plot : MPL-like plotting functionality

    updatePlotDataStyle : Make updates to plots (lines) when a stylistic \
    change is made within the model-table

    updatePlotDataDelete : Remove a plot when deleted from model-table

    refreshAllPlots : Delete all plots and re-plot
    """
    def __init__(self, parent=None):

        # Generic start to any pyQT program
        super(SciPlotUI, self).__init__(parent)
        self.ui = Ui_Plotter()
        self.ui.setupUi(self)
        self.setSizePolicy(_QSizePolicy.Expanding,
                           _QSizePolicy.Expanding)

        # This list will house objects containing all plot-data (i.e. the \
        # actual data and all elements that will be placed within models)
        self._plot_data = []

        # fill_between data-- similar to plot_data above
        self._fill_between_data = []

        # MPL plot widget
        self.mpl_widget = _MplCanvas(height=6, dpi=100)
        self.mpl_widget.axes.hold(True)

        # Insert MPL widget and toolbar
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget)
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget.toolbar)
        self.mpl_widget.draw()

        # Insert TabWidget
        self.ui.modelTabWidget = _QTabWidget()
        self.ui.verticalLayout.insertWidget(-1, self.ui.modelTabWidget)

        # Initial  and insert table view for line plots
        self.tableViewLine = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewLine, 'Lines')

        # Initial and insert table view for fill_between plots
        self.tableViewFillBetween = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewFillBetween,
                                      'Fill Between')

        # Set model and delegates
        # Lines
        self.modelLine = _TableModelLines()
        self.delegateLine = _EditDelegateLines()
        self.tableViewLine.setModel(self.modelLine)
        self.tableViewLine.setItemDelegate(self.delegateLine)
        self.tableViewLine.show()

        # Fill Betweeb
        self.modelFillBetween = _TableModelFillBetween()
        self.delegateFillBetween = _EditDelegateFillBetween()
        self.tableViewFillBetween.setModel(self.modelFillBetween)
        self.tableViewFillBetween.setItemDelegate(self.delegateFillBetween)
        self.tableViewFillBetween.show()

        # Signals & Slots

        # Lines
        # Make use of double-clicking within table
        self.tableViewLine.doubleClicked.connect(
            self.modelLine.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelLine.dataChanged.connect(self.updatePlotDataStyle)
        self.modelLine.dataDeleted.connect(self.updatePlotDataDelete)

        # Fill Between
        # Make use of double-clicking within table
        self.tableViewFillBetween.doubleClicked.connect(
            self.modelFillBetween.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelFillBetween.dataChanged.connect(self.updateFillBetweenDataStyle)
        self.modelFillBetween.dataDeleted.connect(self.updateFillBetweenDataDelete)


    def plot(self, x, y, label=None, x_units=None, y_units=None, **kwargs):
        """
        MPL-like plotting functionality

        Parameters
        ----------
        x : ndarray (1D)
            X-axis data

        y : ndarray (1D, for now)
            Y-axis data

        label : str
            Label of plot

        x_units : str
            X-axis label (units)

        y_units : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-plot

        """

        # Temporary plot-data
        plot_data = _DataLine()
        plot_data.x = x
        plot_data.y = y
        plot_data.label = label
        plot_data.units['x_units'] = x_units
        plot_data.units['y_units'] = y_units

        # Plot outputs a line object
        line_out = self.mpl_widget.axes.plot(x, y, label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')
        self.mpl_widget.axes.set_xlabel(plot_data.units['x_units'])
        self.mpl_widget.axes.set_ylabel(plot_data.units['y_units'])
        self.mpl_widget.fig.tight_layout()

        # Since the plot was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        plot_data.retrieve_style_from_line(line_out[0])

        # Append this specific plot data to out list of all plots
        self._plot_data.append(plot_data)

        # Update model
        self.modelLine._model_data.append(plot_data.model_style)
        self.modelLine.layoutChanged.emit()

    def updatePlotDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the plot data
        """
        for num, style_info in enumerate(self.modelLine._model_data):
            self._plot_data[num].model_style = style_info
        self.refreshAllPlots()

    def updatePlotDataDelete(self, row):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        self._plot_data.pop(row)
        self.refreshAllPlots()

    def refreshAllPlots(self):
        """
        Clear and re-plot all plot data of all types
        """

        # Clear axis -- in the future, maybe clear figure and recreate axis
        self.mpl_widget.axes.clear()

        # Check to see if any plots even are remaining (maybe all were deleted)
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

        if len(self._fill_between_data) > 0:
            self.mpl_widget.axes.hold(True)
            for itm in self._fill_between_data:
                self.mpl_widget.axes.fill_between(itm.x, itm.y_low, itm.y_high,
                                                  label=itm.label,
                                                  facecolor=itm.style_dict['facecolor'],
                                                  edgecolor=itm.style_dict['edgecolor'],
                                                  alpha=itm.style_dict['alpha'],
                                                  linewidth=itm.style_dict['linewidth'])

            self.mpl_widget.axes.legend(loc='best')

        self.mpl_widget.draw()

    def fill_between(self, x, y_low, y_high, label=None, x_units=None,
                     y_units=None, **kwargs):
        """
        MPL-like fill_between plotting functionality

        Parameters
        ----------
        x : ndarray (1D)
            X-axis data

        y_low : ndarray (1D, for now)
            Low Y-axis data

        y_high : ndarray (1D, for now)
            High Y-axis data

        label : str
            Label of plot

        x_units : str
            X-axis label (units)

        y_units : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-fill_between

        """

        # Temporary fill_between-data
        fill_between_data = _DataFillBetween()
        fill_between_data.x = x
        fill_between_data.y_low = y_low
        fill_between_data.y_high = y_high
        fill_between_data.label = label
        fill_between_data.units['x_units'] = x_units
        fill_between_data.units['y_units'] = y_units

        # Fill between outputs a polycollection
        pc_out = self.mpl_widget.axes.fill_between(x, y_low, y_high,
                                                   label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')
        self.mpl_widget.axes.set_xlabel(fill_between_data.units['x_units'])
        self.mpl_widget.axes.set_ylabel(fill_between_data.units['y_units'])
        self.mpl_widget.fig.tight_layout()

        # Since the fill_between was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        fill_between_data.retrieve_style_from_polycollection(pc_out)

        # Append this specific plot data to out list of all plots
        self._fill_between_data.append(fill_between_data)

        # Update model
        self.modelFillBetween._model_data.append(fill_between_data.model_style)
        self.modelFillBetween.layoutChanged.emit()

    def updateFillBetweenDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelFillBetween._model_data):
            self._fill_between_data[num].model_style = style_info
        self.refreshAllPlots()

    def updateFillBetweenDataDelete(self, row):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        self._fill_between_data.pop(row)
        self.refreshAllPlots()


if __name__ == '__main__':

    app = _QApplication(_sys.argv)

    winPlotter = SciPlotUI()

    x = _np.arange(100)
    y = x**2

    winPlotter.plot(x, y, label='Test1')
    winPlotter.plot(x, y**1.1, label='Test2')
    winPlotter.fill_between(x, y-1000, y+1000, label='Test3')
    winPlotter.show()



#    print('Here: {}'.format(winPlotter._data.spectra_list[0].meta_dict['label']))
    _sys.exit(app.exec_())