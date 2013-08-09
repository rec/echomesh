from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

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
