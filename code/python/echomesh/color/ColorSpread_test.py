from __future__ import absolute_import, division, print_function, unicode_literals

import numpy

from cechomesh import Transform, ColorList

from echomesh.color import ColorSpread
from echomesh.util.TestCase import TestCase

class TestColorSpread(TestCase):
  EPSILON = 0.00000001

  def assertSpreadResult(self, *args, **kwds):
    spread = ColorSpread.color_spread(*args, **kwds)
    self.assertEquals(ColorList(self.result), spread)

  def assertColorSpreadResult(self, *args, **kwds):
    spread = ColorSpread.color_spread(*args, **kwds)
    self.assertEquals(ColorList(self.result), spread)

  def test_simple(self):
    self.result = numpy.array([[], [], []], dtype=numpy.float64).T
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 0)

  def test_one_spread(self):
    self.result = [
      [ 1. ,  0. ,  0. ],
      [ 1. ,  0.8,  0. ],
      [ 0.4,  1. ,  0. ],
      [ 0. ,  1. ,  0.4],
      [ 0. ,  0.8,  1. ],
      [ 0. ,  0. ,  1. ]]
    self.assertSpreadResult([1, 0, 0], [0, 0, 1], 6)

  def test_no_hsb(self):
    self.result = [
      [ 1. ,  0. ,  0. ],
      [ 0.8,  0. ,  0.2],
      [ 0.6,  0. ,  0.4],
      [ 0.4,  0. ,  0.6],
      [ 0.2,  0. ,  0.8],
      [ 0. ,  0. ,  1. ]]
    self.assertSpreadResult([1, 0, 0], [0, 0, 1], 6, use_hsb=False)

  def test_two_colors(self):
    self.result = [
      [ 1. ,  1. ,  0. ],
      [ 0.6,  1. ,  0. ],
      [ 0.2,  1. ,  0. ],
      [ 0. ,  1. ,  0.2],
      [ 0. ,  1. ,  0.6],
      [ 0. ,  1. ,  1. ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 6)

  def test_two_colors_identity(self):
    self.result = [
      [ 1. ,  1. ,  0. ],
      [ 0.6,  1. ,  0. ],
      [ 0.2,  1. ,  0. ],
      [ 0. ,  1. ,  0.2],
      [ 0. ,  1. ,  0.6],
      [ 0. ,  1. ,  1. ]]
    self.assertSpreadResult(
      [1, 1, 0], [0, 1, 1], 6, Transform('identity'))

  def test_two_colors_square(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.38754845,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.04939015],
      [ 0.        ,  1.        ,  0.40831892],
      [ 0.        ,  1.        ,  0.7202941 ],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult(
      [1, 1, 0], [0, 1, 1], 6, transform=Transform('square'))

  def test_two_colors_sqrt(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.68574374,  1.        ,  0.        ],
      [ 0.32861561,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.07138439],
      [ 0.        ,  1.        ,  0.51425626],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 6,
                            transform=Transform('square+inverse'))

  def test_inverse_square(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.68574374,  1.        ,  0.        ],
      [ 0.32861561,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.07138439],
      [ 0.        ,  1.        ,  0.51425626],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1],
                            6, transform=Transform('square+inverse'))
  def test_exp(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.54311082,  1.        ,  0.        ],
      [ 0.11856458,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.27791662],
      [ 0.        ,  1.        ,  0.64981435],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 6, transform=Transform('exp'))

  def test_inverse_exp(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.65665603,  1.        ,  0.        ],
      [ 0.28706791,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.11077039],
      [ 0.        ,  1.        ,  0.53901822],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult(
      [1, 1, 0], [0, 1, 1], 6, transform=Transform('exp+inverse'))

  def test_sine(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.46179262,  1.        ,  0.        ],
      [ 0.04354821,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.3244033 ],
      [ 0.        ,  1.        ,  0.66752594],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 6, transform=Transform('sine'))

  def test_inverse_sine(self):
    self.result = [
      [ 1.        ,  1.        ,  0.        ],
      [ 0.65355085,  1.        ,  0.        ],
      [ 0.27194337,  1.        ,  0.        ],
      [ 0.        ,  1.        ,  0.13670856],
      [ 0.        ,  1.        ,  0.56371608],
      [ 0.        ,  1.        ,  1.        ]]
    self.assertSpreadResult([1, 1, 0], [0, 1, 1], 6,
                            transform=Transform('sine+inverse'))

  def test_name(self):
    self.result = [
      [ 1. ,  0. ,  0. ],
      [ 1. ,  0.2,  0.2],
      [ 1. ,  0.4,  0.4],
      [ 1. ,  0.6,  0.6],
      [ 1. ,  0.8,  0.8],
      [ 1. ,  1. ,  1. ]]
    self.assertColorSpreadResult('red', 'white', 6)
