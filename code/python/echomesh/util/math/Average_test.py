from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math import Average
from echomesh.util.TestCase import TestCase

class AverageTest(TestCase):
  def test_grouped(self):
    self.assertEqual(list(Average.average(range(8), grouped_window=2)),
                     [0.5, 2.5, 4.5, 6.5])

  def test_grouped_moving(self):
    result = list(Average.average(range(8), grouped_window=2, moving_window=2))
    self.assertEqual(result, [1.5, 3.5, 5.5])
