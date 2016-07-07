# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 10:23:03 2016

@author: chc
"""

from cycler import cycler
import copy as _copy
import numpy as _np
import matplotlib as _mpl

class MplMarkers:
    MARKER_DICT = _mpl.markers.MarkerStyle.markers
    MARKER_DESC = []
    MARKER_SYMBOL = []
    for count in MARKER_DICT:
        MARKER_SYMBOL.append(count)
        MARKER_DESC.append(MARKER_DICT[count])

    @classmethod
    def index(cls, str_in):
        idx = None
        try:
            idx = cls.MARKER_DESC.index(str_in)
        except:
            idx = None
            try:
                idx = cls.MARKER_SYMBOL.index(str_in)
            except:
                idx = None
        return idx

class MplLines:
    LINESTYLE_DICT = _mpl.lines.lineStyles
    LINESTYLE_DESC = []
    LINESTYLE_SYMBOL = []
    for count in LINESTYLE_DICT:
        LINESTYLE_SYMBOL.append(count)
        LINESTYLE_DESC.append(LINESTYLE_DICT[count])

    @classmethod
    def index(cls, str_in):
        idx = None
        try:
            idx = cls.LINESTYLE_DESC.index(str_in)
        except:
            idx = None
            try:
                idx = cls.LINESTYLE_SYMBOL.index(str_in)
            except:
                idx = None
        return idx

class MplStyleSheets:
    """

    """

    _tableau20 = _np.array([[31, 119, 180],
                           [174, 199, 232],
                           [255, 127, 14],
                           [255, 187, 120],
                           [44, 160, 44],
                           [152, 223, 138],
                           [214, 39, 40],
                           [255, 152, 150],
                           [148, 103, 189],
                           [197, 176, 213],
                           [140, 86, 75],
                           [196, 156, 148],
                           [227, 119, 194],
                           [247, 182, 210],
                           [127, 127, 127],
                           [199, 199, 199],
                           [188, 189, 34],
                           [219, 219, 141],
                           [23, 190, 207],
                           [158, 218, 229]], dtype=_np.float)/255

    _tableau10 = _tableau20[::2,:]

    _tableau10_med = _np.array([[114, 158, 206],
                                [255, 158, 74],
                                [103, 191, 92],
                                [237, 102, 93],
                                [173, 139, 201],
                                [168, 120, 110],
                                [237, 151, 202],
                                [162, 162, 162],
                                [205, 204, 93],
                                [109, 204, 218]], dtype = _np.float)/255


    _base_crikit = {'font.family': ['sans-serif'],
                    'font.sans-serif': ['Arial',
                                        'Bitstream Vera Sans',
                                        'DejaVu Sans',
                                        'Lucida Grande',
                                        'Verdana',
                                        'Geneva',
                                        'Lucid',
                                        'Avant Garde',
                                        'sans-serif'],
                    'axes.prop_cycle': cycler('color', _tableau10),
#                    'axes.prop_cycle': plt.style.library['ggplot']['axes.prop_cycle'],
                    'image.cmap': 'viridis',
                    'image.interpolation': 'none'}

    _paper_halfwidth = {'axes.labelsize': 8.8,
                 'axes.titlesize': 9.6,
                 'figure.figsize': [3.3, 4.4],
                 'grid.linewidth': 0.8,
                 'legend.fontsize': 8.0,
                 'lines.linewidth': 1.4,
                 'lines.markeredgewidth': 0.0,
                 'lines.markersize': 5.6,
                 'patch.linewidth': 0.24,
                 'xtick.labelsize': 8.0,
                 'xtick.major.pad': 5.6,
                 'xtick.major.width': 0.8,
                 'xtick.minor.width': 0.4,
                 'ytick.labelsize': 8.0,
                 'ytick.major.pad': 5.6,
                 'ytick.major.width': 0.8,
                 'ytick.minor.width': 0.4}

    _paper_fullwidth = {'axes.labelsize': 8.8,
                 'axes.titlesize': 9.6,
                 'figure.figsize': [6.4, 4.4],
                 'grid.linewidth': 0.8,
                 'legend.fontsize': 8.8,
                 'lines.linewidth': 1.4,
                 'lines.markeredgewidth': 0.0,
                 'lines.markersize': 5.6,
                 'patch.linewidth': 0.24,
                 'xtick.labelsize': 8.0,
                 'xtick.major.pad': 5.6,
                 'xtick.major.width': 0.8,
                 'xtick.minor.width': 0.4,
                 'ytick.labelsize': 8.0,
                 'ytick.major.pad': 5.6,
                 'ytick.major.width': 0.8,
                 'ytick.minor.width': 0.4}

    _poster = {'axes.labelsize': 17.6,
               'axes.titlesize': 19.2,
               'figure.figsize': [12.8, 8.8],
              'grid.linewidth': 1.6,
              'legend.fontsize': 16.0,
              'lines.linewidth': 2.8,
              'lines.markeredgewidth': 0.0,
              'lines.markersize': 11.2,
              'patch.linewidth': 0.48,
              'xtick.labelsize': 16.0,
              'xtick.major.pad': 11.2,
              'xtick.major.width': 1.6,
              'xtick.minor.width': 0.8,
              'ytick.labelsize': 16.0,
              'ytick.major.pad': 11.2,
              'ytick.major.width': 1.6,
              'ytick.minor.width': 0.8}

    basic_halfwidth = _copy.deepcopy(_base_crikit)
    basic_halfwidth.update(_paper_halfwidth)

    basic_fullwidth = _copy.deepcopy(_base_crikit)
    basic_fullwidth.update(_paper_fullwidth)

    basic_poster = _copy.deepcopy(_base_crikit)
    basic_poster.update(_poster)


if __name__ == '__main__':
    import matplotlib.pyplot as _plt
    import numpy as _np

    x = _np.arange(100)
    _plt.style.use('classic')
    style = MplStyleSheets.basic_fullwidth
    _plt.style.use(style)

    _plt.figure()

    _plt.plot((_np.random.rand(10,1)*x).T, label='test')
    _plt.legend()
    _plt.show()

    _plt.figure()
    _plt.imshow(_np.random.rand(100,100))
    _plt.colorbar()
    _plt.show()
