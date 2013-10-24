from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'FooBar',
    ext_modules = cythonize('tiny.pyx')
)