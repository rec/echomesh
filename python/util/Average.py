from __future__ import absolute_import, division, print_function, unicode_literals

def moving_average(generator, window):
  items = []
  total = 0
  for x in generator:
    items.append(x)
    total += x
    if len(items) >= window:
      if len(items) > window:
        total -= items.pop(0)
      yield total / window

def grouped_average(generator, window, partial=True):
  items = []
  total = 0
  for x in generator:
    items.append(x)
    total += x
    if len(items) is window:
      yield total / window
      items = []
      total = 0
  if partial and items:
    yield total / len(items)

def average(generator, moving=0, grouped=0, partial=True):
  if grouped:
    generator = grouped_average(generator, grouped, partial)
  if moving:
    generator = moving_average(generator, moving)

  return generator
