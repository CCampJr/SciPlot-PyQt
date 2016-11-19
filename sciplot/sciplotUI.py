# -*- coding: utf-8 -*-
"""
SciPlot-PyQt: Publication-ready scientific plotting for Python
==============================================================

SciPlot-PyQt (aka SciPlot) is a user-interface/matplotlib wrapper built with 
PyQt5 that allows interactive plotting through an embedded matplotlib canvas. 
It enables fast and easy publication-ready plots and images:
    
    * Interactive plotting
    * Theme and style editing (TODO)
    * Figure saving and opening for later editing (TODO)
    
Supported Plot Types
---------------------
Line plots : plot

Bar plots : bar, hist

Polycollections : fill_between

Images : imshow

Notes
-----
SciPlot has a lot of advances/improvements to make. Feel free to contact me--
help is always welcome!

Usage
-----
import sciplot
sp = sciplot.SciPlotUI()
sp.show()

Example
-------
sp.plot((0,1),(2,3),label='Line', x_label='X', y_label='Y', ls='--')
sp.fill_between((0,1),(1,2),(3,4),label='Fill Between', color='r', alpha=0.25)

Authors
-------
* Charles H. Camp Jr. <charles.camp@nist.gov>
"""

import sys as _sys
import numpy as _np
import time as _time

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QMainWindow as _QMainWindow,
                             QTableView as _QTableView,
                             QSizePolicy as _QSizePolicy,
                             QTabWidget as _QTabWidget)

# Import from Designer-based GUI
from sciplot.ui.qt_Plotter import Ui_MainWindow as Ui_Plotter
from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas
#from sciplot.utils.mplstyle import MplStyleSheets, MplMarkers, MplLines
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

