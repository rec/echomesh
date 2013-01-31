from __future__ import absolute_import, division, print_function, unicode_literals

class Registry(object):
  def __init__(self, case_insensitive=True):
    self.registry = {}
    self.case_insensitive = case_insensitive

  def register(self, item, name=None):
    name = name or item.__name__
    if self.case_insensitive:
      name = name.lower()
    old_item = self.registry.get(name)
    if old_item is not item:
      if old_item:
        raise Exception('Conflicting registrations for %s' % name)
      self.registry[name] = item

  def get(self, name, default=None):
    return self.registry.get(name, default)

  def dump(self, print=print):
    for k, v in self.registry.iteritems():
      print(k, v)
