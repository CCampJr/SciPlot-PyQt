# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 01:11:04 2016

@author: chc
"""

from setuptools import setup, find_packages

with open('README.rst') as f:
      long_description = f.read()

setup(name='sciplot-pyqt',
      version = '0.2.0rc0',
      description = 'A small matplotlib wrapper/UI for creating \
                     publication-ready plots, graphs, and images',
      long_description = long_description,
      url = 'http://github.com/CCampJr/SciPlot-PyQt',
      author = 'Charles H. Camp Jr.',
      author_email = 'charles.camp@nist.gov',
      license = 'NONLICENSE',
      packages = find_packages(),
      zip_safe = False,
      include_package_data = True,
      install_requires=['numpy','matplotlib'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Visualization'])