class SciPlotUI(_QMainWindow):
    """
    Scientific plotting user-interface for creating publication-quality plots
    and images

    Parameters
    ----------

    limit_to : list, optional (default = None)
        Limit the application to implement only certain functionality. \
        Default is all elements turned ON. See Notes for options.
        
    show : bool, optional (default = True)
        Whether to show the UI upon instantiation

    Methods
    -------
    plot : MPL-like plotting functionality

    imshow : MPL-like imshow

    bar : MPL-like bar plot EXCEPT centered (rather than left-edge defined)

    hist : MPL-like histogram

    fill_between : MPL-like fill_between

    Internal Methods
    ----------------
    updatePlotDataStyle : Make updates to plots (lines) when a stylistic \
    change is made within the model-table

    updatePlotDataDelete : Remove a plot when deleted from model-table

    updateFillBetweenDataStyle : Make updates to fill between's when a \
    stylistic change is made within the model-table

    updateFillBetweenDataDelete : Remove a fill between when deleted from \
    model-table

    updateImagesDataStyle : Make updates to images when a stylistic \
    change is made within the model-table

    updateImageDataDelete : Remove an image when deleted from model-table

    updateBarsDataStyle : Make updates to bars plots when a stylistic \
    change is made within the model-table

    updateBarsDataDelete : Remove a bar plot when deleted from model-table

    refreshAllPlots : Delete all plots and re-plot

    updateAllLabels : Update all labels (x-, y-, title, etc) on MPL widget, \
        in model, in data container, and in UI lineEdits

    updateLineEditLabels : Update all labels (x-, y-, title, etc) in UI \
        lineEdits

    updateDataLabels : Update all labels (x-, y-, title, etc) in data \
    container

    updateMplLabels : Update all labels (x-, y-, title, etc) on MPL widget

    updateLabelsFromLineEdit : Update all labels (x-, y-, title, etc) on MPL \
        widget, in model, and in data container. Edits came from lineEdits.

    axisAspect : Set MPL-axis aspect ratio setting

    axisScaling : Set MPL-axis scaling ratio setting

    axisVisible : Set MPL-axis on or off

    axisLimits : Set MPL-axis limits

    updateAxisParameters : Query and update UI lineEdits related to axis \
        properties such as limits, visibility (on/off), scaling, and aspect \
        ratio

    Notes
    -----
    * limit_to options: 'lines', 'fill betweens', 'bars', images'
    """
    def __init__(self, limit_to=None, parent=None, show=True):
        self.list_ids = []
        self.list_all = []

        self.setup(limit_to=limit_to, parent=parent)
        if show:
            self.show()
        
    def closeEvent(self, event):
        pass

    def _tabAvailability(self, limit_to=None):
        """
        If limit_to is provided, limits the tabs (elements) that are available.

        May be useful for built-upon applications.
        """
        if limit_to is None:
            self.elements = ['lines', 'fill betweens', 'images', 'bars']
            self._to_setup = [self.setupLines, self.setupFillBetweens,
                              self.setupImages, self.setupBars]
        else:
            self._to_setup = []
            self.elements = []
            if limit_to.count('lines'):
                self.elements.append('lines')
                self._to_setup.append(self.setupLines)
            if limit_to.count('fill betweens'):
                self.elements.append('fill betweens')
                self._to_setup.append(self.setupFillBetweens)
            if limit_to.count('images'):
                self.elements.append('images')
                self._to_setup.append(self.setupImages)
            if limit_to.count('bars'):
                self.elements.append('bars')
                self._to_setup.append(self.setupBars)

    def setupLines(self):
        """
        Enable and setup line plotting
        """

        # Enable line plotting
        self.plot = self.__plot
        self.updatePlotDataStyle = self.__updatePlotDataStyle
        self.updatePlotDataDelete = self.__updatePlotDataDelete

        # Initial  and insert table view for line plots
        self.tableViewLine = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewLine, 'Lines')

        # Set model and delegates
        # Lines
        self.modelLine = _TableModelLines()
        self.delegateLine = _EditDelegateLines()
        self.tableViewLine.setModel(self.modelLine)
        self.tableViewLine.setItemDelegate(self.delegateLine)
        self.tableViewLine.show()


        # RESIZE COLUMNS
        header = self.tableViewLine.horizontalHeader()
        # alpha
        col = self.modelLine._COL_ALPHA
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewLine.setColumnWidth(col, new_width)

        # linewidth
        col = self.modelLine._COL_LINEWIDTH
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewLine.setColumnWidth(col, new_width)

        # markersize
        col = self.modelLine._COL_MARKERSIZE
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewLine.setColumnWidth(col, new_width)

        # delete
        col = self.modelLine._COL_DELETE
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewLine.setColumnWidth(col, new_width)

        # SIGNALS AND SLOTS

        # Make use of double-clicking within table
        self.tableViewLine.doubleClicked.connect(
            self.modelLine.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelLine.dataChanged.connect(self.updatePlotDataStyle)
        self.modelLine.dataDeleted.connect(self.updatePlotDataDelete)

    def setupFillBetweens(self):
        """
        Enable and setup fill between plotting
        """

        # Enable fill_between plotting
        self.fill_between = self.__fill_between
        self.updateFillBetweenDataStyle = self.__updateFillBetweenDataStyle
        self.updateFillBetweenDataDelete = self.__updateFillBetweenDataDelete

        # Initial and insert table view for fill_between plots
        self.tableViewFillBetween = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewFillBetween,
                                      'Fill Between')

        # Fill Between
        self.modelFillBetween = _TableModelFillBetween()
        self.delegateFillBetween = _EditDelegateFillBetween()
        self.tableViewFillBetween.setModel(self.modelFillBetween)
        self.tableViewFillBetween.setItemDelegate(self.delegateFillBetween)
        self.tableViewFillBetween.show()

        # RESIZE COLUMNS
        header = self.tableViewFillBetween.horizontalHeader()
        # alpha
        col = self.modelFillBetween._COL_ALPHA
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewFillBetween.setColumnWidth(col, new_width)

        # linewidth
        col = self.modelFillBetween._COL_LINEWIDTH
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewFillBetween.setColumnWidth(col, new_width)

        # delete
        col = self.modelFillBetween._COL_DELETE
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewFillBetween.setColumnWidth(col, new_width)

        # SIGNALS AND SLOTS

        # Make use of double-clicking within table
        self.tableViewFillBetween.doubleClicked.connect(
            self.modelFillBetween.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelFillBetween.dataChanged.connect(self.updateFillBetweenDataStyle)
        self.modelFillBetween.dataDeleted.connect(self.updateFillBetweenDataDelete)

    def setupImages(self):
        """
        Enable and setup image plotting
        """

        # Enable imaging
        self.imshow = self.__imshow
        self.updateImagesDataStyle = self.__updateImagesDataStyle
        self.updateImagesDataDelete = self.__updateImagesDataDelete

        # images data-- similar to plot_data above

        # Initial  and insert table view for images
        self.tableViewImages = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewImages, 'Images')

        # Images
        self.modelImages = _TableModelImages()
        self.delegateImages = _EditDelegateImages()
        self.tableViewImages.setModel(self.modelImages)
        self.tableViewImages.setItemDelegate(self.delegateImages)
        self.tableViewImages.show()

        # RESIZE COLUMNS
        header = self.tableViewImages.horizontalHeader()
        # alpha
        col = self.modelImages._COL_ALPHA
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewImages.setColumnWidth(col, new_width)

        # clim low
        col = self.modelImages._COL_CLIM_LOW
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewImages.setColumnWidth(col, new_width)

        # clim high
        col = self.modelImages._COL_CLIM_HIGH
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewImages.setColumnWidth(col, new_width)

        # delete
        col = self.modelImages._COL_DELETE
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewImages.setColumnWidth(col, new_width)

        # SIGNALS AND SLOTS

        # Make use of double-clicking within table
        self.tableViewImages.doubleClicked.connect(
            self.modelImages.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelImages.dataChanged.connect(self.updateImagesDataStyle)
        self.modelImages.dataDeleted.connect(self.updateImagesDataDelete)

    def setupBars(self):
        """
        Enable and setup bar and histogram plotting
        """

        # Enable bar plotting
        self.bar = self.__bar
        self.hist = self.__hist
        self.updateBarsDataStyle = self.__updateBarsDataStyle
        self.updateBarsDataDelete = self.__updateBarsDataDelete

        # Initial  and insert table view for bars
        self.tableViewBars = _QTableView()
        self.ui.modelTabWidget.addTab(self.tableViewBars, 'Bars')


        # Bars/Bars
        self.modelBars = _TableModelBars()
        self.delegateBars = _EditDelegateBars()
        self.tableViewBars.setModel(self.modelBars)
        self.tableViewBars.setItemDelegate(self.delegateBars)
        self.tableViewBars.show()

        # RESIZE COLUMNS
        header = self.tableViewBars.horizontalHeader()
        # alpha
        col = self.modelBars._COL_ALPHA
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewBars.setColumnWidth(col, new_width)

        # linewidth
        col = self.modelBars._COL_LINEWIDTH
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewBars.setColumnWidth(col, new_width)

        # widthfactor
        col = self.modelBars._COL_WIDTH_FACTOR
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewBars.setColumnWidth(col, new_width)

        # delete
        col = self.modelBars._COL_DELETE
        new_width = int(1.1*header.sectionSizeHint(col))
        self.tableViewBars.setColumnWidth(col, new_width)

        # SIGNALS AND SLOTS

        # Make use of double-clicking within table
        self.tableViewBars.doubleClicked.connect(
            self.modelBars.doubleClickCheck)

        # When a model (table) elements changes or is deleted
        self.modelBars.dataChanged.connect(self.updateBarsDataStyle)
        self.modelBars.dataDeleted.connect(self.updateBarsDataDelete)

    def setup(self, limit_to=None, parent=None):
        """
        Basic UI setup
        """

        # Generic start to any pyQT program
        super(SciPlotUI, self).__init__(parent)
        self.ui = Ui_Plotter()
        self.ui.setupUi(self)
        self.setSizePolicy(_QSizePolicy.Expanding,
                           _QSizePolicy.Expanding)

        # Global "data" i.e., title, x-label, y-label, etc
        self._global_data = _DataGlobal()

        # MPL plot widget
        self.mpl_widget = _MplCanvas(height=6, dpi=100)
        self.mpl_widget.ax.hold(True)

        # Insert MPL widget and toolbar
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget)
        self.ui.verticalLayout.insertWidget(0, self.mpl_widget.toolbar)
        self.updateAxisParameters()
        self.mpl_widget.draw()

        # Insert TabWidget
        self.ui.modelTabWidget = _QTabWidget()
        self.ui.verticalLayout.insertWidget(-1, self.ui.modelTabWidget)

        # Setup what tabs are available:
        self._tabAvailability(limit_to)
        for count in self._to_setup:
            count()

        # SIGNALS AND SLOTS

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
        
        # Actions
        self.ui.pushButtonClearAll.pressed.connect(self.clearAll)
        self.ui.pushButtonDefaultView.pressed.connect(self.defaultView)

    def __plot(self, x, y, label=None, x_label=None, y_label=None, **kwargs):
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
        plot_data.id = _time.time()

        # Plot outputs a line object
        plot_data.mplobj = self.mpl_widget.ax.plot(x, y, label=label, **kwargs)
        try:
            self.mpl_widget.ax.legend(loc='best')
        except:
            pass

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        self.axisAspect()
        self.mpl_widget.draw()


        # Since the plot was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        plot_data.retrieve_style_from_line(plot_data.mplobj[0])

        # Append this specific plot data to out list of all plots
        self.list_ids.append(plot_data.id)
        self.list_all.append(plot_data)

        # Update model
        self.modelLine._model_data.append(plot_data.model_style)
        self.modelLine.layoutChanged.emit()

    def updateMplLabels(self, x_label=None, y_label=None, title=None):
        """
        Within the MPL widget, update the x- and y-labels and the title
        """
        if x_label is not None:
            self.mpl_widget.ax.set_xlabel(x_label)

        if y_label is not None:
            self.mpl_widget.ax.set_ylabel(y_label)

        if title is not None:
            self.mpl_widget.ax.set_title(title)
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

    def __updatePlotDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the plot data
        """
        for num, style_info in enumerate(self.modelLine._model_data):
            idx = self.list_ids.index(style_info['id'])
            self.list_all[idx].model_style = style_info
        self.refreshAllPlots()

    def __updatePlotDataDelete(self, row, plt_id):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        try:
#            print('Plot id: {}'.format(plt_id))
            idx_to_remove = self.list_ids.index(plt_id)
            self.list_ids.pop(idx_to_remove)
            self.list_all.pop(idx_to_remove)
        except:
            print('Error in __updatePlotDataDelete: {}'.format(idx_to_remove))
            
        self.refreshAllPlots()

    def refreshAllPlots(self):
        """
        Clear and re-plot all plot data of all types
        """

        # Clear axis -- in the future, maybe clear figure and recreate axis
        self.mpl_widget.ax.clear()
        
        for itm in self.list_all:
            if isinstance(itm, _DataLine):
#                print('Line')
                self.mpl_widget.ax.hold(True)
                
                # Hide label if alpha=0
                if itm.style_dict['alpha'] == 0:
                    label = None
                else:
                    label = itm.label
                itm.mplobj = self.mpl_widget.ax.plot(itm.x, itm.y, 
                                                     label=label,
                                                     color=itm.style_dict['color'],
                                                     alpha=itm.style_dict['alpha'],
                                                     linewidth=itm.style_dict['linewidth'],
                                                     linestyle=itm.style_dict['linestyle'],
                                                     marker=itm.style_dict['marker'],
                                                     markersize=itm.style_dict['markersize'])
            elif isinstance(itm, _DataBar):
#                print('Bar')
                self.mpl_widget.ax.hold(True)
                
                # Hide label if alpha=0
                if itm.style_dict['alpha'] == 0:
                    label = None
                else:
                    label = itm.label
                itm.mplobj = self.mpl_widget.ax.bar(itm._left, itm.y, 
                                                    bottom=itm.bottom,
                                                    width=itm._width,
                                                    label=label,
                                                    facecolor=itm.style_dict['facecolor'],
                                                    alpha=itm.style_dict['alpha'],
                                                    edgecolor=itm.style_dict['edgecolor'],
                                                    linewidth=itm.style_dict['linewidth'])
            elif isinstance(itm, _DataImages):
#                print('Images')
                self.mpl_widget.ax.hold(True)
                
                # Hide label if alpha=0
                if itm.style_dict['alpha'] == 0:
                    label = None
                else:
                    label = itm.label
                if itm.cbar['obj'] is not None:
                    try:  # Have had some unknown exceptions with .remove()
                        itm.cbar['obj'].remove()
                        itm.cbar['obj'] = None
                    except:
                        pass
                itm.mplobj = self.mpl_widget.ax.imshow(itm.img, label=label,
                                                       interpolation='none',
                                                       origin='lower',
                                                       cmap=_mpl.cm.cmap_d[itm.style_dict['cmap_name']],
                                                       alpha=itm.style_dict['alpha'],
                                                       clim=itm.style_dict['clim'])
                if itm.cbar['show']:
                    itm.cbar['obj'] = self.mpl_widget.fig.colorbar(itm.mplobj,
                                                                   use_gridspec=True)
            elif isinstance(itm, _DataFillBetween):
#                print('Fill Between')
                self.mpl_widget.ax.hold(True)
                
                # Hide label if alpha=0
                if itm.style_dict['alpha'] == 0:
                    label = None
                else:
                    label = itm.label
                itm.mplobj = self.mpl_widget.ax.fill_between(itm.x, itm.y_low, itm.y_high,
                                                  label=label,
                                                  facecolor=itm.style_dict['facecolor'],
                                                  edgecolor=itm.style_dict['edgecolor'],
                                                  alpha=itm.style_dict['alpha'],
                                                  linewidth=itm.style_dict['linewidth'])

            else:
                print('Unknown')

        # Only add a legend if a plot exists
        # Only certain objects provide labels
        label_object_count = len(self.list_all)

        if label_object_count > 0:
            self.mpl_widget.ax.legend(loc='best')

        # Apply x- and y-labels and a title if they are set
        if self._global_data.labels['title'] is not None:
            self.mpl_widget.ax.set_title(self._global_data.labels['title'])
        if self._global_data.labels['x_label'] is not None:
            self.mpl_widget.ax.set_xlabel(self._global_data.labels['x_label'])
        if self._global_data.labels['y_label'] is not None:
            self.mpl_widget.ax.set_ylabel(self._global_data.labels['y_label'])

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.axisAspect()
        self.mpl_widget.draw()

    def __fill_between(self, x, y_low, y_high, label=None, x_label=None,
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
        fill_between_data.id = _time.time()

        # Fill between outputs a polycollection
        fill_between_data.mplobj = self.mpl_widget.ax.fill_between(x, y_low, y_high,
                                                   label=label, **kwargs)
        self.mpl_widget.ax.legend(loc='best')
        self.mpl_widget.fig.tight_layout()
        self.axisAspect()
        self.mpl_widget.draw()

        # Since the fill_between was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        fill_between_data.retrieve_style_from_polycollection(fill_between_data.mplobj)

        # Append this specific plot data to out list of all plots
        self.list_ids.append(fill_between_data.id)
        self.list_all.append(fill_between_data)

        # Update model
        self.modelFillBetween._model_data.append(fill_between_data.model_style)
        self.modelFillBetween.layoutChanged.emit()
        

    def __updateFillBetweenDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelFillBetween._model_data):
            idx = self.list_ids.index(style_info['id'])
            self.list_all[idx].model_style = style_info
        self.refreshAllPlots()

    def __updateFillBetweenDataDelete(self, row, plt_id):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        idx_to_remove = self.list_ids.index(plt_id)
        self.list_ids.pop(idx_to_remove)
        self.list_all.pop(idx_to_remove)
        
        self.refreshAllPlots()

    def __imshow(self, img, x=None, y=None, label=None,
               x_label=None, y_label=None, cbar=False, **kwargs):
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
            
        cbar : bool
            Attach a colorbar to the img

        kwargs : dict
            Other parameters sent directly to mpl-imshow

        """

        # Temporary plot-data
        image_data = _DataImages()
        image_data.img = img
        image_data.x = x
        image_data.y = y
        image_data.label = label
        image_data.id = _time.time()
        image_data.cbar['show'] = cbar

        # Imshow outputs an image object
        image_data.mplobj = self.mpl_widget.ax.imshow(img, interpolation='None',
                                                origin='lower',
                                                label=label,
                                                **kwargs)
        if image_data.cbar['show']:
            image_data.cbar['obj'] = self.mpl_widget.fig.colorbar(image_data.mplobj,
                                                use_gridspec=True)
            
