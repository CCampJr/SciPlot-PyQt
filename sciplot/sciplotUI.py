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

from sciplot.ui.models.images import (TableModelImages as _TableModelImages,
                                     EditDelegateImages as _EditDelegateImages)

from sciplot.ui.models.bars import (TableModelBars as _TableModelBars,
                                     EditDelegateBars as _EditDelegateBars)

from sciplot.data.generic import DataGlobal as _DataGlobal
from sciplot.data.lines import DataLine as _DataLine
from sciplot.data.images import DataImages as _DataImages
from sciplot.data.bars import DataBar as _DataBar
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

        # Global "data" i.e., title, x-label, y-label, etc
        self._global_data = _DataGlobal()

        # This list will house objects containing all plot-data (i.e. the \
        # actual data and all elements that will be placed within models)
        self._plot_data = []

        # fill_between data-- similar to plot_data above
        self._fill_between_data = []

        # images data-- similar to plot_data above
        self._images_data = []

        # bar data-- similar to plot_data above
        self._bar_data = []

        # MPL plot widget
        self.mpl_widget = _MplCanvas(height=6, dpi=100)
        self.mpl_widget.axes.hold(True)


        # Insert MPL widget and toolbar
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget)
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget.toolbar)
        self.updateAxisParameters()
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

        # Initial  and insert table view for images
        self.tableViewImages = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewImages, 'Images')

        # Initial  and insert table view for bars
        self.tableViewBars = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewBars, 'Bars')

        # Set model and delegates
        # Lines
        self.modelLine = _TableModelLines()
        self.delegateLine = _EditDelegateLines()
        self.tableViewLine.setModel(self.modelLine)
        self.tableViewLine.setItemDelegate(self.delegateLine)
        self.tableViewLine.show()

        # Fill Between
        self.modelFillBetween = _TableModelFillBetween()
        self.delegateFillBetween = _EditDelegateFillBetween()
        self.tableViewFillBetween.setModel(self.modelFillBetween)
        self.tableViewFillBetween.setItemDelegate(self.delegateFillBetween)
        self.tableViewFillBetween.show()

        # Images
        self.modelImages = _TableModelImages()
        self.delegateImages = _EditDelegateImages()
        self.tableViewImages.setModel(self.modelImages)
        self.tableViewImages.setItemDelegate(self.delegateImages)
        self.tableViewImages.show()

        # Bars/Bars
        self.modelBars = _TableModelBars()
        self.delegateBars = _EditDelegateBars()
        self.tableViewBars.setModel(self.modelBars)
        self.tableViewBars.setItemDelegate(self.delegateBars)
        self.tableViewBars.show()

        # Signals & Slots

        # Global labels
        self.ui.lineEditTitle.editingFinished.connect(self.updateLabelsFromLineEdit)
        self.ui.lineEditXLabel.editingFinished.connect(self.updateLabelsFromLineEdit)
        self.ui.lineEditYLabel.editingFinished.connect(self.updateLabelsFromLineEdit)

        # Non-tracked (not saved) properties
        self.ui.comboBoxAspect.currentIndexChanged.connect(self.axisAspect)
        self.ui.comboBoxAxisScaling.currentIndexChanged.connect(self.axisScaling)
        self.ui.checkBoxAxisVisible.stateChanged.connect(self.axisVisible)
        self.ui.lineEditXLimMin.editingFinished.connect(self.axisLimits)
        self.ui.lineEditXLimMax.editingFinished.connect(self.axisLimits)
        self.ui.lineEditYLimMin.editingFinished.connect(self.axisLimits)
        self.ui.lineEditYLimMax.editingFinished.connect(self.axisLimits)

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

        # Images
        # Make use of double-clicking within table
        self.tableViewImages.doubleClicked.connect(
            self.modelImages.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelImages.dataChanged.connect(self.updateImagesDataStyle)
        self.modelImages.dataDeleted.connect(self.updateImagesDataDelete)

        # Bars
        # Make use of double-clicking within table
        self.tableViewBars.doubleClicked.connect(
            self.modelBars.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelBars.dataChanged.connect(self.updateBarsDataStyle)
        self.modelBars.dataDeleted.connect(self.updateBarsDataDelete)

    def plot(self, x, y, label=None, x_label=None, y_label=None, **kwargs):
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

        x_label : str
            X-axis label (units)

        y_label : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-plot

        """

        # Temporary plot-data
        plot_data = _DataLine()
        plot_data.x = x
        plot_data.y = y
        plot_data.label = label

        # Plot outputs a line object
        line_out = self.mpl_widget.axes.plot(x, y, label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()


        # Since the plot was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        plot_data.retrieve_style_from_line(line_out[0])

        # Append this specific plot data to out list of all plots
        self._plot_data.append(plot_data)

        # Update model
        self.modelLine._model_data.append(plot_data.model_style)
        self.modelLine.layoutChanged.emit()

    def updateMplLabels(self, x_label=None, y_label=None, title=None):
        """
        Within the MPL widget, update the x- and y-labels and the title
        """
        if x_label is not None:
            self.mpl_widget.axes.set_xlabel(x_label)

        if y_label is not None:
            self.mpl_widget.axes.set_ylabel(y_label)

        if title is not None:
            self.mpl_widget.axes.set_title(title)
        self.mpl_widget.fig.tight_layout()
        self.mpl_widget.draw()

    def updateDataLabels(self, x_label=None, y_label=None, title=None):
        """
        Within the global data container, update the x- and y-labels and the \
        title
        """
        if x_label is not None:
            self._global_data.labels['x_label'] = x_label

        if y_label is not None:
            self._global_data.labels['y_label'] = y_label

        if title is not None:
            self._global_data.labels['title'] = title

    def updateLineEditLabels(self, x_label=None, y_label=None, title=None):
        """
        Within the pyQT lineEdit widgets, update the x- and y-labels and the \
        title
        """
        if x_label is not None:
            self.ui.lineEditXLabel.setText(x_label)

        if y_label is not None:
            self.ui.lineEditYLabel.setText(y_label)

        if title is not None:
            self.ui.lineEditTitle.setText(title)

    def updateAllLabels(self, x_label=None, y_label=None, title=None):
        """
        Update the x- and y-labels and the title in the MPL widget, the \
        lineEdit boxes, and the global data container
        """
        self.updateMplLabels(x_label=x_label, y_label=y_label, title=title)
        self.updateDataLabels(x_label=x_label, y_label=y_label, title=title)
        self.updateLineEditLabels(x_label=x_label, y_label=y_label,
                                  title=title)

    def updateLabelsFromLineEdit(self):
        """
        From the linEdit widgets, update the x- and y-labels and the title \
        in the MPL widget and the global data container
        """
        title = None
        x_label = None
        y_label = None

        sender = self.sender()
        if sender == self.ui.lineEditTitle:
            title = self.ui.lineEditTitle.text()
        elif sender == self.ui.lineEditXLabel:
            x_label = self.ui.lineEditXLabel.text()
        elif sender == self.ui.lineEditYLabel:
            y_label = self.ui.lineEditYLabel.text()
        self.updateDataLabels(x_label=x_label, y_label=y_label, title=title)
        self.updateMplLabels(x_label=x_label, y_label=y_label, title=title)

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

        # Images
        # Check to see if any images even remain (maybe all were deleted)
        if len(self._images_data) > 0:
            self.mpl_widget.axes.hold(True)
            for itm in self._images_data:
                self.mpl_widget.axes.imshow(itm.img, label=itm.label,
                                            interpolation='none',
                                            origin='lower',
                                            cmap=_mpl.cm.cmap_d[itm.style_dict['cmap_name']],
                                            alpha=itm.style_dict['alpha'],
                                            clim=itm.style_dict['clim'])

        # Bars
        # Check to see if any images even remain (maybe all were deleted)
        if len(self._bar_data) > 0:
            self.mpl_widget.axes.hold(True)
            for itm in self._bar_data:
                self.mpl_widget.axes.bar(itm._left, itm.y, width=itm._width,
                                         label=itm.label,
                                         facecolor=itm.style_dict['facecolor'],
                                         alpha=itm.style_dict['alpha'],
                                         edgecolor=itm.style_dict['edgecolor'],
                                         linewidth=itm.style_dict['linewidth'])
        # Lines
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

        # Fill between
        # Check to see if any plots even are remaining (maybe all were deleted)
        if len(self._fill_between_data) > 0:
            self.mpl_widget.axes.hold(True)
            for itm in self._fill_between_data:
                self.mpl_widget.axes.fill_between(itm.x, itm.y_low, itm.y_high,
                                                  label=itm.label,
                                                  facecolor=itm.style_dict['facecolor'],
                                                  edgecolor=itm.style_dict['edgecolor'],
                                                  alpha=itm.style_dict['alpha'],
                                                  linewidth=itm.style_dict['linewidth'])

        # Only add a legend if a plot exists
        if len(self._fill_between_data) + len(self._plot_data) + \
                len(self._bar_data) > 0:
            self.mpl_widget.axes.legend(loc='best')

        # Apply x- and y-labels and a title if they are set
        if self._global_data.labels['title'] is not None:
            self.mpl_widget.axes.set_title(self._global_data.labels['title'])
        if self._global_data.labels['x_label'] is not None:
            self.mpl_widget.axes.set_xlabel(self._global_data.labels['x_label'])
        if self._global_data.labels['y_label'] is not None:
            self.mpl_widget.axes.set_ylabel(self._global_data.labels['y_label'])

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def fill_between(self, x, y_low, y_high, label=None, x_label=None,
                     y_label=None, **kwargs):
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

        x_label : str
            X-axis label (units)

        y_label : str
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

        # Fill between outputs a polycollection
        pc_out = self.mpl_widget.axes.fill_between(x, y_low, y_high,
                                                   label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

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

    def imshow(self, img, x=None, y=None, label=None,
               x_label=None, y_label=None, **kwargs):
        """
        MPL-like plotting functionality

        Parameters
        ----------
        img : ndarray (2D)
            Image data

        x : ndarray (1D)
            X-axis data

        y : ndarray (1D, for now)
            Y-axis data

        label : str
            Label of plot

        x_label : str
            X-axis label (units)

        y_label : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-imshow

        """

        # Temporary plot-data
        image_data = _DataImages()
        image_data.img = img
        image_data.x = x
        image_data.y = y
        image_data.label = label

        # Imshow outputs an image object
        image_out = self.mpl_widget.axes.imshow(img, interpolation='None',
                                                origin='lower',
                                                label=label,
                                                **kwargs)
#        self.mpl_widget.axes.legend(loc='best')

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

        # Since the image was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup cmap, etc.
        # Thus, we plot, then retrieve what the style info was
        image_data.retrieve_style_from_image(image_out)

        # Append this specific plot data to out list of all plots
        self._images_data.append(image_data)

        # Update model
        self.modelImages._model_data.append(image_data.model_style)
        self.modelImages.layoutChanged.emit()


    def updateImagesDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelImages._model_data):
            self._images_data[num].model_style = style_info
        self.refreshAllPlots()

    def updateImagesDataDelete(self, row):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        self._images_data.pop(row)
        self.refreshAllPlots()


    def bar(self, x, y, width_fraction=1.0, label=None, x_label=None,
            y_label=None, **kwargs):
        """
        MPL-like plotting functionality

        Note
        ----
        Unlike MPL bar, this method uses centered data. Thus, x is the center \
        position of the bar

        Parameters
        ----------
        x : ndarray (1D)
            X-axis data (center of bars)

        y : ndarray (1D, for now)
            Y-axis data

        width_fraction: float
            Fraction of space between bars taken up by bar (e.g. 1.0 leads to \
            bars that tough)

        label : str
            Label of plot

        x_label : str
            X-axis label (units)

        y_label : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-plot

        """

        # Temporary plot-data
        bar_data = _DataBar()
        bar_data.x = x
        bar_data.y = y
        bar_data.label = label

        bar_data._gap = _np.abs(x[1]-x[0])

        bar_data.style_dict['width_fraction']=width_fraction

        bar_data._width = bar_data._gap*bar_data.style_dict['width_fraction']
        bar_data._left = bar_data.x - bar_data._width/2

        # Plot outputs a list of patch objects
        bar_out = self.mpl_widget.axes.bar(bar_data._left, y,
                                           width = bar_data._width,
                                           label=label, **kwargs)
        self.mpl_widget.axes.legend(loc='best')

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()


        # Since the plot was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        bar_data.retrieve_style_from_bar(bar_out[0])

        # Append this specific plot data to out list of all plots
        self._bar_data.append(bar_data)
        # Update model
        self.modelBars._model_data.append(bar_data.model_style)
        self.modelBars.layoutChanged.emit()

    def hist(self, data, bins=10, label=None, x_label=None,
             y_label='Counts', **kwargs):
        """
        MPL-like histogram plotting

        Parameters
        ----------
        data : ndarray (1D, for now)
            Data (center of bars)

        bins : int
            Number of histogram bins

        label : str
            Label of plot

        x_label : str
            X-axis label (units)

        y_label : str
            Y-axis label (units)

        kwargs : dict
            Other parameters sent directly to mpl-plot

        """
        counts, lefts = _np.histogram(data, bins=bins)
        gap = _np.abs(lefts[1] - lefts[0])
        offset = gap/2

        self.bar(lefts[:-1]+offset, counts, width_fraction=1.0, label=label,
                 x_label=x_label, y_label=y_label, **kwargs)

    def updateBarsDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelBars._model_data):
            self._bar_data[num].model_style = style_info
        self.refreshAllPlots()

    def updateBarsDataDelete(self, row):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        self._bar_data.pop(row)
        self.refreshAllPlots()

    def axisAspect(self):
        """
        Set axis aspect ratio property
        """
        aspect = self.ui.comboBoxAspect.currentText()
        self.mpl_widget.axes.set_aspect(aspect)
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def axisScaling(self):
        """
        Set axis scaling property
        """
        ratio = self.ui.comboBoxAxisScaling.currentText()
        self.mpl_widget.axes.axis(ratio)
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def axisVisible(self):
        """
        Set whether axis is on or off
        """
        state = self.ui.checkBoxAxisVisible.isChecked()
        if state:
            state = 'on'
        else:
            state = 'off'

        self.mpl_widget.axes.axis(state)
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def axisLimits(self):
        """
        Set axis limits
        """
        if self.sender() == self.ui.lineEditXLimMin:
            value = float(self.ui.lineEditXLimMin.text())
            self.mpl_widget.axes.axis(xmin=value)
        elif self.sender() == self.ui.lineEditXLimMax:
            value = float(self.ui.lineEditXLimMax.text())
            self.mpl_widget.axes.axis(xmax=value)
        elif self.sender() == self.ui.lineEditYLimMin:
            value = float(self.ui.lineEditYLimMin.text())
            self.mpl_widget.axes.axis(ymin=value)
        elif self.sender() == self.ui.lineEditYLimMax:
            value = float(self.ui.lineEditYLimMax.text())
            self.mpl_widget.axes.axis(ymax=value)

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def updateAxisParameters(self):
        axis_visible = self.mpl_widget.axes.axison
        self.ui.checkBoxAxisVisible.setChecked(axis_visible)
        xmin, xmax, ymin, ymax = self.mpl_widget.axes.axis()
        self.ui.lineEditXLimMin.setText(str(xmin))
        self.ui.lineEditXLimMax.setText(str(xmax))
        self.ui.lineEditYLimMin.setText(str(ymin))
        self.ui.lineEditYLimMax.setText(str(ymax))

if __name__ == '__main__':

    app = _QApplication(_sys.argv)

    winPlotter = SciPlotUI()
    winPlotter.show()

    x = _np.arange(100)
    y = x**2

    winPlotter.plot(x, y, x_label='X', label='Plot')
    winPlotter.plot(x, y**1.1, label='Plot 2')
    winPlotter.fill_between(x, y-1000, y+1000, label='Fill Between')

    winPlotter.imshow(_np.random.randn(100,100), label='Imshow')
    winPlotter.bar(x[::10],y[::10],label='Bar')
    winPlotter.hist(y,label='Hist')

    _sys.exit(app.exec_())