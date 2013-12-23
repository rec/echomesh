from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color

from echomesh.util.TestCase import TestCase

class ColorTest(TestCase):
  def test_empty_color(self):
    self.assertEqual(str(Color()), 'Color(black, alpha=0.000)')

  def test_black(self):
    self.assertEqual(str(Color('black')), 'Color(black)')

  def test_red(self):
    self.assertEqual(str(Color('red')), 'Color(red)')

  def test_red2(self):
    self.assertEqual(str(Color(1.0, 0, 0)), 'Color(red)')

  def test_unnnamed(self):
    self.assertEqual(str(Color(0.7, 0.1, 0.2)),
                     'Color(red=0.698, green=0.098, blue=0.200)')

  def test_unknown(self):
    self.assertRaises(ValueError, Color, 'glug')
