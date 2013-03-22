from __future__ import absolute_import, division, print_function, unicode_literals

import numpy

# We define a transform as pair of functions from [0, 1] -> [0, 1]
# such that f[0](f[1](x)) = f[1](f(0)[x] = x

def inverse(x):
  return x[1], x[0]

_ID = lambda x: x

IDENTITY = _ID, _ID

SQUARE = lambda x: x * x, numpy.sqrt

def power(n):
  return lambda x: numpy.power(x, n), lambda x: numpy.power(x, 1.0 / n)

SINE = (lambda x: (1 + numpy.sin(numpy.pi * (x - 0.5))) / 2,
        lambda x: 0.5 + numpy.arcsin(2 * x - 1) / numpy.pi)

EXP = (lambda x: (numpy.exp(x) - 1) / (numpy.e - 1),
       lambda x: numpy.log((numpy.e - 1) * x + 1))

