from __future__ import absolute_import, division, print_function, unicode_literals

import copy

def merge(old, new, path=[]):
  """Merges two dictionaries, mutating the dictionary "old"."""
  nothing = ()
  for key, new_v in new.iteritems():
    new_path = path + [key]
    old_v = old.get(key, nothing)

    if old_v is nothing:
      raise Exception('Tried to override non-existent key ' +
                      ':'.join(new_path))

    if isinstance(old_v, dict):
      if isinstance(new_v, dict):
        merge(old_v, new_v, new_path)
      else:
        raise Exception('Tried to override dict with non-dict for key ' +
                        ':'.join(new_path))

    elif old_v is nothing or not isinstance(new_v, dict):
      old[key] = new_v

    else:
      raise Exception('Tried to override non-dict with dict for key ' +
                      ':'.join(new_path))

  return old

def merge_all(target, *others):
  return reduce(merge, others, target)

def difference(old, new):
  """
  Returns the elements that are different between two dictionaries, recursively.
  """
  nothing = ()
  for key, new_v in new.iteritems():
    old_v = old.get(key, nothing)

    if old_v is nothing:
      continue

    if isinstance(old_v, dict):
      if isinstance(new_v, dict):
        difference(old_v, new_v)
        if not old_v:
          del old[key]
      else:
        raise Exception('Tried to override dict with non-dict for key ' + key)

    elif not isinstance(new_v, dict):
      del old[key]

    else:
      raise Exception('Tried to override non-dict with dict for key ' + key)

  return old


"""
>>> Merge.merge({1:2, 3:5}, {1:4, 2:7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge_all({1:2, 3:5}, {1:4, 2:7}, {1:23, 5:1000})
{1: 23, 2: 7, 3: 5, 5: 1000}
"""
