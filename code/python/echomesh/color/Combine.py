from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

def combine(data):
  result = cechomesh.ColorList()
  result.combine(*data)
  return result
