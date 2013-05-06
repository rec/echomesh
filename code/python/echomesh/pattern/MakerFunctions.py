from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.color import ColorTable
from echomesh.base import Config

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

def concatenate(light_sets):
  return list(itertools.chain(*light_sets))

def inject(light_sets, mapping, length):
  """
    mapping:
      Maps a light index in the result to the light index in the original
      light_set.  We need a reverse mapping because we need a way to map one
      light in the input to many lights in the output.

  """
  assert len(light_sets) == 1
  light_set = light_sets[0]

  def _map(i):
    x = mapping.get(i)
    return x is not None and light_set[x]

  return [_map(i) for i in range(max(int(length), 0))]

def insert(light_sets, target=None, begin=None, length=None, rollover=True,
           skip=None):
  assert len(light_sets) == 1
  light_set = light_sets[0]

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

def transpose(light_sets, x=None, y=None, reverse_x=False, reverse_y=False):
  assert len(light_sets) == 1
  light_set = light_sets[0]
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

# The Python built-in works perfectly.
def reverse(light_sets):
  assert len(light_sets) == 1
  light_set = light_sets[0]
  return reversed(light_set)

