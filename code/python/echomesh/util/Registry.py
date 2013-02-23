from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import GetPrefix
from echomesh.util import Join

class Registry(object):
  def __init__(self, name, case_insensitive=True, allow_prefixes=True):
    self.registry = {}
    self.name = name
    self.case_insensitive = case_insensitive
    self.allow_prefixes = allow_prefixes

  def register_all(self, **kwds):
    for item_name, item in kwds.iteritems():
      help_text, see_also = None, None
      if isinstance(item, (list, tuple)):
        if len(item) > 1:
          help_text = item[1]
          if len(item) > 2:
            see_also = item[2]
        item = item[0]
      self.register(item_name, item, help_text, see_also)

  def register(self, item_name, item, help_text=None, see_also=None):
    if self.case_insensitive:
      item_name = item_name.lower()

    none = object()
    old_item, old_help = self.registry.get(item_name, (none, none))
    if old_item is not item:
      if old_item is not none:
        raise Exception('Conflicting registrations for %s' % item_name)
      self.registry[item_name] = item, help_text, see_also

  def _get(self, name):
    return GetPrefix.get_prefix_and_match(self.registry, name,
                                          allow_prefixes=self.allow_prefixes)

  def get(self, name):
    return self._get(name)[1][0]

  def get_help(self, name):
    full_name, (item, help_text, see_also) = self._get(name)

    if full_name == 'commands':  # HACK.
      help_text += self.join_keys()

    if see_also:
      also = Join.join_words(*('"help %s"' % h for h in see_also))
      return '%s\n\nSee also: %s\n' % (help_text, also)
    else:
      return help_text

  def keys(self):
    return self.registry.keys()

  def join_keys(self, command_only=True):
    w = (k for (k, v) in self.registry.iteritems() if (not command_only) or v[0])
    return Join.join_words(*sorted(w))

  def dump(self, print=print):
    for k, v in self.registry.iteritems():
      print(k, v)
