# SciPlot-PyQt: Publication-ready scientific plotting for Python #

SciPlot-PyQt (aka SciPlot) is a user-interface/matplotlib wrapper built with
PyQt5 that allows interactive plotting through an embedded matplotlib canvas.
It enables fast and easy publication-ready plots and images:
* Interactive plotting
* Theme and style editing (TODO)
* Figure saving and opening for later editing (TODO)

## Dependencies ##

Note: These are the developmental system specs. Older versions of certain
packages may work.

* Python >= 3.4
* Numpy (1.9.3)
* PyQT5 (5.5.1 or 5.6.0)
* Matplotlib (1.5.0rc3)

## Known Issues ##
1. SciPlot has problems when imported and ran via sciplot.main() or %run from within IPython. It appears to 
work as expected when called through a normal Python interpreter.

2. There is a bug in PyQt 5.7.* that will prevent SciPlot's tables from showing the individual plot entries 
(see https://www.riverbankcomputing.com/pipermail/pyqt/2017-January/038483.html). Apparently, this will be fixed in 5.7.2.

* As WinPython 3.5.2.3Qt5 and 3.5.2.2Qt5 use PyQt 5.7.*, it is advised to use WinPython 3.5.2.1Qt5 or 3.4.4.5Qt5 until the matter is sorted out.
* Alternatively, one can uninstall pyqt5.7.* and force an install of <= 5.6.*.

## Installation ##
```
# Make new directory for crikit2 and enter it
# Clone from github
git clone https://github.com/CCampJr/SciPlot-PyQt.git

# Install (mainly check installation)
pip install -e .

# IMPORTANT: You will need to manually install PyQt5 and Qt5
# These packages are not pip-installable at this time
```

## Usage ##
```Python
import sciplot
sp = sciplot.main()
```

## Example ##
```Python
sp.plot((0,1),(2,3),label='Line', x_label='X', y_label='Y', ls='--')
sp.fill_between((0,1),(1,2),(3,4),label='Fill Between', color='r', alpha=0.25)
```
![Screenshot.png](./Screenshot.png)

```Python
sp.hist(r, bins=100, label='Histogram', color=[0, .2, .3],
        x_label='Amplitude', y_label='Counts', alpha=0.5)
```
![Screenshot2.png](./Screenshot2.png)

```Python
sp.imshow(r, clim=[25,75], cmap='viridis', label='Imshow', x_label='X (pix)', 
          y_label='Y (pix)')
```
![Screenshot3.png](./Screenshot3.png)

### NONLICENSE ###
This software was developed at the National Institute of Standards and Technology (NIST) by
employees of the Federal Government in the course of their official duties. Pursuant to
[Title 17 Section 105 of the United States Code](http://www.copyright.gov/title17/92chap1.html#105),
this software is not subject to copyright protection and is in the public domain.
NIST assumes no responsibility whatsoever for use by other parties of its source code,
and makes no guarantees, expressed or implied, about its quality, reliability, or any other characteristic.

Specific software products identified in this open source project were used in order
to perform technology transfer and collaboration. In no case does such identification imply
recommendation or endorsement by the National Institute of Standards and Technology, nor
does it imply that the products identified are necessarily the best available for the
purpose.

### Contact ###
Charles H Camp Jr: [charles.camp@nist.gov](mailto:charles.camp@nist.gov)

### Contributors ###
Charles H Camp Jr, Mona Lee
