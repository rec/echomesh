from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def register(class_path, *modules, ***kwds):
  module = sys.modules[class_path]
  registry = Registry(class_path, class_path=class_path, **kwds)

  for sub in module:
    registry.register(sub, sub.lower())

  setattr(module, 'REGISTRY', registry)
  for a in dir(registry):
    if not a.startswith('_'):
      setattr(module, a, getattr(registry, a))
