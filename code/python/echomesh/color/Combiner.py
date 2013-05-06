from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.color import ColorTable
from echomesh.base import Config

USE_NUMPY = False

# The Python built-in works perfectly.
reverse = reversed

def insert(light_set, target=None, begin=None, length=None, rollover=True,
           skip=None):
  skip = int(skip or 1)
  begin = int(begin or 0)
  if length is None:
    length = Config.get('light', 'count') if target is None else len(target)

  result = target or ([None] * length)
  for i, light in enumerate(light_set):
    index = begin + i
    if index < 0 or index >= length:
      if rollover:
        index = index % length
      else:
        continue
    result[index] = light

  return result

def inject(light_set, mapping, length):
  """
    mapping:
      Maps a light index in the result to the light index in the original
      light_set.  We need a reverse mapping because we need a way to map one
      light in the input to many lights in the output.

  """
  def _map(i):
    x = mapping.get(i)
    return x is not None and light_set[x]

  return [_map(i) for i in range(max(int(length), 0))]

def choose(light_sets, choose=None):
  length = len(light_sets)
  def restrict(size):
    return int(max(0, min(length - 1, size)))

  if callable(choose):
    # TODO: there's no way to specify callables to choose.
    zipped = itertools.izip_longest(*light_sets)
    return [vec[restrict(choose(i))] for i, vec in enumerate(zipped)]
  else:
    return light_sets[restrict(choose)]

def combine(combiner, *lighters):
  linverse = itertools.izip_longest(*lighters)
  if USE_NUMPY:
    import numpy
    return numpy.array([combiner(z) for z in linverse])
  else:
    return [combiner(z) for z in linverse]

def concatenate(light_sets):
  return list(itertools.chain(*light_sets))

def transpose(light_set, x=None, y=None, reverse_x=False, reverse_y=False):
  if not (x and y):
    default_x, default_y = Config.get('light', 'visualizer', 'layout')
    x = x or default_x
    y = y or default_y

  result = [None] * len(light_set)
  for i, light in enumerate(light_set):
    my_x = i % x;
    my_y = i // x;
    if reverse_x:
      my_x = x - my_x - 1
    if reverse_y:
      my_y = y - my_y - 1
    index = my_x * y + my_y
    if index < len(result):
      result[index] = light
  return result

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

