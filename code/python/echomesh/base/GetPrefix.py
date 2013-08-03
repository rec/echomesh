from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Join

class PrefixException(Exception):
  pass

_NONE = object()

def get_prefix(table, name, allow_prefixes=True):
  """
  Looks up an entry in a table where unique prefixes are allowed.
  """
  result = table.get(name, _NONE)
  if result is not _NONE:
    return name, result

  if allow_prefixes:
    results = [(k, v) for (k, v) in table.iteritems() if k.startswith(name)]
    if len(results) == 1:
      return results[0]
    elif len(results) > 1:
      words = sorted(x[0] for x in results)
      cmds = Join.join_words(words)
      raise PrefixException('"%s" matches more than one: %s.' % (name, cmds))
  raise PrefixException('"%s" is not valid.' % (name))

def get(table, name, allow_prefixes=True):
  try:
    return get_prefix(table, name, allow_prefixes)
  except PrefixException:
    return None

def accessor(table, names,
             allow_prefixes=True, unmapped_names=None, create=False):
  path = []
  unmapped = False
  for i, name in enumerate(names):
    is_last = i >= len(names) - 1
    if create:
      value = table.setdefault(name, None if is_last else {})
    elif unmapped:
      value = (table or {}).get(name, None)
    else:
      name, value = get_prefix(table, name, allow_prefixes)
    path.append(name)
    if is_last:
      return path, table, value
    table = value
    if (not i) and unmapped_names and name in unmapped_names:
      unmapped = True

def get_accessor(table, names, **kwds):
  return accessor(table, names, **kwds)[2]

def set_accessor(table, names, value, create=True, allow_prefixes=False):
  for i, name in enumerate(names):
    if i < len(names) - 1:
      if create:
        table = table.setdefault(name, {})
      else:
        table = get_prefix(table, name, allow_prefixes)
    else:
      table[name] = value

def set_assignment(address, value, master_table, slave_table,
                    allow_prefixes=True, unmapped_names=None):
  names = accessor(master_table, address.split('.'),
                   allow_prefixes, unmapped_names)[0]
  set_accessor(slave_table, names, value)

def leafs(table):
  values = {}
  def recurse(item, path):
    if isinstance(item, dict):
      for key, value in item.iteritems():
        recurse(value, path + (key,))
    else:
      values[path] = value
  recurse(table, ())
  return values

def leafs_parent(table):
  values = []
  def recurse(item, parent, path):
    if isinstance(item, dict):
      for key, value in item.iteritems():
        recurse(value, item, path + [key])
    else:
      values.append((path, value, parent))
  recurse(table, None, [])
  return values
