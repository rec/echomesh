from __future__ import absolute_import, division, print_function

#!/usr/bin/env python

import os
import os.path
import shutil
import sys

if 'build_ext' in sys.argv:
  index = sys.argv.index('build_ext') + 1
  if sys.argv[index] != '--inplace':
    sys.argv.insert(index, '--inplace')

ECHOMESH_BASE = os.path.dirname(os.path.dirname(os.path.dirname(
  os.path.abspath(__file__))))
ECHOMESH_PATH = os.path.join(ECHOMESH_BASE, 'code', 'python')

sys.path.append(ECHOMESH_PATH)

import Config

from distutils.core import setup, Command
from Cython.Build import cythonize
from Cython.Distutils import build_ext, extension

from echomesh.base import Platform

DEBUG = True

CONFIG = Config.Config(DEBUG, ECHOMESH_BASE)

MODULE_NAME = 'cechomesh'
LIBRARY_NAME = '%s.so' % MODULE_NAME
PYX_FILES = ['cechomesh.pyx']
LIBRARIES = ['echomesh', 'pthread', 'glog']

DEBUG_ARGS = {
  'cython_gdb': True,
  'pyrex_gdb': True,
  }
EXTRA_ARGS = DEBUG_ARGS if DEBUG else {}

LIB_DIRS = ['build/lib', CONFIG.echomesh_lib]

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


print(type(CONFIG.module_name))
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

