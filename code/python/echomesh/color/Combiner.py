from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def apply_processor(function, lighter):
  if callable(lighter):
    def func(t):
      return function(lighter(t))
    return func
  else:
    return function(lighter)

def applier(function):
  def f(light_set):
    return [function(light) for light in light_set]
  return f

# The Python built-in works perfectly.
reverse = reversed

# Must set one of length or target.
def insert(light_set, length=None, target=None, offset=None, skip=None,
           rollover=False):
  skip = int(skip or 1)
  offset = int(offset or 0)
  if length is None and target is None:
    length = offset + len(light_set) * skip
  result = target or ([None] * length)
  if length is None:
    length = len(result)
  else:
    assert length >= 0

  index = offset
  for light in light_set:
    while index >= length:
      index -= length
    result[index] = light
    index += skip

    if not rollover and index >= length:
      break

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

  return [_map(i) for i in range(length)]

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

# We could put HSV combiners in here.
