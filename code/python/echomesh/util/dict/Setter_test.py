from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.util.dict import Setter
from echomesh.util.TestCase import TestCase

class SetterTest(TestCase):
  def setUp(self):
    self.config = {
      'hello': 'world',
      'deep': {
        'tree': {
          'nesting': 'egg',
          'fish': 'food'
        }
      }
    }

  def add_suffix(self, x):
    return x + '.end'

  def test_simple_setter(self):
    self.assertEqual(Setter.setter(self.config, 'hello'),
                     (self.config, 'hello'))

  def test_two_setter(self):
    self.assertEqual(Setter.setter(self.config, 'deep', 'tree', 'nesting'),
                     ({'fish': 'food', 'nesting': 'egg'}, 'nesting'))

  def test_apply_list(self):
    Setter.apply_list(self.config, self.add_suffix,
                      ['hello'], ['deep', 'tree', 'fish'])
    self.assertEqual(self.config,
                     {'hello': 'world.end',
                      'deep': {'tree': {'fish': 'food.end', 'nesting': 'egg'}}})

  def test_apply_dict(self):
    Setter.apply_dict(self.config, self.add_suffix,
                      {'hello': True,
                       'deep': {'tree': {'fish': True}}})
    self.assertEqual(self.config,
                     {'hello': 'world.end',
                      'deep': {'tree': {'fish': 'food.end', 'nesting': 'egg'}}})
