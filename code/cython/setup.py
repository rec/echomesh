## Run python setup.py build_ext to build echomesh.so

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Echomesh',
  ext_modules = cythonize('echomesh.pyx')
)
