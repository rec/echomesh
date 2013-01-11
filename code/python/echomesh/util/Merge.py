from __future__ import absolute_import, division, print_function, unicode_literals

import copy

def merge(old, new):
  """Merges two dictionaries, mutating the dictionary "old"."""
  nothing = ()
  for key, new_v in new.iteritems():
    old_v = old.get(key, nothing)

    if old_v is nothing:
      raise Exception('Tried to override non-existent key ' + key)

    if isinstance(old_v, dict):
      if isinstance(new_v, dict):
        old[key] = merge(old_v, new_v)
      else:
        raise Exception('Tried to override dict with non-dict for key ' + key)

    elif old_v is nothing or not isinstance(new_v, dict):
      old[key] = new_v

    else:
      raise Exception('Tried to override non-dict with dict for key ' + key)

  return old

def merge_all(target, *others):
  return reduce(merge, others, target)

"""
>>> Merge.merge({1:2, 3:5}, {1:4, 2:7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge_all({1:2, 3:5}, {1:4, 2:7}, {1:23, 5:1000})
{1: 23, 2: 7, 3: 5, 5: 1000}
"""
