from __future__ import absolute_import, division, print_function, unicode_literals

import copy

def _merge_or_diff(is_merge, old, new, require_old_key, path=''):
  """Merges two dictionaries, mutating the dictionary "old"."""
  nothing = ()
  for key, new_v in new.iteritems():
    new_path = '%s:%s' % (path, key)
    old_v = old.get(key, nothing)

    if old_v is nothing:
      if is_merge:
        if require_old_key
        raise Exception('Tried to override non-existent key ' +
                        ':'.join(new_path))
      else:
        continue

    if isinstance(old_v, dict):
      if isinstance(new_v, dict):
        merge_or_diff(is_merge, old_v, new_v, new_path, require_old_key)
      else:
        raise Exception('Tried to override dict with non-dict for key ' +
                        ':'.join(new_path))

    elif not isinstance(new_v, dict):
      if is_merge:
        old[key] = new_v
      else:
        del old[key]

    else:
      raise Exception('Tried to override non-dict with dict for key ' +
                      ':'.join(new_path))

  return old

def merge(old, new, require_old_key=True):
  return _merge_or_diff(True, old, new, require_old_key)

def difference(old, new, require_old_key=True):
  return _merge_or_diff(False, old, new, require_old_key)

def merge_all(target, *others):
  return reduce(merge, others, target)

"""
>>> Merge.merge({1:2, 3:5}, {1:4, 2:7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge_all({1:2, 3:5}, {1:4, 2:7}, {1:23, 5:1000})
{1: 23, 2: 7, 3: 5, 5: 1000}
"""
