from __future__ import absolute_import, division, print_function, unicode_literals

import math

from pyparsing import Expressions
from pyparsing.pyparsing import ParseException
from echomesh.util.TestCase import TestCase

class ParsingTest(TestCase):
  def assertParse(self, s, expected):
    try:
      result = Expressions.evaluate(s)
    except ParseException as pe:
      result = 'failed parse: ' + str(pe)
    except Exception as e:
      result = 'failed eval: ' + str(e)
    self.assertEqual(result, expected)

  def test_x(self):
    self.assertParse('9', 9)

  def test_x(self):
    self.assertParse('-9', -9)

  def test_x(self):
    self.assertParse('--9', 9)

  def test_x(self):
    self.assertParse('-E', -2.718281828459045)

  def test_x(self):
    self.assertParse('9 + 3 + 6', 18)

  def test_x(self):
    self.assertParse('9 + 3 / 11', 9.272727272727273)

  def test_x(self):
    self.assertParse('(9 + 3)', 12)

  def test_x(self):
    self.assertParse('(9+3) / 11', 1.0909090909090908)

  def test_x(self):
    self.assertParse('9 - 12 - 6', -9)

  def test_x(self):
    self.assertParse('9 - (12 - 6)', 3)

  def test_x(self):
    self.assertParse('2*3.14159', 6.28318)

  def test_x(self):
    self.assertParse('3.1415926535*3.1415926535 / 10', 0.9869604400525172)

  def test_x(self):
    self.assertParse('PI * PI / 10', 0.9869604401089358)

  def test_x(self):
    self.assertParse('PI*PI/10', 0.9869604401089358)

  def test_x(self):
    self.assertParse('PI^2', 9.869604401089358)

  def test_x(self):
    self.assertParse('round(PI^2)', 10.0)

  def test_x(self):
    self.assertParse('6.02E23 * 8.048', 4.844896e+24)

  def test_x(self):
    self.assertParse('e / 3', 0.9060939428196817)

  def test_x(self):
    self.assertParse('sin(PI/2)', 1.0)

  def test_x(self):
    self.assertParse('trunc(E)', 2)

  def test_x(self):
    self.assertParse('trunc(-E)', -2)

  def test_x(self):
    self.assertParse('round(E)', 3.0)

  def test_x(self):
    self.assertParse('round(-E)', -3.0)

  def test_x(self):
    self.assertParse('E^PI', 23.140692632779263)

  def test_x(self):
    self.assertParse('2^3^2', 512)

  def test_x(self):
    self.assertParse('2^3+2', 10)

  def test_x(self):
    self.assertParse('2^3+5', 13)

  def test_x(self):
    self.assertParse('2^9', 512)

  def test_x(self):
    self.assertParse('sgn(-2)', -1)

  def test_x(self):
    self.assertParse('sgn(0)', 0)

  def test_x(self):
    self.assertParse('foo(0.1)', u'failed eval: invalid identifier "foo"')

  def test_x(self):
    self.assertParse('sgn(0.1)', 1)

# >>> test_parse('0x01')
# 1
#
# >>> test_parse('0xff')  # Doesn't yet work.
# 255
