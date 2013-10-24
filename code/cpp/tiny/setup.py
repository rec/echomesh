## Run python setup.py build_ext 
## It will build the tiny.so that is useable.

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'FooBar',
    ext_modules = cythonize('tiny.pyx')
)
