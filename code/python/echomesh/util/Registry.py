from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import GetPrefix
from echomesh.util import String

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
      self.register(item, item_name, help_text, see_also)

  def module(self, module):
    function_name = module.__name__
    function = getattr(module, function_name.lower(), None)
    help_text = getattr(module, 'HELP', None)
    see_also = getattr(module, 'SEE_ALSO', None)
    self.register(function, function_name, help_text, see_also)

  def register(self, function, function_name=None,
               help_text=None, see_also=None):
    function_name = function_name or function.__name__
    if self.case_insensitive:
      function_name = function_name.lower()

    none = object()
    old_function = self.registry.get(function_name, (none, none))[0]
    if old_function is not function:
      if old_function is not none:
        raise Exception('Conflicting registrations for %s' % function_name)
      self.registry[function_name] = function, help_text, see_also


  def _get(self, name):
    return GetPrefix.get_prefix_and_match(self.registry, name, self.name,
                                          allow_prefixes=self.allow_prefixes)

  def get(self, name):
    return self._get(name)[1][0]

  def get_help(self, name):
    full_name, (_, help_text, see_also) = self._get(name)

    if full_name == 'commands':  # HACK.
      help_text += self.join_keys()

    if see_also:
      also = String.join_words('"help %s"' % h for h in see_also)
      return '%s\n\nSee also: %s\n' % (help_text, also)
    else:
      return help_text

  def keys(self):
    return self.registry.keys()

  def join_keys(self, command_only=True):
    w = (k for (k, v) in self.registry.iteritems() if (not command_only) or v[0])
    return String.join_words(w)

  def dump(self, print=print):
    for k, v in self.registry.iteritems():
      print(k, v)
