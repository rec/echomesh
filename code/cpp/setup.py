#!/usr/bin/env python

## Run python setup.py build_ext to build echomesh.so

import os

import platform

from distutils.core import setup, Command, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext, extension
from Cython.Compiler import Options

DEBUG = not True

PLATFORM = platform.system().lower()

IS_LINUX = (PLATFORM == 'linux')
IS_MAC = (PLATFORM == 'darwin')
IS_WINDOWS = (PLATFORM == 'windows')

assert IS_LINUX or IS_MAC or IS_WINDOWS

MODULE_NAME = 'cechomesh_debug' if DEBUG else 'cechomesh'
PYX_FILES = ['cechomesh.pyx']
LIBRARIES = ['echomesh', 'pthread']

DEBUG_ARGS = {
  'cython_gdb': True,
  'pyrex_gdb': True,
  }
EXTRA_ARGS = DEBUG_ARGS if DEBUG else {}

EXTRA_COMPILE_ARGS = ['-I.']
if IS_MAC:
  EXTRA_COMPILE_ARGS += ('-x c++ -arch x86_64 -fmessage-length=0 -std=c++11 '
                         '-stdlib=libc++ -IJuceLibraryCode -O0'.split())
  EXTRA_LINK_ARGS = '-framework Cocoa -framework WebKit -framework CoreMidi'.split()

  if DEBUG:
    EXTRA_COMPILE_ARGS += ('-O0 -g -D_DEBUG=1 -DDEBUG=1').split()
    EXTRA_LINK_ARGS += ['-g']
    LIB_DIRS = ['Builds/MacOSX/build/Debug']

  else:
    EXTRA_COMPILE_ARGS += ('-O2'.split())
    LIB_DIRS = ['Builds/MacOSX/build/Release']

else:
  raise Exception("Don't understand platform %s." % platform)

class CleanCommand(Command):
  description = "custom clean command that forcefully removes dist/build directories"
  user_options = []
  def initialize_options(self):
    self.cwd = None

  def finalize_options(self):
    self.cwd = os.getcwd()

  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    os.system('rm -Rf %s.so ./build ./dist echomesh.cpp' % MODULE_NAME)

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
    'clean': CleanCommand},
  ext_modules=cythonize(
    [echomesh_extension],
    **EXTRA_ARGS),
  )

# Typical use: python setup.py build_ext --inplace
