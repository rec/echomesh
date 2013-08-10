from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.expression import Transform
from echomesh.util.TestCase import TestCase

class TransformTest(TestCase):
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
