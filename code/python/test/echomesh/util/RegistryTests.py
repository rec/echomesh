"""
>>> registry = Registry.Registry('test')
>>> registry.register('foo', 'item1')
>>> registry.register('fot', 'item2')
>>> registry.register('bar', 'item3')
>>> registry.get('foo')
u'item1'

>>> registry.get('b')
u'item3'

>>> registry_exception(registry, 'fo')
"fo" matches multiple tests: foo and fot.

>>> registry.allow_prefixes = False
>>> registry_exception(registry, 'fo')
"fo" is not a valid test.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Registry

def registry_exception(registry, name):
  try:
    print(registry.get(name))
  except Exception as e:
    print(e)
