from __future__ import absolute_import, division, print_function, unicode_literals

class FactoryDict(dict):
  def __init__(self, factory, *args, **kwds):
    super(FactoryDict, self).__init__(*args, **kwds)
    self.factory = factory

  def __missing__(self, key):
    value = self.factory(key)
    self[key] = value
    return value

  def __repr__(self):
    drep = super(FactoryDict, self).__repr__()
    return 'FactoryDict(%s, %s)' % (self.factory, drep)
