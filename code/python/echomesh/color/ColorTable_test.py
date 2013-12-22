from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import to_color
from echomesh.util.TestCase import TestCase

class TestColorTable(TestCase):
  def test_black(self):
    self.assertEqual(to_color('black'), [0.0, 0.0, 0.0])

  def test_white(self):
    self.assertEqual(to_color('white'), [1.0, 1.0, 1.0])

  def test_pink(self):
    self.assertEqual(to_color('pink'),
                     [1.0, 0.7529411911964417, 0.7960784435272217])

  def test_gray(self):
    self.assertEqual(to_color('gray'),
                     [0.501960813999176, 0.501960813999176, 0.501960813999176])

  def test_grey(self):
    self.assertEqual(to_color('grey'),
                     [0.501960813999176, 0.501960813999176, 0.501960813999176])

  def test_grey3(self):
    self.assertEqual(to_color('grey 3'),
                     [0.027450980618596077, 0.027450980618596077, 0.027450980618596077])

  def test_grey0(self):
    self.assertEqual(to_color('grey 0'), [0.0, 0.0, 0.0])

  def test_grey1000(self):
    self.assertEqual(to_color('grey 100'), [1.0, 1.0, 1.0])
