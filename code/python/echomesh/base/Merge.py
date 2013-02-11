from __future__ import absolute_import, division, print_function, unicode_literals

import copy

def _merge_or_diff(old, new, is_merge, require_old_key, path=''):
  """Merges two dictionaries, mutating the dictionary "old"."""
  nothing = ()

  if old is None:
    old = {}
    require_old_key = False
  else:
    # old = copy.deepcopy(old)
    pass

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
        _merge_or_diff(old_v, new_v, is_merge, new_path, require_old_key)
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

def difference_strict(old, new):
  return _merge_or_diff(old, new, False, True)

def difference(old, new):
  return _merge_or_diff(old, new, False, False)

def merge_strict(*others, **kwds):
  def merge(old, new):
    return _merge_or_diff(old, new, True, True)

  return reduce(merge, others + (kwds, ), None)

def merge(*others, **kwds):
  def merge(old, new):
    return _merge_or_diff(old, new, True, False)

  return reduce(merge, others + (kwds, ), None)
