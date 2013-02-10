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
        if require_old_key:
          raise Exception('Tried to override non-existent key ' + new_path)
      else:
        continue

    if isinstance(old_v, dict):
      if isinstance(new_v, dict):
        _merge_or_diff(is_merge, old_v, new_v, new_path, require_old_key)
      else:
        raise Exception('Tried to override dict with non-dict for key ' +
                        new_path)

    elif not isinstance(new_v, dict):
      if is_merge:
        old[key] = new_v
      else:
        del old[key]

    elif require_old_key:
      raise Exception('Tried to override non-dict with dict for key ' +
                      new_path)

    elif is_merge:
      old[key] = new_v

  return old

def merge_strict(old, new):
  return _merge_or_diff(True, old, new, True)

def merge(old, new):
  return _merge_or_diff(True, old, new, False)

def difference_strict(old, new):
  return _merge_or_diff(False, old, new, True)

def difference(old, new):
  return _merge_or_diff(False, old, new, False)

def merge_all_strict(target, *others):
  return reduce(merge_strict, others, target)

def merge_all(target, *others):
  return reduce(merge, others, target)

"""
>>> Merge.merge_strict({1:2, 3:5}, {1:4, 2:7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge_all_strict({1:2, 3:5}, {1:4, 2:7}, {1:23, 5:1000})
{1: 23, 2: 7, 3: 5, 5: 1000}
"""
