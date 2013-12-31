from __future__ import absolute_import, division, print_function, unicode_literals

import math

import cechomesh

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

class CTransformTest(TestCase):
  def assertTransform(self, name):
    tr = cechomesh.Transform(name)
    # print('1.', name)
    self.assertNear(tr.apply(0), 0)
    self.assertNear(tr.inverse(0), 0)
    self.assertNear(tr.apply(1), 1)
    self.assertNear(tr.inverse(1), 1)

    VALUES = 0, 1, 0.5, 1 / 3, 2 / 3
    for v in VALUES:
      # print('2.', v, tr.apply(v), tr.inverse(v))
      self.assertNear(v, tr.apply(tr.inverse(v)))
      self.assertNear(v, tr.inverse(tr.apply(v)))

  def test_identity(self):
    self.assertTransform("identity")

  def test_square(self):
    self.assertTransform("square")

  def test_cube(self):
    self.assertTransform("cube")

  def test_sine(self):
    self.assertTransform("sine")

  def test_exp(self):
    self.assertTransform("exp")
