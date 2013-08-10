from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math.WeightedRandom import WeightedRandom
from echomesh.util.TestCase import TestCase

class WeighedRandomTest(TestCase):
  def test_empty(self):
    wr = WeightedRandom([None])
    self.assertEqual(wr.select(), 0)

  def test_single(self):
    wr = WeightedRandom([1])
    self.assertEqual(wr.select(), 0)

  def test_double_empty(self):
    wr = WeightedRandom([None, None])
    self.assertEqual(wr.select(0.4), 0)
    self.assertEqual(wr.select(0.6), 1)

  def test_empty_right(self):
    wr = WeightedRandom([1, None])
    self.assertEqual(wr.select(0.4), 0)
    self.assertEqual(wr.select(0.6), 1)

  def test_double(self):
    wr = WeightedRandom([1, 3])
    self.assertEqual(wr.select(0.2), 0)
    self.assertEqual(wr.select(0.25), 1)
    self.assertEqual(wr.select(0.4), 1)
    self.assertEqual(wr.select(0.6), 1)

  def test_squares(self):
    v = [1, 4, 9, 25]
    s = 1 / sum(v)
    wr = WeightedRandom(v)
    self.assertEqual(wr.select(0), 0)
    self.assertEqual(wr.select(s), 1)
    self.assertEqual(wr.select(5 * s), 2)
    self.assertEqual(wr.select(14 * s), 3)
    self.assertEqual(wr.select(39 * s), 4)

  def test_squares_missing(self):
    wr = WeightedRandom([1, None, 9, None, 20])
    s = 1 / 50
    self.assertEqual(wr.select(s / 2), 0)
    self.assertEqual(wr.select(s), 1)
    self.assertEqual(wr.select(10 * s), 1)
    self.assertEqual(wr.select(11 * s), 2)
    self.assertEqual(wr.select(19 * s), 2)
    self.assertEqual(wr.select(20 * s), 3)
    self.assertEqual(wr.select(29 * s), 3)
    self.assertEqual(wr.select(30 * s), 4)
    self.assertEqual(wr.select(50 * s), 5)
