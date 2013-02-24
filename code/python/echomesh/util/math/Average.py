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
    if len(items) == window:
      yield total / window
      items = []
      total = 0
  if partial and items:
    yield total / len(items)

def average(generator, moving_window=1, grouped_window=1, partial=True):
  if grouped_window and grouped_window > 1:
    generator = grouped_average(generator, grouped_window, partial)
  if moving_window or moving_window > 1:
    generator = moving_average(generator, moving_window)

  return generator
