from __future__ import absolute_import, division, print_function, unicode_literals

def light_count(get):
  count = get('light', 'count')
  if not count:
    size = get('light', 'visualizer', 'layout')
    count = size[0] * size[1]
  return count