#        self.mpl_widget.ax.legend(loc='best')

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        
        self.axisAspect()
        self.mpl_widget.draw()

        # Since the image was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup cmap, etc.
        # Thus, we plot, then retrieve what the style info was
        image_data.retrieve_style_from_image(image_data.mplobj)

        # Append this specific plot data to out list of all plots
        self.list_ids.append(image_data.id)
        self.list_all.append(image_data)

        # Update model
        self.modelImages._model_data.append(image_data.model_style)
        self.modelImages.layoutChanged.emit()


    def __updateImagesDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelImages._model_data):
            idx = self.list_ids.index(style_info['id'])
            self.list_all[idx].model_style = style_info
        self.refreshAllPlots()

    def __updateImagesDataDelete(self, row, plt_id):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        
        idx_to_remove = self.list_ids.index(plt_id)
        self.list_ids.pop(idx_to_remove)
        popd = self.list_all.pop(idx_to_remove)
            
        if popd.cbar['obj'] is not None:
            popd.cbar['obj'].remove()
#        self.axisAspect()
        self.refreshAllPlots()


    def __bar(self, x, y, bottom=0, width_factor=1.0, use_real_width=False, label=None,
            x_label=None, y_label=None, **kwargs):
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
            Y-axis data (height)

        bottom : float (for now)
            Baseline of bars
            
        width_factor: float
            If legnth of y>1, fraction of space between bars taken up by bar \
            (e.g. 1.0 leads to bars that tough). If y is a single-value OR \
            use_real_width is True), is the width of the bar.

        use_real_width : bool, optional (default=False):
            If True, width_factor is the real width (in x-units)
            
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
        bar_data.bottom = bottom
        bar_data.label = label
        bar_data.id = _time.time()

        bar_data.style_dict['width_factor'] = width_factor

        _multi_value = None

        if isinstance(y, (int, float)):
            _multi_value = False
        if isinstance(y, _np.ndarray):
            if y.size == 1:
                _multi_value = False
            else:
                _multi_value = True
        if isinstance(y, (list, tuple)):
            if len(y) == 1:
                _multi_value = False
            else:
                _multi_value = True

        if _multi_value and use_real_width == False:
            # Distance between bars
            bar_data._gap = _np.abs(x[1]-x[0])

            # Width of a bar is a fraction of the gap
            bar_data._width = bar_data._gap*bar_data.style_dict['width_factor']

        else:
            # Single-valued: no gap
            bar_data._gap = None
            bar_data._width = width_factor

        # MPL-bar uses left-edge rather than center
        bar_data._left = bar_data.x - bar_data._width/2

        # Plot outputs a list of patch objects
        bar_data.mplobj = self.mpl_widget.ax.bar(bar_data._left, y,
                                           bottom=bar_data.bottom,
                                           width=bar_data._width,
                                           label=label, **kwargs)
        self.mpl_widget.ax.legend(loc='best')

        # If labels are provided, update the global data and the linEdits
        if x_label is not None or y_label is not None:
            self.updateAllLabels(x_label=x_label, y_label=y_label)

        self.mpl_widget.fig.tight_layout()
        
        self.axisAspect()
        self.mpl_widget.draw()


        # Since the plot was not fed style-info (unless kwargs were used)
        # we rely on the mpl stylesheet to setup color, linewidth, etc.
        # Thus, we plot, then retrieve what the style info was
        bar_data.retrieve_style_from_bar(bar_data.mplobj[0])

        # Append this specific plot data to out list of all plots
        self.list_ids.append(bar_data.id)
        self.list_all.append(bar_data)
        
        # Update model
        self.modelBars._model_data.append(bar_data.model_style)
        self.modelBars.layoutChanged.emit()

    def __hist(self, data, bins=10, label=None, x_label=None,
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

        self.bar(lefts[:-1]+offset, counts, width_factor=1.0, label=label,
                 x_label=x_label, y_label=y_label, **kwargs)

    def __updateBarsDataStyle(self):
        """
        Something style-related changed in the model; thus, need to change \
        these elements in the fill_between data
        """
        for num, style_info in enumerate(self.modelBars._model_data):
            idx = self.list_ids.index(style_info['id'])
            self.list_all[idx].model_style = style_info
        self.refreshAllPlots()

    def __updateBarsDataDelete(self, row, plt_id):
        """
        A plot was deleted (likely from within the model); thus, need to \
        remove the corresponding plot data
        """
        idx_to_remove = self.list_ids.index(plt_id)
        self.list_ids.pop(idx_to_remove)
        self.list_all.pop(idx_to_remove)
        
        self.refreshAllPlots()

    def axisAspect(self):
        """
        Set axis aspect ratio property
        """
        aspect = self.ui.comboBoxAspect.currentText()
        self.mpl_widget.ax.set_aspect(aspect)
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def axisScaling(self):
        """
        Set axis scaling property
        """
        ratio = self.ui.comboBoxAxisScaling.currentText()
        self.mpl_widget.ax.axis(ratio)
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

        self.mpl_widget.ax.axis(state)
        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def axisLimits(self):
        """
        Set axis limits
        """
        if self.sender() == self.ui.lineEditXLimMin:
            value = float(self.ui.lineEditXLimMin.text())
            self.mpl_widget.ax.axis(xmin=value)
        elif self.sender() == self.ui.lineEditXLimMax:
            value = float(self.ui.lineEditXLimMax.text())
            self.mpl_widget.ax.axis(xmax=value)
        elif self.sender() == self.ui.lineEditYLimMin:
            value = float(self.ui.lineEditYLimMin.text())
            self.mpl_widget.ax.axis(ymin=value)
        elif self.sender() == self.ui.lineEditYLimMax:
            value = float(self.ui.lineEditYLimMax.text())
            self.mpl_widget.ax.axis(ymax=value)

        self.mpl_widget.fig.tight_layout()
        self.updateAxisParameters()
        self.mpl_widget.draw()

    def updateAxisParameters(self):
        """
        Query current state of axis settings and update appropriate lineEdit's
        """
        axis_visible = self.mpl_widget.ax.axison
        self.ui.checkBoxAxisVisible.setChecked(axis_visible)
        xmin, xmax, ymin, ymax = self.mpl_widget.ax.axis()
        self.ui.lineEditXLimMin.setText(str(xmin))
        self.ui.lineEditXLimMax.setText(str(xmax))
        self.ui.lineEditYLimMin.setText(str(ymin))
        self.ui.lineEditYLimMax.setText(str(ymax))
        
    def defaultView(self):
        """
        Set default and Home view to the current one
        """
        self.mpl_widget.toolbar._views.clear()
        self.mpl_widget.toolbar._positions.clear()
        self.mpl_widget.toolbar.update()
        
    def clearAll(self):
        """
        Clear all plots and graphs and images
        """
        try:
            self.modelLine._model_data = []
            self.modelLine.layoutChanged.emit()
        except:
            print('Error in clear all of plots/lines')
        
        try:
            self.modelBars._model_data = []
            self.modelBars.layoutChanged.emit()
        except:
            print('Error in clear all of bars')
        
        
        try:
            # Need to iterate as to check for colorbar existance
            for num, model_data in enumerate(self.modelImages._model_data):
                idx_to_remove = self.list_ids.index(model_data['id'])
                self.list_ids.pop(idx_to_remove)
                popd = self.list_all.pop(idx_to_remove)
                if popd.cbar['obj'] is not None:
                    popd.cbar['obj'].remove()
            
            self.modelImages._model_data = []
            self.modelImages.layoutChanged.emit()
        except:
            print('Error in clear all of images')
        
        try:
            self.modelFillBetween._model_data = []
            self.modelFillBetween.layoutChanged.emit()
        except:
            print('Error in clear all of fill-betweens')
            
        try:
            self.list_ids = []
            self.list_all = []
        except:
            print('Error in clear all')
        finally:
            self.refreshAllPlots()
            
            
if __name__ == '__main__':

    app = _QApplication(_sys.argv)
    #app.setQuitOnLastWindowClosed(True)
    
    winPlotter = SciPlotUI(limit_to=['lines','bars', 'fill betweens',
                                     'images'])
    #winPlotter.show()

    x = _np.arange(100)
    y = x**2

    winPlotter.plot(x, y, x_label='X', label='Plot')
#    winPlotter.plot(x, y**1.1, label='Plot 2')
    winPlotter.fill_between(x, y-1000, y+1000, label='Fill Between')
#
    winPlotter.imshow(_np.random.randn(100,100), label='Imshow', cbar=True)
    winPlotter.bar(x[::10],y[::10],label='Bar')
#    winPlotter.hist(y,label='Hist')

#    winPlotter.bar(0,10, label='Bar: single-value')
    app.exec_()