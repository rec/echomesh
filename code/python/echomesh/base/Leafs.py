from __future__ import absolute_import, division, print_function, unicode_literals

def leafs(table):
  values = {}
  def recurse(item, path):
    if isinstance(item, dict):
      for key, value in six.iteritems(item):
        recurse(value, path + (key,))
    else:
      values[path] = item
  recurse(table, ())
  return values

def leafs_parent(table):
  values = []
  def recurse(item, parent, path):
    if isinstance(item, dict):
      for key, value in six.iteritems(item):
        recurse(value, item, path + [key])
    else:
      values.append((path, value, parent))
  recurse(table, None, [])
  return values
