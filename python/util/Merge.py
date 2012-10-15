from __future__ import absolute_import, division, print_function, unicode_literals

import copy

def merge(old, new):
  """Merges a new item into an old item.

  If the old item is a dictionary, returns a dictionary with the keys from both
  the old and new items and calling merge_items recursively whenever a key
  exists in both old and new.  Otherwise, it returns a copy of the new item.

  Note that lists are overwritten and not appended.
  """
  if type(old) is type({}):
    old = copy.deepcopy(old)
    for k, v in new.iteritems():
      old[k] = merge(old.get(k, None), v)
    return old

  else:
    return copy.deepcopy(new)

def merge_all(*items):
  result = {}
  for i in items:
    result = merge(result, i)
  return result
