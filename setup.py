# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 01:11:04 2016

@author: chc
"""

from setuptools import setup, find_packages

setup(name='sciplot-pyqt',
      version = '0.1.4',
      description = 'A small matplotlib wrapper/UI for creating \
                     publication-ready plots, graphs, and images',
      url = 'http://github.com/CCampJr/SciPlot-PyQt',
      author = 'Charles H. Camp Jr.',
      author_email = 'charles.camp@nist.gov',
      license = 'NONLICENSE',
      packages = find_packages(),
      zip_safe = False,
      include_package_data = True,
      install_requires=['numpy','matplotlib'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Visualization'])