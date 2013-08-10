from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math import Interval
from echomesh.util.TestCase import TestCase

INF = float('inf')

class IntervalTest(TestCase):
  def test_empty(self):
    self.assertEqual(Interval.interval(), (INF, 0, INF, 1))

  def test_one(self):
    self.assertEqual(Interval.interval(10), (10, 0, 9, 1))

  def test_one_arg(self):
    self.assertEqual(Interval.interval(count=10), (10, 0, 9, 1))

  def test_begin_only(self):
    self.assertEqual(Interval.interval(begin=10), (INF, 10, INF, 1))

  def test_end_only(self):
    self.assertEqual(Interval.interval(end=10), (11, 0, 10, 1))

  def test_begin_and_end(self):
    self.assertEqual(Interval.interval(begin=10, end=15), (6, 10, 15, 1))

  def test_begin_and_count(self):
    self.assertEqual(Interval.interval(begin=10, count=5), (5, 10, 14, 1))

  def test_end_and_count(self):
    self.assertEqual(Interval.interval(end=10, count=5), (5, 6, 10, 1))

  def test_begin_after_end(self):
    self.assertEqual(Interval.interval(begin=10, end=5), (6, 10, 5, -1))

  def test_negative_skip(self):
    self.assertEqual(Interval.interval(begin=10, count=3, skip=-2), (3, 10, 6, -2))

  def test_begin_after_end_negative_skip(self):
    self.assertEqual(Interval.interval(begin=10, end=3, skip=-2), (4, 10, 3, -2))

  def test_begin_after_end_skip(self):
    self.assertEqual(Interval.interval(begin=10, end=3, count=3), (3, 10, 3, -2))

