.. image:: https://travis-ci.org/CCampJr/SciPlot-PyQt.svg?branch=master
    :target: https://travis-ci.org/CCampJr/SciPlot-PyQt

.. image:: https://ci.appveyor.com/api/projects/status/github/CCampJr/SciPlot-PyQt?branch=master&svg=true
    :target: https://ci.appveyor.com/project/CCampJr/sciplot-pyqt


SciPlot-PyQt: Publication-ready scientific plotting for Python 
===============================================================

SciPlot-PyQt (aka SciPlot) is a user-interface/matplotlib wrapper built with
PyQt5 that allows interactive plotting through an embedded matplotlib canvas.
It enables fast and easy publication-ready plots and images:

-   Interactive plotting

-   Theme and style editing (TODO)

-   Figure saving and opening for later editing (TODO)

Dependencies
------------

**Note**: These are the developmental system specs. Older versions of certain
packages may work.

-   python >= 3.4
    
    - Tested with 3.4.4, 3.5.2, 3.6.1

-   numpy (1.9.3)
    
    - Tested with 1.11.3+mkl

-   PyQT5 (5.5.* or 5.6.*)  
    
    - Tested with 5.6, 5.8.1

-   matplotlib (1.5.0rc3, 2.0.0) (see below for MPL2)
    
    - Tested with 1.5.2, 2.0.0

-   Sphinx (1.5.2) (Only for building documentation)
    
    - Tested with 1.4.5, 1.6.4

-   numpydoc (0.6.0) (Only for building documentation)

-   sphinx_rtd_theme (0.2.5b2) (Only for building documentation)


Known Issues
------------

1.  **IPython**: SciPlot has problems when imported and ran via sciplot.main() or %run from within 
    IPython. It appears to work as expected when called through a normal Python interpreter.

2.  **PyQt 5.7**: There is a bug in PyQt 5.7.* that will prevent SciPlot's tables from showing the 
    individual plot entries (see https://www.riverbankcomputing.com/pipermail/pyqt/2017-January/038483.html). 
    Apparently, this will be fixed in 5.7.2.
    
    - As WinPython 3.5.2.3Qt5 and 3.5.2.2Qt5 use PyQt 5.7.*, it is advised to use WinPython 3.5.2.1Qt5 or 
      3.4.4.5Qt5 until the matter is sorted out.

    - Alternatively, one can uninstall pyqt5.7.* and force an install of <= 5.6.*.

3.  **MATPLOTLIB 2.0**: SciPlot version solder than 0.1.4 will crash with MPL 2.* as 
    several changes have been made to the MPL API.
    
    - For v0.1.3, the dev-MPL2 branch should address those problems
    - v0.1.4 is a merge of v0.1.3 and the dev-MPL2 branch (with other updates)


Installation
------------

**Note**: the installer only checks for the dependencies of matplotlib and
numpy. PyQt5 is not checked for, though, it is also required. See Depencies
above for more information and requirements.

Using pip (hard install)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # Only Python 3.* installed
    pip install sciplot-pyqt

    # If you have both Python 2.* and 3.* you may need
    pip3 install sciplot-pyqt

Using pip (soft install [can update with git])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::
    
    # Make new directory for sciplot-pyqt and enter it
    # Clone from github
    git clone https://github.com/CCampJr/SciPlot-PyQt.git

    # Only Python 3.* installed
    pip install -e .

    # If you have both Python 2.* and 3.* you may need instead
    pip3 install -e .

    # To update in the future
    git pull

Using setuptools
~~~~~~~~~~~~~~~~

You will need to `download the repository <https://github.com/CCampJr/SciPlot-PyQt/releases>`_
or clone the repository with git:

.. code::
    
    # Make new directory for sciplot-pyqt and enter it
    # Clone from github
    git clone https://github.com/CCampJr/SciPlot-PyQt.git

Perform the install **without building the documentation**:

.. code::

    python setup.py install

Perform the install **and build the documentation** (see dependencies above):

.. code::

    python setup.py build_sphinx
    python setup.py install

Usage
-----

.. code:: python

    import sciplot
    sp = sciplot.main()

**Note** Sciplot-pyqt relies on an existing, active Qt5 QApplication instance 
to operate. Some versions of Matplotlib 1.5.* provide this, others do not.
Matplotlib 2.* seems to always provide this functionality.

**If** you perform the examples below and just a non-repsonsive white window
appears, follow up the plotting commands with:

.. code:: python

    sp.app.exec_()

Sciplot tests for this and will prove you with a message to your terminal:

.. code::

    No QApplication instance (this is common with certain
    version of Matplotlib). Creating one.
    You will need to exec manually after you finish plotting.
    
    -----------Example---------------
    import sciplot\n\
    sp = sciplot.main()\n\n\

    # Plot a line
    sp.plot((0,1),(0,1))
    # Start the QApplication
    sp.app.exec_()

Example
~~~~~~~

.. code:: python

    sp.plot((0,1),(2,3),label='Line', x_label='X', y_label='Y', ls='--')
    sp.fill_between((0,1),(1,2),(3,4),label='Fill Between', color='r', alpha=0.25)

.. image:: ./Screenshot.png

.. code:: python

    sp.hist(r, bins=100, label='Histogram', color=[0, .2, .3],
            x_label='Amplitude', y_label='Counts', alpha=0.5)

.. image:: ./Screenshot2.png

.. code:: python

    sp.imshow(r, clim=[25,75], cmap='viridis', label='Imshow', x_label='X (pix)', 
              y_label='Y (pix)')

.. image:: ./Screenshot3.png

NONLICENSE
----------
This software was developed at the National Institute of Standards and Technology (NIST) by
employees of the Federal Government in the course of their official duties. Pursuant to
`Title 17 Section 105 of the United States Code <http://www.copyright.gov/title17/92chap1.html#105>`_,
this software is not subject to copyright protection and is in the public domain.
NIST assumes no responsibility whatsoever for use by other parties of its source code,
and makes no guarantees, expressed or implied, about its quality, reliability, or any other characteristic.

Specific software products identified in this open source project were used in order
to perform technology transfer and collaboration. In no case does such identification imply
recommendation or endorsement by the National Institute of Standards and Technology, nor
does it imply that the products identified are necessarily the best available for the
purpose.

Contact
-------
Charles H Camp Jr: `charles.camp@nist.gov <mailto:charles.camp@nist.gov>`_

Contributors
-------------
Charles H Camp Jr, Mona Lee
