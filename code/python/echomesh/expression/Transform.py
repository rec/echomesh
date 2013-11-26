from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util.registry import Registry
from echomesh.util import Log

if Config.get('load_module', 'numpy'):
  import numpy as math
  pow = math.power
else:
  import math
  pow = math.pow


LOGGER = Log.logger(__name__)

REGISTRY = Registry.Registry('transforms')

# We define a transform as pair of functions f0, f1 from [0, 1] -> [0, 1]
# such that f0(f1(x)) = f1(f0(x)) = x

def inverse(x):
  return x[1], x[0]

def identity(x):
  return x

def reverse(x):
  return 1.0 - x

def square(x):
  return x * x

def power(n):
  def pwr(x):
    return pow(x, n)
  def pwr_inverse(x):
    return pow(x, 1.0 / n)
  return pwr, pwr_inverse

def sine(x):
  return (1 + math.sin(math.pi * (x - 0.5))) / 2

def arcsine(x):
  return 0.5 + math.arcsin(2 * x - 1) / math.pi

def exp(x):
  return (math.exp(x) - 1) / (math.e - 1)

def log(x):
  return math.log((math.e - 1) * x + 1)

IDENTITY = identity, identity
SQUARE = square, math.sqrt
REVERSE = reverse, reverse
SINE = sine, arcsine
EXP = exp, log

REGISTRY.register(power(3), 'cube',
                  help_text="""\
The cube transform is like the square transform, but more dramatic.""")

REGISTRY.register(EXP, 'exponential',
                  help_text="""\
The exponential transform converts power curves into amplitude curves.""")

REGISTRY.register(IDENTITY, 'identity',
                  help_text="""\
The identity transformation has no effect.""")

REGISTRY.register(inverse, 'inverse',
                  help_text="""\
The inverse transform is a special case that cannot stand alone and cannot
appear as the first transform in a series.
It takes the inverse of transform that it is attached to.

For example, you can talk about the transform identity.inverse, which is
the same as identity, or square.inverse, which is the same as sqrt, but you
can't talk about the transform inverse or inverse.sine, as neither of these
make any sense.""")

REGISTRY.register(REVERSE, 'reverse',
                  help_text="""\
Reverses the result of a transform, so [0, 1] is mapped directly onto
[1, 0].  Really useful to apply before or after another transform.""")

REGISTRY.register(SINE, 'sine',
                  help_text="""\
A half-period sine wave scaled to run from 0 to 1.  Has the nice property that
the derivative is zero at both 0 and 1.""")

REGISTRY.register(SQUARE, 'square',
                  help_text="""\
The square transform starts off completely flat and then accelerates as it
approaches 1.0.""")

REGISTRY.register(inverse(SQUARE), 'sqrt',
                  help_text="""\
The inverse of the "square" transform, this acccelerates rapidly at
the start and then slows down as it approaches 1.0.""")

def compose(f, g):
  ff, fi = f
  gg, gi = g

  def composed_function(x):
    return gg(ff(x))

  def composed_function_inverse(x):
    return fi(gi((x)))

  return composed_function, composed_function_inverse

def transform(name):
  if name:
    result = None
    parts = name.split('.')
    for part in parts:
      try:
        transform = REGISTRY.function(part)
      except:
        LOGGER.error("Transform: bad part %s in name %s.", part, name)
        break
      if transform is inverse:
        if not result:
          LOGGER("Can't start a transform with inverse: %s" % name)
          break
        result = inverse(result)
      else:
        result = compose(result, transform) if result else transform

  return IDENTITY
