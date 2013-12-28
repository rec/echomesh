from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color
from echomesh.util.TestCase import TestCase

class TestColorTable(TestCase):
  def test_black(self):
    self.assertEqual(Color('black').parts, [0.0, 0.0, 0.0])

  def test_white(self):
    self.assertEqual(Color('white').parts, [1.0, 1.0, 1.0])

  def test_pink(self):
    self.assertEqual(Color('pink').parts,
                     [1.0, 0.7529411911964417, 0.7960784435272217])

  def test_gray(self):
    self.assertEqual(Color('gray').parts,
                     [0.501960813999176, 0.501960813999176, 0.501960813999176])

  def test_grey(self):
    self.assertEqual(Color('grey').parts,
                     [0.501960813999176, 0.501960813999176, 0.501960813999176])

  def test_grey3(self):
    self.assertEqual(Color('grey 3').parts,
                     [0.027450980618596077, 0.027450980618596077, 0.027450980618596077])

