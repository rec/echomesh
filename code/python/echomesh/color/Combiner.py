from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from six.moves import xrange

import cechomesh

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

def combine_to_bytearray(array, lighters, brightness):
  for i in xrange(int(len(array) / 3)):
    for j in xrange(3):
      b = 0
      for light in lighters:
        if i < len(light) and light[i] is not None:
          b = max(b, light[i][j])
      array[3 * i + j] = min(0xFF, int(0x100 * b * brightness))

def ccombine(data):
  if not data:
    return []

  data = [cechomesh.to_color_list(d) for d in data]
  lights = data.pop()
  lights.combine(*data)
  return lights

