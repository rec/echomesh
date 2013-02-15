from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Registry

_REGISTRY = Registry.Registry('command line')

get = _REGISTRY.get
get_help = _REGISTRY.get_help
register = _REGISTRY.register
register_all = _REGISTRY.register_all
join_keys = _REGISTRY.join_keys
