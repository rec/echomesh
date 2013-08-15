from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.registry import Registry
from echomesh.util.TestCase import TestCase

def _item1(): pass
def _item2(): pass
def _item3(): pass

class RegistryTest(TestCase):
  def setUp(self):
    self.registry = Registry.Registry('test')
    self.registry.register(_item1, 'foo')
    self.registry.register(_item2, 'fot')
    self.registry.register(_item3, 'bar')

  def test_full(self):
    self.assertEqual(self.registry.get('foo'), _item1)

  def test_abbrev(self):
    self.assertEqual(self.registry.get('b'), _item3)

  def test_multiple(self):
    try:
      self.registry.get('fo')
    except Exception as e:
      self.assertEqual(
        str(e), '"fo" matches more than one: foo and fot in registry "test"')

  def test_no_prefixes(self):
    self.registry.allow_prefixes = False
    try:
      self.registry.get('fo')
    except Exception as e:
      self.assertEqual(str(e), '"fo" is not valid in registry "test"')
