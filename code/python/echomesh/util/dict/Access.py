from __future__ import absolute_import, division, print_function, unicode_literals

import six

class Access(dict):
  def __init__(self, args=None, **kwds):
    if args is None:
      super(Access, self).__init__(**kwds)
    else:
      super(Access, self).__init__(args, **kwds)
    self._accessed = set()

  def not_accessed(self):
    return set(six.iterkeys(self)).difference(self._accessed)

  def clear_accessed(self):
    self._accessed = set(six.iterkeys(self))

  def pop(self, key, *args):
    self._accessed.add(key)
    return super(Access, self).pop(key, *args)

  def __getitem__(self, key):
    res = super(Access, self).__getitem__(key)
    self._accessed.add(key)
    return res

  def __delitem__(self, key):
    res = super(Access, self).__delitem__(key)
    self._accessed.add(key)
    return res

  def get(self, key, default=None):
    res = super(Access, self).get(key, default)
    self._accessed.add(key)
    return res
  # TODO: why do I need both get and __getitem__ ?
  # probably should  use either collections.MutableMapping or UserDict but not
  # obvious how to do it.
