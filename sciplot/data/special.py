# -*- coding: utf-8 -*-
"""
Somewhat specialized data containers.

Created on Thu Jul  7 15:21:29 2016

@author: chc
"""

from sciplot.data.polycollections import PolyCollectionStyle
from sciplot.data.generic import Data as _Data

class DataFillBetween(_Data, PolyCollectionStyle):
    def __init__(self):
        self._setupData()
        self._setupPolyCollectionStyle()
        del self.y
        self.y_low = None
        self.y_high = None

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
        self.style_dict['facecolor'] = value['facecolor']
        self.style_dict['alpha'] = value['alpha']
        self.style_dict['edgecolor'] = value['edgecolor']
        self.style_dict['linewidth'] = value['linewidth']
