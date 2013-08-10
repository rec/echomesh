from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.util.dict import Setter
from echomesh.util.TestCase import TestCase

class SetterTest(TestCase):
  def setUp(self):
    self.config = {'hello': 'world', 'deep': {'tree': {'nesting': 'egg'}}}

  def test_simple(self):
    self.assertEqual(Setter.setter(self.config, 'hello'),
                     (self.config, 'hello'))

  def test_two(self):
    self.assertEqual(Setter.setter(self.config, 'deep', 'tree', 'nesting'),
                     ({'nesting': 'egg'}, 'nesting'))

