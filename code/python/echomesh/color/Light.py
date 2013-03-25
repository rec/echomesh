from __future__ import absolute_import, division, print_function, unicode_literals

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

def insert(light_set, length, target=None, offset=0, interleave=1):
  result = target or ([None] * length)

  index = offset
  for light in light_set:
    result[index] = light
    index += interleave

  return result

def inject(light_set, reverse_mapping, length):
  """
    reverse_mapping:
      Maps a light index in the result to the light index in the original
      light_set.  We need a reverse mapping because we need a way to map one
      light in the input to many lights in the output.

  """
  def _map(i):
    x = reverse_mapping.get(i)
    return x is not None and light_set[x]

  return [_map(i) for i in range(length)]


def combine(combiner, *lighters):
  return [combiner(z) for z in zip(*lighters)]

def first(items):
  return items[0]

def sup(items):
  return [max(*i) for i in zip(*items)]

def inf(items):
  return [min(*i) for i in zip(*items)]

# We could put HSV combiners in here.
