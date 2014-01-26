from __future__ import absolute_import, division, print_function, unicode_literals

import six
import sys

from echomesh.util.registry.Registry import Registry

def register(class_path, *modules, **kwds):
  module = sys.modules[class_path]
  registry = Registry(class_path, class_path=class_path, **kwds)

  for sub in modules:
    if isinstance(sub, six.string_types):
      registry.register(sub, sub.lower())
    else:
      registry.register(sub[1], sub[0].lower())

  return registry
