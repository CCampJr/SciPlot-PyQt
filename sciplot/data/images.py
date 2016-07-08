# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 13:52:57 2016

@author: chc
"""

from sciplot.data.generic import Data2D as _Data2D
import matplotlib as _mpl
import numpy as _np


class ImageStyle:
    """
    Style information for each data plotted (images)
    """
    def __init__(self):
        self._setupImageStyle()

    def _setupImageStyle(self):
        """
        Style dictioonary.

        Maybe include cmap color in the future
        """
        self.style_dict = {'cmap_name': None,
                           'alpha': None,
                           'clim': None}

    def retrieve_style_from_image(self, image):
        """
        Take an MPL image object and retrieve appropriate attributes
        """

        # cmap name
        cmap_name = image.get_cmap().name
        if cmap_name is None:
            cmap_name = 'Custom'
        self.style_dict['cmap_name'] = cmap_name

        # Alpha (transparency)
        alpha = image.get_alpha()
        if alpha is None:
            alpha = 1
        self.style_dict['alpha'] = alpha

        # clim
        self.style_dict['clim'] = image.get_clim()


class DataImages(_Data2D, ImageStyle):
    def __init__(self):
        self._setupData()
        self._setupImageStyle()

    @property
    def model_style(self):
        out = {}
        out.update(self.style_dict)

        # clim broken out into high and low in model
        clim = out.pop('clim')
        out['clim_low'] = _np.min(clim)
        out['clim_max'] = _np.max(clim)
        out['label'] = self.label
        return out

    @model_style.setter
    def model_style(self, value):
        self.label = value['label']
        self.style_dict['cmap_name'] = value['cmap_name']
        self.style_dict['alpha'] = value['alpha']

        # clim broken out into high and low in model
        self.style_dict['clim'] = list(value['clim_low'], value['clim_high'])
