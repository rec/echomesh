from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.config.ConfigValues import ConfigValues
from echomesh.util.TestCase import TestCase

class ConfigValuesTest(TestCase):
  def add_client(self, values):
    def get(*names):
      if names == ('c',):
        return 42
      if names == ('d', 'e'):
        return 99
      raise Exception('oops')

    values.config_update(get)

  def setUp(self):
    self.values = ConfigValues(values={'a': 23, 'b': 'hello'},
                               configs={'c': 'c', 'd': 'd.e'},
                               add_client=self.add_client)
    self.values.add_client()

  def test_simple(self):
    self.assertEqual(self.values.a, 23)
    self.assertEqual(self.values.b, 'hello')
    self.assertEqual(self.values.c, 42)
    self.assertEqual(self.values.d, 99)
