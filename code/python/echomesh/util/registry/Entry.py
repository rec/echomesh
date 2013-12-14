from __future__ import absolute_import, division, print_function, unicode_literals

import importlib
import six

from echomesh.base import Join

class Entry(object):
  def __init__(self, name, function, help_text, see_also, registry):
    self.name = name
    self.function = function
    self.help_text = help_text
    self.see_also = see_also
    self.registry = registry

  def __str__(self):
    return (
      'RegistryEntry(name=%s, function=%s, help_text=%s, see_also=%s)' %
      (self.name, self.function, self.help_text, self.see_also))

  def resolve_function(self):
    if isinstance(self.function, six.string_types):
      class_path = '%s.%s' % (self.registry.class_path, self.function)
      mod = importlib.import_module(class_path)
      name = self.function.lower()
      f = self.function
      self.function = (getattr(mod, 'FUNCTION', None) or
                       getattr(mod, name, None) or
                       getattr(mod, self.function, None))
      assert self.function

      self.help_text = getattr(mod, 'HELP', None)
      self.see_also = getattr(mod, 'SEE_ALSO', None)

  def help(self):
    help = self.help_text

    if self.name == 'commands':  # HACK.
      help += self.registry.join_keys()

    help = help or self.name
    if self.see_also:
      also = Join.join_words('"help %s"' % h for h in self.see_also)
      help = '%s\n\nSee also: %s\n' % (help, also)

    return help
