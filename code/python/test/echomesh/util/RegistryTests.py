"""
>>> registry = Registry.Registry('test')
>>> registry.register('item1', 'foo')
>>> registry.register('item2', 'fot')
>>> registry.register('item3', 'bar')
>>> registry.get('foo')
u'item1'

>>> registry.get('b')
u'item3'

>>> registry_exception(registry, 'fo')
"fo" matches more than one: foo and fot.

>>> registry.allow_prefixes = False
>>> registry_exception(registry, 'fo')
"fo" is not valid.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.registry import Registry

def registry_exception(registry, name):
  try:
    print('WRONG', registry.get(name))
  except Exception as e:
    print(str(e))
