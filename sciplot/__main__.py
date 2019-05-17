"""

"""

import sys as _sys
import os as _os
from PyQt5.QtWidgets import (QApplication as _QApplication)
# from crikit import CRIkitUI
from sciplot import sciplotUI

def main(args=None):
    """
    The main routine.
    """

    if args is None:
        args = _sys.argv[1:]

    print('Starting up sciplot...')

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    win = sciplotUI.SciPlotUI() ### EDIT ###

    win.showMaximized()

    app.exec_()

if __name__ == '__main__':
    _sys.exit(main())