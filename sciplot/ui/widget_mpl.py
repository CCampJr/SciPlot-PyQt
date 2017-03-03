# -*- coding: utf-8 -*-
"""
Create generic MPL canvas, toolbar, figure, axis.

Heavily borrowed from:
    matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

Created on Thu Jun 30 15:41:35 2016

@author: chc
"""

import sys as _sys
import os as _os
import numpy as _np
import matplotlib as _mpl
import matplotlib.style as _mpl_sty

from PyQt5 import QtWidgets as _QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as \
    FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as \
    _NavigationToolbar

from matplotlib.figure import Figure as _Figure

# Make sure that we are using QT5
_mpl.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, subplot=111, parent=None, width=5, height=4, dpi=100, 
                 figfacecolor=3*[0.941], style=None, **kwargs):

        #        super(MplCanvas, self).__init__(parent)
        if style is None:
            pass
        else:
            _mpl.style.use(style)

        # Create figure and axes
        self.fig = _Figure(figsize=(width, height), dpi=dpi, 
                           facecolor=figfacecolor, **kwargs)
        # Initialize the canvas
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        
        self.setupAx(subplot=subplot, **kwargs)
        
        # Not really used, but could be used to have some sort of initial plot
        self.compute_initial_figure()

        # Set canvas size policies and geometry
        FigureCanvas.setSizePolicy(self, _QtWidgets.QSizePolicy.Expanding,
                                   _QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Create the toolbar and connect to canvas (self)
        self.toolbar = _NavigationToolbar(self, None)
        
    def setupAx(self, subplot=111, **kwargs):
        if subplot > 339:
            raise ValueError('Subplot is limited to 3x3 or less')
        # Break out e.g. 111 to [1, 1, 1]
        subplot_list = [int(val) for val in list(str(subplot))]
        
        # Total number of subplots
        num_plots = subplot_list[0]*subplot_list[1]
        
        # Num of vertical subplots
        vnum = subplot_list[0]

        # Num of horiz subplots
        hnum = subplot_list[1]

        # [start, stop) count
        c_start = vnum*100 + hnum*10 + 1
        c_stop = vnum*100 + hnum*10 + num_plots + 1
        
        if num_plots <= 0:
            raise ValueError('subplot need be 1x1 to 3x3')
        elif num_plots == 1:
            self.ax = self.fig.add_subplot(111, **kwargs)
        elif num_plots > 1:
            self.ax = []
            for num, splt_num in enumerate(_np.arange(c_start, c_stop)):
                self.ax.append(self.fig.add_subplot(splt_num, **kwargs))
                self.ax[num].hold(False)
            self.fig.tight_layout()

    def compute_initial_figure(self):
        pass


if __name__ == '__main__':

    from PyQt5 import QtCore as _QtCore

    class ApplicationWindow(_QtWidgets.QMainWindow):
        def __init__(self, subplot=111, style=None):
            _QtWidgets.QMainWindow.__init__(self)
            #super(ApplicationWindow, self).__init__(None)
            self.setAttribute(_QtCore.Qt.WA_DeleteOnClose)

            self.main_widget = _QtWidgets.QWidget(self)

            self.mpl_layout = _QtWidgets.QVBoxLayout(self.main_widget)
            self.mpl_widget = MplCanvas(parent=self.main_widget, 
                                        subplot=subplot, width=5, height=4,
                                        dpi=100, style=style)
            self.mpl_layout.addWidget(self.mpl_widget.toolbar)
            self.mpl_layout.addWidget(self.mpl_widget)

            self.main_widget.setFocus()
            self.setCentralWidget(self.main_widget)

            self.setSizePolicy(_QtWidgets.QSizePolicy.Expanding,
                               _QtWidgets.QSizePolicy.Expanding)

    qApp = _QtWidgets.QApplication(_sys.argv)
    
#    aw = ApplicationWindow(style='seaborn-deep')
#    aw.mpl_widget.ax.plot((2,3),(4,-1), label='a')
#    aw.mpl_widget.ax.hold(True)
#    aw.mpl_widget.ax.plot((2,3),(4,-2), label='b')
#    aw.mpl_widget.ax.set_xlabel('X')
#    aw.mpl_widget.ax.set_ylabel('Y')
#    aw.mpl_widget.ax.set_title('Title')
#    aw.mpl_widget.ax.legend()
#    aw.mpl_widget.fig.tight_layout()
#    aw.show()
    
    aw2 = ApplicationWindow(style='seaborn-deep', subplot=211)
    aw2.mpl_widget.ax[0].set_title('0')
    aw2.mpl_widget.ax[1].set_title('1')
    aw2.show()

    qApp.exec_()
