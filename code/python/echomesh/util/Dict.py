from __future__ import absolute_import, division, print_function, unicode_literals

import six

class Factory(dict):
  def __init__(self, factory, *args, **kwds):
    super(Factory, self).__init__(*args, **kwds)
    self.factory = factory

  def __missing__(self, key):
    value = self.factory(key)
    self[key] = value
    return value

  def __repr__(self):
    rep = super(Factory, self).__repr__()
    return 'Factory(%s, %s)' % (self.factory, rep)

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

def from_attributes(object, fields):
  return dict((f, getattr(object, f, None)) for f in fields)

