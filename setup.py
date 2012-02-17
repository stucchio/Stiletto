#!/usr/bin/env python

from distutils.core import setup

setup(name='Stiletto',
      version='0.1',
      description='Pre-render views for django.',
      author='Chris Stucchio',
      author_email='stucchio@gmail.com',
      url='https://github.com/stucchio/Stiletto',
      packages = ['stiletto', 'stiletto.management', 'stiletto.management.commands'],
     )
