from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Registry

_REGISTRY = Registry.Registry('Commander')

def _fix_exception_message(m, name):
  loc = m.find(')')
  if loc >= 0:
    m = m[loc + 1:]
  m = (m.replace('1', '0').
       replace('2', '1').
       replace('3', '2').
       replace('4', '3'))
  return name + m

def usage():
  return 'Commands are:\n  %s' % ', '.join(_REGISTRY.registry)

get = _REGISTRY.get
register = _REGISTRY.register
register_all = _REGISTRY.register_all
