from __future__ import absolute_import, division, print_function, unicode_literals

import six

def setter(table, *address):
  for part in address[:-1]:
    try:
      table = table[part]
    except:
      return None, None

  return table, address[-1]

def apply_list(table, function, *addresses):
  for address in addresses:
    table, part = setter(table, *address)
    if table:
      table[part] = function(table[part])
  return table

def apply_dict(table, function, addresses):
  def recurse(table, addresses, key):
    try:
      items = six.iteritems(addresses)
    except:
      table[key] = function(table[key])
    else:
      for subkey, subaddresses in items:
        recurse(table[key] if key else table, subaddresses, subkey)
  recurse(table, addresses, None)
  return table

def list_to_dict(*addresses):
  return apply_list({}, lambda x: True, *addresses)
