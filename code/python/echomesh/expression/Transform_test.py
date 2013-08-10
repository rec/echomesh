from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.expression import Transform

from unittest import TestCase

EPSILON = 0.000001

class TransformTest(TestCase):
  def assertNear(self, x, y):
    self.assertTrue(abs(x - y) < EPSILON, '%s != %s' % (x, y))

  def assertTransform(self, tr):
    s, t = tr
    self.assertNear(s(0), 0)
    self.assertNear(t(0), 0)
    self.assertNear(s(1), 1)
    self.assertNear(t(1), 1)

    VALUES = 0, 1, 0.5, 1 / 3, 2 / 3
    for v in VALUES:
      self.assertNear(v, s(t(v)))
      self.assertNear(v, t(s(v)))

  def test_identity(self):
    self.assertTransform(Transform.IDENTITY)

  def test_square(self):
    self.assertTransform(Transform.SQUARE)

  def test_cube(self):
    self.assertTransform(Transform.power(3))

  def test_sine(self):
    self.assertTransform(Transform.SINE)

  def test_exp(self):
    self.assertTransform(Transform.EXP)
