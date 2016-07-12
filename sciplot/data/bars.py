# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:30:28 2016

@author: chc
"""

from sciplot.data.generic import Data as _Data
import matplotlib as _mpl


class BarStyle:
    """
    Style information for each data plotted (bar)
    """
    def __init__(self):
        self._setupBarStyle()

    def _setupBarStyle(self):
        self.style_dict = {'facecolor': None,
                           'alpha': None,
                           'edgecolor': None,
                           'linewidth': None,
                           'width_factor': None}

    def retrieve_style_from_bar(self, bar):
        """
        Take an MPL bar object and retrieve appropriate attributes
        """

        # facecolor
        facecolor = bar.get_facecolor()[:-1]
        if isinstance(facecolor, str):
            facecolor = _mpl.colors.ColorConverter.cache[facecolor]
        if isinstance(facecolor, tuple):
            facecolor = list(facecolor)
        self.style_dict['facecolor'] = facecolor

        # Alpha (transparency)
        alpha = bar.get_alpha()
        if alpha is None:
            alpha = 1
        self.style_dict['alpha'] = alpha

        # edgecolor
        edgecolor = bar.get_edgecolor()[:-1]
        if isinstance(edgecolor, str):
            edgecolor = _mpl.colors.ColorConverter.cache[edgecolor]
        if isinstance(edgecolor, tuple):
            edgecolor = list(edgecolor)
        self.style_dict['edgecolor'] = edgecolor

        # Linewidth
        self.style_dict['linewidth'] = bar.get_linewidth()


class DataBar(_Data, BarStyle):
    def __init__(self):
        self._width = None
        self._left = None
        self._gap = None
        self._setupData()
        self._setupBarStyle()

    @property
    def model_style(self):
        out = {}
        out.update(self.style_dict)
        out['label'] = self.label
        return out

    @model_style.setter
    def model_style(self, value):
        self.label = value['label']
        self.style_dict['facecolor'] = value['facecolor']
        self.style_dict['alpha'] = value['alpha']
        self.style_dict['edgecolor'] = value['edgecolor']
        self.style_dict['linewidth'] = value['linewidth']
        self.style_dict['width_factor'] = value['width_factor']
        if self._gap is not None:
            self._width = self._gap*self.style_dict['width_factor']
        else:
            self._width = self.style_dict['width_factor']
        self._left = self.x - self._width/2
