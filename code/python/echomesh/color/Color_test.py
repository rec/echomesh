from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color, interpolate_hue

from echomesh.util.TestCase import TestCase

class ColorTest(TestCase):
  def assertEqualList(self, l1, l2):
    assert len(l1) == len(l2)
    for i, j in zip(l1, l2):
      self.assertNear(i, j)

  def test_empty_color(self):
    self.assertEqual(str(Color()), 'black')

  def test_black(self):
    self.assertEqual(str(Color('black')), 'black')

  def test_red(self):
    self.assertEqual(str(Color('red')), 'red')

  def test_red2(self):
    self.assertEqual(str(Color([1.0, 0, 0])), 'red')

  def test_yellow(self):
    self.assertEqual(str(Color('white', model='hsb')), 'white')

  def test_equal(self):
    self.assertEqual(Color('red'), Color('red'))

  def test_unnamed(self):
    self.assertEqual(str(Color([0.7, 0.1, 0.2])),
                     '[red=0.700, green=0.100, blue=0.200]')

  def test_rgb(self):
    self.assertEqual(Color('red').rgb, [1.0, 0.0, 0.0])
    self.assertEqual(Color('red').hsb, [0.0, 1.0, 1.0])
    self.assertEqual(Color('green').rgb, [0.0, 1.0, 0.0])
    self.assertNear(Color('green').hsb, [1.0 / 3.0, 1.0, 1.0])
    self.assertEqual(Color('blue').rgb, [0.0, 0.0, 1.0])
    self.assertNear(Color('blue').hsb, [2.0 / 3.0, 1.0, 1.0])

  def test_hsb(self):
    self.assertEqual(Color('red', model='hsb').rgb, [1.0, 0.0, 0.0])
    self.assertEqual(Color('red', model='hsb').hsb, [0.0, 1.0, 1.0])
    self.assertEqual(Color('green', model='hsb').rgb, [0.0, 1.0, 0.0])
    self.assertNear(Color('green', model='hsb').hsb, [1.0 / 3.0, 1.0, 1.0])
    self.assertEqual(Color('blue', model='hsb').rgb, [0.0, 0.0, 1.0])
    self.assertNear(Color('blue', model='hsb').hsb, [2.0 / 3.0, 1.0, 1.0])

  def test_unknown(self):
    self.assertRaises(ValueError, Color, 'glug')

  def test_sort2(self):
    self.assertTrue(Color('blue') < Color('green'))

  def test_sort6(self):
    self.assertTrue(Color('blue') < Color('red'))

  def test_sort9(self):
    self.assertTrue(Color('green') < Color('red'))

  def test_interpolate_hue1(self):
    self.assertNear(interpolate_hue(0, 0, 0), 0)
    self.assertNear(interpolate_hue(0, 0, 0.5), 0)
    self.assertNear(interpolate_hue(0, 0, 1.0), 0)

  def test_interpolate_hue2(self):
    self.assertNear(interpolate_hue(0, 0.5, 0), 0)
    self.assertNear(interpolate_hue(0, 0.5, 0.5), 0.25)
    self.assertNear(interpolate_hue(0, 0.5, 1), 0.5)

  def test_interpolate_hue3(self):
    self.assertNear(interpolate_hue(0, 0.6, 0), 0)
    self.assertNear(interpolate_hue(0, 0.6, 0.5), 0.80)
    self.assertNear(interpolate_hue(0, 0.6, 1), 0.6)

  def test_interpolate_hue4(self):
    self.assertNear(interpolate_hue(0.4, 0, 0), 0.4)
    self.assertNear(interpolate_hue(0.4, 0, 0.4), 0.24)
    self.assertNear(interpolate_hue(0.4, 0, 0.6), 0.16)

  def test_interpolate_hue5(self):
    self.assertNear(interpolate_hue(0.8, 0.2, 0.0), 0.8)
    self.assertNear(interpolate_hue(0.8, 0.2, 0.4), 0.96)
    self.assertNear(interpolate_hue(0.8, 0.2, 0.6), 0.04)
