from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.util.Registry import Registry
from echomesh.util import Importer

class ClassRegistry(Registry):
  def __init__(self, name, classpath='',
               case_insensitive=True, allow_prefixes=True):
    super(ClassRegistry, self).__init__(name, case_insensitive, allow_prefixes)
    optional_dot = '.' if classpath and not classpath.endswith('.') else ''
    self.classpath = classpath + optional_dot

  def get(self, name):
    name, (function, _, _) = self._get(name)
    if not six.callable(function):
      parts = function.split('.')
      if len(parts) < 2 or parts[-2].islower():
        classname = parts[-1]
      else:
        classname = parts.pop()
      mod = Importer.imp(self.classpath + '.'.join(parts), defer_failure=False)
      function = getattr(mod, classname)
      self.registry[name][0] = function
    return function

