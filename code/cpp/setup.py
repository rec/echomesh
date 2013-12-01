#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import sys

if 'build_ext' in sys.argv:
  index = sys.argv.index('build_ext') + 1
  if sys.argv[index] != '--inplace':
    sys.argv.insert(index, '--inplace')

from Config import CONFIG

from distutils.core import setup, Command
from Cython.Build import cythonize
from Cython.Distutils import build_ext, extension


class CleanCommand(Command):
  description = 'Complete clean command'
  user_options = []
  def initialize_options(self):
    self.cwd = None

  def finalize_options(self):
    self.cwd = os.getcwd()

  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    os.system('rm -Rf %s.so ./build/temp* ./dist echomesh.cpp' %
              CONFIG.module_name)


class InstallCommand(Command):
  description = 'Install library in bin directory.'
  user_options = []
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    print('Copying %s to %s' % (CONFIG.library_name, CONFIG.bin_dir))
    shutil.copy(CONFIG.library_name, CONFIG.bin_dir)


echomesh_extension = extension.Extension(
  CONFIG.module_name,
  CONFIG.pyx_files,
  library_dirs=CONFIG.lib_dirs,
  libraries=CONFIG.libraries,
  extra_compile_args=CONFIG.extra_compile_args,
  extra_link_args=CONFIG.extra_link_args,
  **CONFIG.extra_args)

setup(
  name='Echomesh',

  cmdclass={
    'build_ext': build_ext,
    'clean': CleanCommand,
    'install': InstallCommand,
    },

    ext_modules=cythonize([echomesh_extension], **CONFIG.extra_args),
  )

