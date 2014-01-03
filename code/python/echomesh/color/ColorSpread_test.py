from __future__ import absolute_import, division, print_function, unicode_literals

import numpy

from cechomesh import ColorList

from echomesh.color import ColorSpread
from echomesh.util.TestCase import TestCase

class TestColorSpread(TestCase):
  def assertSpread(self, *args, **kwds):
    spread = ColorSpread.color_spread(*args, **kwds)
    self.assertEquals(self.result, str(spread))

  def test_tiny_spread(self):
    self.result = '[red, [red=0.500, green=0.000, blue=0.500], blue]'
    self.assertSpread('red', 'blue', 3, use_hsb=False)

  def test_tiny_spread_hsb(self):
    self.result = '[red, magenta, blue]'
    self.assertSpread('red', 'blue', 3, use_hsb=True)

  def test_one_spread(self):
    self.result = ('[red, [red=1.000, green=0.000, blue=0.400], [red=1.000, green=0.000, blue=0.800], [red=0.800, green=0.000, blue=1.000], [red=0.400, green=0.000, blue=1.000], blue]')
    self.assertSpread('red', 'blue', 6, use_hsb=True)

  def test_no_hsb(self):
    self.result = ('[red, [red=0.800, green=0.000, blue=0.200], [red=0.600, green=0.000, blue=0.400], [red=0.400, green=0.000, blue=0.600], [red=0.200, green=0.000, blue=0.800], blue]')
    self.assertSpread('red', 'blue', 6, use_hsb=False)

  def test_two_colors(self):
    self.result = ('[yellow, [red=0.600, green=1.000, blue=0.000], [red=0.200, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.200], [red=0.000, green=1.000, blue=0.600], cyan]')
    self.assertSpread('yellow', 'cyan', 6)

  def test_two_colors_identity(self):
    self.result = ('[yellow, [red=0.600, green=1.000, blue=0.000], [red=0.200, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.200], [red=0.000, green=1.000, blue=0.600], cyan]')
    self.assertSpread('yellow', 'cyan', 6, 'identity')

  def test_two_colors_square(self):
    self.result = ('[yellow, [red=0.920, green=1.000, blue=0.000], [red=0.680, green=1.000, blue=0.000], [red=0.280, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.280], cyan]')
    self.assertSpread(
      'yellow', 'cyan', 6, transform='square')

  def test_two_colors_sqrt(self):
    self.result = ('[yellow, [red=0.106, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.265], [red=0.000, green=1.000, blue=0.549], [red=0.000, green=1.000, blue=0.789], cyan]')
    self.assertSpread('yellow', 'cyan', 6,
                            transform='square+inverse')

  def test_inverse_square(self):
    self.result = ('[yellow, [red=0.106, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.265], [red=0.000, green=1.000, blue=0.549], [red=0.000, green=1.000, blue=0.789], cyan]')
    self.assertSpread('yellow', 'cyan',
                            6, transform='square+inverse')
  def test_exp(self):
    self.result = ('[yellow, '
                   '[red=0.742, green=1.000, blue=0.000], '
                   '[red=0.428, green=1.000, blue=0.000], '
                   '[red=0.043, green=1.000, blue=0.000], '
                   '[red=0.000, green=1.000, blue=0.426], '
                   'cyan]')
    self.assertSpread('yellow', 'cyan', 6, transform='exp')

  def test_inverse_exp(self):
    self.result = ('[yellow, [red=0.409, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.046], [red=0.000, green=1.000, blue=0.417], [red=0.000, green=1.000, blue=0.730], cyan]')
    self.assertSpread(
      'yellow', 'cyan', 6, transform='exp+inverse')

  def test_sine(self):
    self.result = ('[yellow, [red=0.809, green=1.000, blue=0.000], [red=0.309, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.309], [red=0.000, green=1.000, blue=0.809], cyan]')
    self.assertSpread('yellow', 'cyan', 6, transform='sine')

  def test_inverse_sine(self):
    self.result = ('[yellow, [red=0.410, green=1.000, blue=0.000], [red=0.128, green=1.000, blue=0.000], [red=0.000, green=1.000, blue=0.128], [red=0.000, green=1.000, blue=0.410], cyan]')
    self.assertSpread('yellow', 'cyan', 6, transform='sine+inverse')

  def test_name(self):
    self.result = ('[red, [red=1.000, green=0.200, blue=0.200], [red=1.000, green=0.400, blue=0.400], [red=1.000, green=0.600, blue=0.600], [red=1.000, green=0.800, blue=0.800], white]')
    self.assertSpread('red', 'white', 6)
