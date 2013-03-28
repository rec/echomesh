from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.util import Registry


MATH_FUNCTIONS = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil',
                  'cos', 'cosh', 'degrees', 'erf', 'erfc', 'exp', 'expm1',
                  'fabs', 'factorial', 'floor', 'frexp', 'gamma', 'isinf',
                  'isnan', 'lgamma', 'log', 'log10', 'log1p', 'modf',
                  'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc']

def _function_register():
  register = Registry.Registry('Functions')

  for f in MATH_FUNCTIONS:
    register.register(getattr(math, f))
  register.register(int)
  return register

FUNCTIONS = _function_register()
