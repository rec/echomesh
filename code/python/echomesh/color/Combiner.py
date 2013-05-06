from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.base import Config

USE_NUMPY = False

def combine(combiner, *lighters):
  linverse = itertools.izip_longest(*lighters)
  if USE_NUMPY:
    import numpy
    return numpy.array([combiner(z) for z in linverse])
  else:
    return [combiner(z) for z in linverse]

def first(items):
  return items[0]

def sup(items):
  light = [0, 0, 0]
  for item in items:
    if item is not None:
      for j in xrange(3):
        light[j] = max(light[j], item[j])
  return light

def combine_to_bytearray(bytes, lighters, brightness):
  for i in xrange(int(len(bytes) / 3)):
    for j in xrange(3):
      b = 0
      for light in lighters:
        if i < len(light) and light[i] is not None:
          b = max(b, light[i][j])
      bytes[3 * i + j] = min(0xFF, int(0x100 * b * brightness))


# We could put HSV combiners in here.

