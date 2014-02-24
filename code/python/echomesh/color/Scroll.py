from __future__ import absolute_import, division, print_function, unicode_literals

def _scroll(items, dx, dy, x, empty=None, wrap=False):
  if abs(dx) >= x or abs(dy) >= len(items) / x:
    return [empty] * len(items)

  if dx > 0:
    items = items[:]
    for i in xrange(len(items) - 1, -1, -1):
      m = i % x
      items[i] = items[i - dx] if m >= dx else empty
  elif dx < 0:
    items = items[:]
    for i in xrange(len(items)):
      m = i % x
      rollover = (m < x + dx) and (i - dx < len(items))
      items[i] = items[i - dx] if rollover  else empty

  if dy > 0:
    items = ([empty] * (dy * x) + items)[:len(items)]
  elif dy < 0:
    items = items[-dy * x:] + [empty] * (-dy * x)
  return items

def scroll(colors, dx, dy, x_size, empty=None, smooth=True, wrap=False):
  bx, by = int(dx), int(dy)
  if (not smooth) or (bx == dx and by == dy):
    return _scroll(colors, dx, dy, x_size, empty, wrap)
