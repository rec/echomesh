#!/usr/bin/env python

## Run python setup.py build_ext to build echomesh.so

import os

from distutils.core import setup, Command, Extension
from Cython.Build import cythonize

# Link line is:
# c++ -framework Cocoa -framework WebKit -bundle -undefined dynamic_lookup -L/usr/local/lib -L/usr/local/opt/sqlite/lib build/temp.macosx-10.8-x86_64-2.7/echomesh.o build/temp.macosx-10.8-x86_64-2.7/Source/Tiny.o -L/development/echomesh/code/cython/Builds/MacOSX/build/Debug -lechomesh -o /development/echomesh/code/cython/echomesh.so

# invocation line is
# cd /development/echomesh/code/cython && CC="cc -IJuceLibraryCode" CXX="c++ -IJuceLibraryCode" python setup.py build_ext --inplace

lib = Extension(
  'echomesh',
  ['echomesh.pyx'],
  library_dirs=['/development/echomesh/code/cython/Builds/MacOSX/build/Debug'],
  libraries=['echomesh'],
  extra_compile_args=['-x', 'c++', '-arch', 'x86_64', '-fmessage-length=0', '-std=c++11', '-IJuceLibraryCode'],
  extra_link_args=['-framework', 'Cocoa', '-framework', 'WebKit'],
  )

class CleanCommand(Command):
  description = "custom clean command that forcefully removes dist/build directories"
  user_options = []
  def initialize_options(self):
    self.cwd = None

  def finalize_options(self):
    self.cwd = os.getcwd()

  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    os.system('rm -Rf echomesh.so ./build ./dist')

setup(
  name='Echomesh',
  ext_modules=cythonize([lib]),
  cmdclass={'clean': CleanCommand},
  )
