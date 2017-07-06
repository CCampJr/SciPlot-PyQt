# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:30:28 2016

@author: chc
"""

from sciplot.data.generic import Data as _Data
import matplotlib as _mpl


class LineStyle:
    """
    Style information for each data plotted (line)
    """
    def __init__(self):
        self._setupLineStyle()

    def _setupLineStyle(self):
        self.style_dict = {'color': None,
                           'alpha': None,
                           'linewidth': None,
                           'linestyle': None,
                           'marker': None,
                           'markersize': None}

    def retrieve_style_from_line(self, line):
        """
        Take an MPL line object and retrieve appropriate attributes
        """

        # Line color
        color = line.get_color()
        if isinstance(color, str):
            # print('Color: {}'.format(color))
            # color = _mpl.colors.ColorConverter.cache[color]
            color = _mpl.colors.ColorConverter().to_rgb(color)
        if isinstance(color, tuple):
            color = list(color)
        self.style_dict['color'] = color

        # Alpha (transparency)
        alpha = line.get_alpha()
        if alpha is None:
            alpha = 1
        self.style_dict['alpha'] = alpha

        # Linewidth
        self.style_dict['linewidth'] = line.get_linewidth()

        # Linestyle
        self.style_dict['linestyle'] = line.get_linestyle()

        # Marker
        self.style_dict['marker'] = line.get_marker()

        # Marker Size
        self.style_dict['markersize'] = line.get_markersize()


class DataLine(_Data, LineStyle):
    def __init__(self):
        self._setupData()
        self._setupLineStyle()

    @property
    def model_style(self):
        out = {}
        out.update(self.style_dict)
        out['label'] = self.label
        out['id'] = self.id
        out['meta'] = self.meta
        return out

    @model_style.setter
    def model_style(self, value):
        self.label = value['label']
        self.meta = value['meta']
        self.style_dict['color'] = value['color']
        self.style_dict['alpha'] = value['alpha']
        self.style_dict['linewidth'] = value['linewidth']
        self.style_dict['linestyle'] = value['linestyle']
        self.style_dict['marker'] = value['marker']
        self.style_dict['markersize'] = value['markersize']

class PlotsDataContainer:
    """
    Contains all plot data
    """
    def __init__(self):
        self.line_data_list = []
        self.patch_data_list = []
