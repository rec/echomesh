from __future__ import absolute_import, division, print_function, unicode_literals

class Registry(object):
  def __init__(self, name, case_insensitive=True, allow_prefixes=True):
    self.registry = {}
    self.name = name
    self.case_insensitive = case_insensitive
    self.allow_prefixes = allow_prefixes
    self.none = object()

  def register(self, item_name, item):
    if self.case_insensitive:
      item_name = item_name.lower()
    old_item = self.registry.get(item_name)
    if old_item is not item:
      if old_item:
        raise Exception('Conflicting registrations for %s' % item_name)
      self.registry[item_name] = item

  def get(self, name):
    result = self.registry.get(name, self.none)
    if result is not self.none:
      return result
    if self.allow_prefixes:
      match = [v for (k, v) in self.registry.iteritems() if k.startswith(name)]
      if match:
        if len(match) > 1:
          raise Exception(
            'Name "%s" matches multiple entries in registry %s: %s.' %
            (name, self.name, ', '.join(sorted(match))))
        return match[0]
    raise Exception("Didn't find \"%s\" in registry %s." % (name, self.name))

  def dump(self, print=print):
    for k, v in self.registry.iteritems():
      print(k, v)
