from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.util import Importer
from echomesh.util import Registry

class Entry(Registry.Entry):
  def __init__(self, function, registry):
    super(Registry.Entry, self).__init__(function, None, None)
    self.registry = registry

  def load(self):
    if self.function and not six.callable(self.function):
      module_name = self.function
      module = Importer.imp(self.registry.classpath + module_name,
                            defer_failure=False)
      self.function = (getattr(module, 'FUNCTION', None) or
                       getattr(module, module_name.lower(), None) or
                       getattr(module, module_name, None))
      self.help_text = getattr(module, 'HELP', None)
      self.see_also = getattr(module, 'SEE_ALSO', None)


class LazyRegistry(Registry.Registry):
  def __init__(self, name, classpath='',
               case_insensitive=True, allow_prefixes=True):
    super(LazyRegistry, self).__init__(name, case_insensitive, allow_prefixes,
                                       entry_class=Registry.Entry)
    optional_dot = '.' if classpath and not classpath.endswith('.') else ''
    self.classpath = classpath + optional_dot

  def entry(self, name):
    entry = super(LazyRegistry, self).entry(name)
    if not six.callable(entry.function):
      entry.function = Importer.imp(self.classpath + entry.function,
                                    defer_failure=False)
    return entry
