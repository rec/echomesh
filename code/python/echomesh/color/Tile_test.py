from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import tile_color_list, ColorList
from echomesh.util.TestCase import TestCase

class TestTile(TestCase):
  def test_empty(self):
    before = ColorList()
    self.assertEqual(tile_color_list(before, 1, 1), before)
    self.assertEqual(tile_color_list(before, 1, 1, 1), ColorList(columns=1))

  def test_trivial(self):
    before = ColorList(['red', 'yellow', 'green', 'blue'], columns=2)
    self.assertEqual(tile_color_list(before, 1, 1), before)

