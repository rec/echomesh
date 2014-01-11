from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

def ccombine(data):
  if not data:
    return cechomesh.ColorList()

  data = [cechomesh.to_color_list(d) for d in data]
  lights = data.pop()
  lights.combine(*data)
  return lights

