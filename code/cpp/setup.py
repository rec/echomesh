#!/usr/bin/env python

# Typical command:
#   setup.py library build_ext install

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import sys

from distutils.core import setup
from Cython.Distutils import build_ext

if 'build_ext' in sys.argv:
  index = sys.argv.index('build_ext') + 1
  if index >= len(sys.argv) or sys.argv[index] != '--inplace':
    sys.argv.insert(index, '--inplace')


ECHOMESH_BASE = os.path.dirname(os.path.dirname(os.path.dirname(
  os.path.abspath(__file__))))
ECHOMESH_PATH = os.path.join(ECHOMESH_BASE, 'code', 'python')

sys.path.append(ECHOMESH_PATH)

from echomesh.build import clean_older, CONFIG, Clean, Install, Library

clean_older()

setup(
  name='Echomesh',

  cmdclass={
    'build_ext': build_ext,
    'clean': Clean,
    'install': Install,
    'library': Library,
    },

  ext_modules=CONFIG.modules
)

