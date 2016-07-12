# -*- coding: utf-8 -*-
"""

Demonstration of adding functionality to Sciplot

Created on Mon Jul 11 23:46:01 2016

@author: chc
"""

import numpy as _np

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../'))

from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QTabWidget as _QTabWidget,
                             QCalendarWidget as _QCalendarWidget)

from sciplot.sciplotUI import SciPlotUI as _SciPlotUI

class SciPlotAddon(_SciPlotUI):
    """
    Trivial example of using SciPlot with addons (or building another \
    application on top of SciPlot).
    """
    def __init__(self, limit_to=None, parent=None):
        # Setup SciPlot window
        self.setup(limit_to=limit_to, parent=parent)

        # Add a calendar to the tabs and have it displayed initially
        cal1 = _QCalendarWidget()
        self.ui.modelTabWidget.insertTab(0, cal1, 'Add-On Tab')
        self.ui.modelTabWidget.setCurrentIndex(0)

        # Add a calendar to the toolBox and have it displayed initially
        cal2 = _QCalendarWidget()
        self.ui.toolBox.addItem(cal2, 'Add-On Toolbox Tab')
        self.ui.toolBox.setCurrentIndex(self.ui.toolBox.count()-1)

        # Adjust with of groupBox to accomodate new widget (10% larger than)
        width = cal2.sizeHint().width()
        self.ui.groupBox.setMinimumWidth(1.1*width)
        self.ui.groupBox.setMaximumWidth(1.1*width)
        self.ui.groupBox.updateGeometry()

if __name__ == '__main__':

    app = _QApplication(_sys.argv)

    winPlotter = SciPlotAddon(limit_to=['bars'])

    winPlotter.show()

    x = _np.arange(100)
    y = x**2

#    winPlotter.plot(x, y, x_label='X', label='Plot')
#    winPlotter.plot(x, y**1.1, label='Plot 2')
#    winPlotter.fill_between(x, y-1000, y+1000, label='Fill Between')
#
#    winPlotter.imshow(_np.random.randn(100,100), label='Imshow')
#    winPlotter.bar(x[::10],y[::10],label='Bar')
#    winPlotter.hist(y,label='Hist')

    winPlotter.bar(0,10, label='Bar: single-value')
    _sys.exit(app.exec_())
