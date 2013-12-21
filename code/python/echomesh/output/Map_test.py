from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.TestCase import TestCase

class MapTest(TestCase):
  def test_map(self):
    self.assertOutput(
      {'type': 'map', 'map': {0: [3, 4], 1: 2}},
      ['a', 'b', 'c', 'd', 'e'],
      ['a', 'b', 'b', 'a', 'a'])

  def test_filter(self):
    self.assertOutput(
      {'type': 'map', 'map': {0: [3, 4], 1: 2}, 'filter': True},
      ['a', 'b', 'c', 'd', 'e'],
      [None, None, 'b', 'a', 'a'])

