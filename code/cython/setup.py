## Run python setup.py build_ext to build echomesh.so

import os

from distutils.core import setup, Command, Extension
from Cython.Build import cythonize

lib = Extension('echomesh',
                ['echomesh.pyx'],
                library_dirs=['/development/echomesh/code/cython/Builds/MacOSX/build/Debug'],
                libraries=['echomesh'],
#                extra_compile_args=['-arch i386'],
#                extra_link_args=['-arch i386'],
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
