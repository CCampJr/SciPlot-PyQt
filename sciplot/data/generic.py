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
    """
    def __init__(self):
        self._setupData()

    def _setupData(self):
        self.x = None
        self.y = None
        self.label = None
        #self.units = {'x_units': None, 'y_units': None}
        self.style_dict = {}

    @property
    def model_style(self):
        out = {}
        out.update(self.style_dict)
        out['label'] = self.label
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
