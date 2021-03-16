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
"""

import sys as _sys
import os as _os
import pkg_resources as _pkg_resources

try:
    from . import sciplotUI
except Exception as e:
    print(e)
else:
    _sys.path.append(_os.path.abspath('../'))

__version__ = '0.2.3a0'

# __all__ = ['SciPlotUI']

# from .sciplotUI import SciPlotUI as main
