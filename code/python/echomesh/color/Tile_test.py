from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import tile_color_list, ColorMatrix
from echomesh.util.TestCase import TestCase

class TestTile(TestCase):
    def test_empty(self):
        before = ColorMatrix(columns=1)
        self.assertEqual(tile_color_list(before, 1, 1), before)
        self.assertEqual(tile_color_list(before, 1, 1), ColorMatrix(columns=1))

    def test_trivial(self):
        before = ColorMatrix(['red', 'yellow', 'green', 'blue'], columns=2)
        self.assertEqual(tile_color_list(before, 1, 1), before)

    def test_double(self):
        before = ColorMatrix(
          ['red', 'yellow', 'green', 'blue', 'pink', 'white'], columns=3)
        after = tile_color_list(before, 2, 2)
        result = ColorMatrix(
          ['red', 'yellow', 'green', 'red', 'yellow', 'green',
           'blue', 'pink', 'white', 'blue', 'pink', 'white',
           'red', 'yellow', 'green', 'red', 'yellow', 'green',
           'blue', 'pink', 'white', 'blue', 'pink', 'white'], columns=6)
        self.assertEqual(after, result)

    def test_partial(self):
        before = ColorMatrix(
          ['red', 'yellow', 'green', 'blue'], columns=3)
        after = tile_color_list(before, 2, 2)
        result = ColorMatrix(
          ['red', 'yellow', 'green', 'red', 'yellow', 'green',
           'blue', 'black', 'black', 'blue', 'black', 'black',
           'red', 'yellow', 'green', 'red', 'yellow', 'green',
           'blue', 'black', 'black', 'blue', 'black', 'black'], columns=6)
        self.assertEqual(after, result)
