#!/usr/bin/env python

import os
import os.path
import platform
import shutil
import sys

if 'build_ext' in sys.argv:
  sys.argv.insert(sys.argv.index('build_ext') + 1, '--inplace')

from distutils.core import setup, Command
from Cython.Build import cythonize
from Cython.Distutils import build_ext, extension

ECHOMESH_BASE = os.path.dirname(os.path.dirname(os.path.dirname(
  os.path.abspath(__file__))))
ECHOMESH_PATH = os.path.join(ECHOMESH_BASE, 'code', 'python')

sys.path.append(ECHOMESH_PATH)

from echomesh.base import Platform

DEBUG = True

MODULE_NAME = 'cechomesh_debug' if (DEBUG and False) else 'cechomesh'
PYX_FILES = ['cechomesh.pyx']
LIBRARIES = ['echomesh', 'pthread', 'glog']

DEBUG_ARGS = {
  'cython_gdb': True,
  'pyrex_gdb': True,
  }
EXTRA_ARGS = DEBUG_ARGS if DEBUG else {}

EXTRA_COMPILE_ARGS = (
  '-I. -x c++ -arch x86_64 -fmessage-length=0 -std=c++11 '
  '-stdlib=libc++ -IJuceLibraryCode -Ibuild/include').split()

LIB_DIRS = ['build/lib']

if Platform.PLATFORM == Platform.MAC:
  EXTRA_LINK_ARGS = '-framework Cocoa -framework WebKit -framework CoreMidi'.split()

  if DEBUG:
    EXTRA_COMPILE_ARGS += ('-O0 -g -D_DEBUG=1 -DDEBUG=1').split()
    EXTRA_LINK_ARGS += ['-g']
    LIB_DIRS += ['Builds/MacOSX/build/Debug']

  else:
    EXTRA_COMPILE_ARGS += ('-O2'.split())
    LIB_DIRS += ['Builds/MacOSX/build/Release']

elif Platform.PLATFORM == Platform.UBUNTU:
    EXTRA_LINK_ARGS = ('-lc++ -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound '
                      '-ldl -lfreetype -lpthread -lrt -lglog').split()

    if DEBUG:
        EXTRA_COMPILE_ARGS += ('-O0 -g -D_DEBUG=1 -DDEBUG=1').split()
        EXTRA_LINK_ARGS += ['-g']
        LIB_DIRS += ['Builds/Ubuntu/build']

    else:
        EXTRA_COMPILE_ARGS += ('-02'.split())
        LIB_DIRS += ['Builds/Ubuntu/build/Release']


else:
  raise Exception("Don't understand platform %s." % platform)


class CleanCommand(Command):
  description = 'Complete clean command'
  user_options = []
  def initialize_options(self):
    self.cwd = None

  def finalize_options(self):
    self.cwd = os.getcwd()

  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    os.system('rm -Rf %s.so ./build/temp* ./dist echomesh.cpp' % MODULE_NAME)


class InstallCommand(Command):
  description = 'Install library in bin directory.'
  user_options = []
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    bin_dir = os.path.join(ECHOMESH_BASE, 'bin', Platform.PLATFORM)
    shutil.copy('%s.so' % MODULE_NAME, bin_dir)


echomesh_extension = extension.Extension(
  MODULE_NAME,
  PYX_FILES,
  library_dirs=LIB_DIRS,
  libraries=LIBRARIES,
  extra_compile_args=EXTRA_COMPILE_ARGS,
  extra_link_args=EXTRA_LINK_ARGS,
  **EXTRA_ARGS)

setup(
  name='Echomesh',

  cmdclass={
    'build_ext': build_ext,
    'clean': CleanCommand,
    'install': InstallCommand,
    },

    ext_modules=cythonize(
    [echomesh_extension],
    **EXTRA_ARGS),
  )

