from __future__ import absolute_import, division, print_function, unicode_literals

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
  def __init__(self, *args, **kwds):
    super(Access, self).__init__(*args, **kwds)
    self._accessed = set()

  def not_accessed(self):
    return set(self.iterkeys()).difference(self._accessed)

  def __getitem__(self, key):
    res = super(Access, self).__getitem__(key)
    self._accessed.add(key)
    return res

  def get(self, key, default=None):
    res = super(Access, self).get(key, default)
    self._accessed.add(key)
    return res
  # TODO: why do I need both get and __getitem__ ?
  # probably should  use either collections.MutableMapping or UserDict but not
  # obvious how to do it.
