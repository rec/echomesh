from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.expression.RawExpression import RawExpression

from unittest import TestCase

def evaluate(expression):
  return RawExpression(expression, None).evaluate()

class TextExpression(TestCase):
  def assertEvaluate(self, expression, result):
    self.assertEqual(evaluate(expression), result)

  def assertFail(self, expression, error):
    try:
      result = evaluate(expression)
    except Exception as e:
      self.assertEqual(str(e), error)
    else:
      self.assertTrue(False, 'Expected an error but got result %s' % result)

  def test_simple(self):
    self.assertEvaluate('2+2', 4)

  def test_three_terms(self):
    self.assertEvaluate('2*2+2', 6)

  def test_parens(self):
    self.assertEvaluate('2*(2+2)', 8)

  def test_many_parens(self):
    self.assertEvaluate('(2*((((2)+2))))', 8)

  def test_sin(self):
    self.assertEvaluate('2+sin(0)', 2.0)

  def test_trunc(self):
    self.assertEvaluate('2 + trunc(1.2)', 3)

  def test_minus_cos(self):
    self.assertEvaluate('-cos(0)', -1.0)

  def test_pi(self):
    self.assertEvaluate('3 + sys.pi', 3 + math.pi)

  def test_powers(self):
    self.assertEvaluate('2 ** 3 ** 2', 512)

  def test_powers_parens(self):
    self.assertEvaluate('(2 ** 3) ** 2', 64)

  def test_failure(self):
    self.assertFail('2 +', 'Expected end of text (at char 2), (line:1, col:3)')

