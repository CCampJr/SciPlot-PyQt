# -*- coding: utf-8 -*-
"""
Generic data containers

Created on Thu Jul  7 10:31:43 2016

@author: chc
"""

import numpy as _np

class Data:
    """
    Contains the underlying data to be plotted
    
    Attributes
    ----------
    x : ndarray (1D)
        x-data (effectively, the horizontal axis data)
    
    y : ndarray (1D)
        y-data (effectively, the vertical axis data)
    
    label : str
        Label information, i.e., the name of the plot, graph, etc.
        
    style_dict : dict
        Style information (e.g., color, linewidth, etc)
        
    mplobj : object
        Object returned from the MPL plotting procedure.
    """
    def __init__(self):
        self._setupData()

    def _setupData(self):
        self.x = None
        self.y = None
        self.id = None
        self.label = None
        self.mplobj = None
        #self.units = {'x_units': None, 'y_units': None}
        self.style_dict = {}

    @property
    def model_style(self):
        out = {}
        out.update(self.style_dict)
        out['label'] = self.label
        out['id'] = self.id
        return out

class Data2D(Data):
    """
    Contains the underlying data to be imaged
    """
    def __init__(self):
        self._setupData()
        self.img = None

    @property
    def extent(self):
        """
        Generate an extent list used for mpl.imshow
        [xmin, xmax, ymin, ymax]
        """
        ext = [None, None, None, None]

        if self.x is not None:
            ext[0] = self.x.min()
            ext[1] = self.x.max()
        else:
            ext[0] = 0
            ext[1] = self.img.shape[1]

        if self.y is not None:
            ext[2] = self.y.min()
            ext[3] = self.y.max()
        else:
            ext[2] = 0
            ext[3] = self.img.shape[0]

        return ext

class DataGlobal:
    """
    Contains data that is pertinent across all plots
    """
    def __init__(self):
        self.labels = {'x_label': None, 'y_label': None, 'title': None}
