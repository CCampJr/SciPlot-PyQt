"""
Just a basic test
"""
import sys
import numpy as np

from PyQt5.QtWidgets import QApplication

from sciplot.sciplotUI import SciPlotUI

def test_pass():
    pass
    # app = QApplication(sys.argv)
    # winPlotter = SciPlotUI(limit_to=['lines','bars', 'fill betweens',
    #                                  'images'])
    
    # x = np.arange(100)
    # y = x**2
    # winPlotter.plot(x, y, x_label='X', label='Plot')
    # winPlotter.fill_between(x, y-1000, y+1000, label='Fill Between')
    # winPlotter.imshow(np.random.randn(100,100), label='Imshow', cbar=True)
    # winPlotter.bar(x[::10],y[::10],label='Bar')
    # app.exec_()