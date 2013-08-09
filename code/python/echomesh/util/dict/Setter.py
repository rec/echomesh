from __future__ import absolute_import, division, print_function, unicode_literals

def setter(table, address):
  for part in address[:-1]:
    table = table[part]

  return table, address[-1]

def apply_function(table, function, *addresses):
  for address in addresses:
    table, part = setter(table, address)
    table[part] = function(table[part])

