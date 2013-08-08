from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

import six
import sys

from echomesh.base import GetPrefix
from echomesh.base import Join
from echomesh.util import Importer

class Entry(object):
  def __init__(self, name, function, help_text, see_also):
    self.name = name
    self.function = function
    self.help_text = help_text
    self.see_also = see_also

  def __str__(self):
    return (
      'RegistryEntry(name=%s, function=%s, help_text=%s, see_also=%s)' %
      (self.name, self.function, self.help_text, self.see_also))

  def load(self):
    pass

class Registry(object):
  def __init__(self, name, case_insensitive=True, allow_prefixes=True,
               entry_class=Entry):
    self.registry = {}
    self.name = name
    self.case_insensitive = case_insensitive
    self.allow_prefixes = allow_prefixes
    self.entry_class = Entry

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
      self.registry[function_name] = self.entry_class(
        function_name, function, help_text, see_also)

  def register_all(self, **kwds):
    for item_name, item in six.iteritems(kwds):
      help_text, see_also = None, None
      if isinstance(item, (list, tuple)):
        if len(item) > 1:
          help_text = item[1]
          if len(item) > 2:
            see_also = item[2]
        item = item[0]
      self.register(item, item_name, help_text, see_also)

  def _get(self, name):
    return GetPrefix.get_prefix(self.registry, name,
                                allow_prefixes=self.allow_prefixes)[1]

  def full_name(self, name):
    return self._get(name).name

  def get(self, name):
    return self._get(name).function

  def get_key_and_value(self, name):
    entry = self._get(name)
    return entry.name, entry.function

  def get_key_and_value_or_none(self, name):
    entry = self._get(name)
    if not entry:
      return None, None

    return entry.name, entry.function

  def get_help(self, name):
    entry = self._get(name)
    entry.load()
    help_text = entry.help_text

    if entry.name == 'commands':  # HACK.
      help_text += self.join_keys()

    help_text = help_text or entry.name

    if entry.see_also:
      also = Join.join_words('"help %s"' % h for h in entry.see_also)
      return '%s\n\nSee also: %s\n' % (help_text, also)
    else:
      return help_text

  def keys(self):
    return self.registry.keys()

  def join_keys(self, command_only=True):
    # TODO: not loading for this, will this work?
    w = (k for (k, entry) in six.iteritems(self.registry)
         if (not command_only) or entry.function)
    return Join.join_words(w)

  def dump(self, printer=print, load=True):
    for k, v in six.iteritems(self.registry):
      load and v.load()
      printer(k, v)

def module_registry(module_name, name=None, **kwds):
  module = sys.modules[module_name]
  registry = Registry(name or module_name, **kwds)

  for sub in module.__all__:
    sub_lower = sub.lower()
    sub_module = Importer.import_module('%s.%s' % (module_name, sub))
    function = (getattr(sub_module, 'FUNCTION', None) or
                getattr(sub_module, sub_lower) )
    registry.register(
      function=function,
      function_name=getattr(sub_module, 'NAME', sub_lower),
      help_text=getattr(sub_module, 'HELP', None),
      see_also=getattr(sub_module, 'SEE_ALSO', None))

  setattr(module, 'REGISTRY', registry)
  for a in dir(registry):
    if not a.startswith('_'):
      setattr(module, a, getattr(registry, a))
