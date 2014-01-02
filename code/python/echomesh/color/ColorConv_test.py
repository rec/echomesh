from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorConv
from echomesh.util.TestCase import TestCase

class TestColorConv(TestCase):
  def assertToHsb(self, items, expected):
    self.assertArrayEquals(ColorConv.rgb_to_hsb(items), expected)

  def assertToRgb(self, items, expected):
    self.assertArrayEquals(ColorConv.hsb_to_rgb(items), expected)

  def test_black(self):
    self.assertToHsb([0, 0, 0], [[ 0.,  0.,  0.]])


  def test_white(self):
    self.assertToHsb([1, 1, 1], [[ 0.,  0.,  1.]])


  def test_two(self):
    self.assertToHsb([[1.0, 0, 0], [0, 0, 1.0]],
                     [[ 0.        ,  1.        ,  1.        ],
                      [ 0.66666667,  1.        ,  1.        ]])

  def test_grey(self):
    self.assertToHsb([(0.5, 0.5, 0.5)], [[ 0. ,  0. ,  0.5]])

  def test_two_grey(self):
    self.assertToRgb([(0.1, 0.1, 0.1), (0.5, 0.5, 1)],
                     [[ 0.1  ,  0.096,  0.09 ], [ 0.5  ,  1.   ,  1.   ]])

