from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.util import Importer
from echomesh.util import Registry

class LazyRegistry(Registry.Registry):
  def __init__(self, name, classpath='',
               case_insensitive=True, allow_prefixes=True):
    super(LazyRegistry, self).__init__(name, case_insensitive, allow_prefixes)
    optional_dot = '.' if classpath and not classpath.endswith('.') else ''
    self.classpath = classpath + optional_dot

  def get(self, name):
    name, (function, _, _) = self._get(name)
    if not six.callable(function):
      function = Importer.imp(self.classpath + function, defer_failure=False)
      self.registry[name][0] = function
    return function

