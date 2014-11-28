from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color
from echomesh.util.TestCase import TestCase

class TestColorTable(TestCase):
    def test_black(self):
        self.assertEqual(Color('black').rgb, [0.0, 0.0, 0.0])

    def test_white(self):
        self.assertEqual(Color('white').rgb, [1.0, 1.0, 1.0])

    def test_pink(self):
        self.assertEqual(Color('pink').rgb,
                         [1.0, 0.7529411911964417, 0.7960784435272217])

    def test_gray(self):
        self.assertEqual(
            Color('gray').rgb,
            [0.501960813999176, 0.501960813999176, 0.501960813999176])

    def test_grey(self):
        self.assertEqual(
            Color('grey').rgb,
            [0.501960813999176, 0.501960813999176, 0.501960813999176])

    def test_grey3(self):
        self.assertEqual(
          Color('grey 3').rgb,
          [0.029999999329447746, 0.029999999329447746, 0.029999999329447746])
