from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Registry

_REGISTRY = Registry.Registry('command line')

def usage():
  return 'Commands are:\n  %s' % ', '.join(_REGISTRY.registry)

get = _REGISTRY.get
get_help = _REGISTRY.get_help
register = _REGISTRY.register
register_all = _REGISTRY.register_all
