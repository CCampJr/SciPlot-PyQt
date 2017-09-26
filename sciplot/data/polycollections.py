# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:06:04 2016

@author: chc
"""

import matplotlib as _mpl


class PolyCollectionStyle:
    """
    Style information for each data plotted (polycollection)
    """
    def __init__(self):
        self._setupPolyCollectionStyle()

    def _setupPolyCollectionStyle(self):
        self.style_dict = {'facecolor': None,
                           'alpha': None,
                           'edgecolor': None,
                           'linewidth': None}

    def retrieve_style_from_polycollection(self, pc):
        """
        Take an MPL polycollection object and retrieve appropriate attributes
        """

        # facecolor p-collections return arrays of RGBA
        # Not going to worry about different face colors yet
        color = pc.get_facecolors()[0][:-1]
        if isinstance(color, str):
            # color = _mpl.colors.ColorConverter.cache[color]
            color = _mpl.colors.ColorConverter().to_rgb(color)
        if isinstance(color, tuple):
            color = list(color)
        self.style_dict['facecolor'] = color

        # Alpha (transparency)
        alpha = pc.get_alpha()
        if alpha is None:
            alpha = 1
        self.style_dict['alpha'] = alpha

        # edgecolor p-collections return arrays of RGBA
        # Not going to worry about different edge colors yet
        if pc.get_edgecolors().size > 0:  # MPL 2.0 starts with no edgecolors
            color = pc.get_edgecolors()[0][:-1]
        else:
            pass
        if isinstance(color, str):
            # color = _mpl.colors.ColorConverter.cache[color]
            color = _mpl.colors.ColorConverter().to_rgb(color)
        if isinstance(color, tuple):
            color = list(color)
        self.style_dict['edgecolor'] = color

        # Linewidth (p-collection return tuples of len 1)
        self.style_dict['linewidth'] = pc.get_linewidth()[0]


# Not actually going to use polycollection raw data
# So I'm not going to create this
#
#class DataPolyCollection(_Data, PolyCollectionStyle):
#    def __init__(self):
#        self._setupData()
#        self._setupLineStyle()
#
#    @property
#    def model_style(self):
#        out = {}
#        out.update(self.style_dict)
#        out['label'] = self.label
#        return out
#
#    @model_style.setter
#    def model_style(self, value):
#        self.label = value['label']
#        self.style_dict['color'] = value['color']
#        self.style_dict['alpha'] = value['alpha']
#        self.style_dict['linewidth'] = value['linewidth']
#        self.style_dict['linestyle'] = value['linestyle']
#        self.style_dict['marker'] = value['marker']
#        self.style_dict['markersize'] = value['markersize']

class PlotsDataContainer:
    """
    Contains all plot data
    """
    def __init__(self):
        self.line_data_list = []
        self.patch_data_list = []
