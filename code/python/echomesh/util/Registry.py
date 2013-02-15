from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Join

class Registry(object):
  def __init__(self, name, case_insensitive=True, allow_prefixes=True):
    self.registry = {}
    self.name = name
    self.case_insensitive = case_insensitive
    self.allow_prefixes = allow_prefixes

  def register_all(self, **kwds):
    for item_name, item in kwds.iteritems():
      help_text = None
      if isinstance(item, (list, tuple)):
        item, help_text = item
      self.register(item_name, item, help_text)

  def register(self, item_name, item, help_text=None):
    if self.case_insensitive:
      item_name = item_name.lower()
    old_item, old_help = self.registry.get(item_name, (None, None))
    if old_item is not item:
      if old_item:
        raise Exception('Conflicting registrations for %s' % item_name)
      self.registry[item_name] = item, help_text

  def _get(self, name):
    result = self.registry.get(name)
    if result:
      return result

    if self.allow_prefixes:
      match = [v for (k, v) in self.registry.iteritems() if k.startswith(name)]
      if match:
        if len(match) > 1:
          raise Exception(
            'Name "%s" matches multiple commands for %s.' % (name, self.name))
        return match[0]

    raise Exception('"%s" is not a valid command for %s.' % (name, self.name))

  def get(self, name):
    return self._get(name)[0]

  def get_help(self, name):
    return self._get(name)[1]

  def keys(self):
    return self.registry.keys()

  def join_keys(self):
    return Join.join_words(*sorted(self.registry.iterkeys()))

  def dump(self, print=print):
    for k, v in self.registry.iteritems():
      print(k, v)
