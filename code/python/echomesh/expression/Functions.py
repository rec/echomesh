from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.base import Version
from echomesh.util.registry import Registry

MATH_FUNCTIONS = [
  'acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil', 'cos', 'cosh',
  'degrees', 'exp', 'fabs', 'factorial', 'floor', 'frexp', 'isinf', 'isnan',
  'log', 'log10', 'log1p', 'modf', 'radians', 'sin', 'sinh', 'sqrt', 'tan',
  'tanh', 'trunc']

if Version.IS_27:
  MATH_FUNCTIONS += ['erf', 'erfc',  'expm1',  'gamma', 'lgamma']

def _function_register():
  register = Registry.Registry('Functions')

  for f in MATH_FUNCTIONS:
    register.register(getattr(math, f))

  register.register(int)
  return register

FUNCTIONS = _function_register()
