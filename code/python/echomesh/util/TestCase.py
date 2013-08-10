from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import unittest

class TestCase(unittest.TestCase):
  EPSILON = 0.000001

  def assertNear(self, x, y, msg=None):
    self.assertTrue(abs(x - y) < self.EPSILON, msg or ('%s != %s' % (x, y)))

  def assertArrayEquals(self, x, y):
    x, y = numpy.array(x), numpy.array(y)
    self.assertEqual(x.shape, y.shape)
    columns, rows = x.shape
    for i in range(columns):
      for j in range(rows):
        msg = 'for [%d][%d], %s != %s' % (i, j, x[i][j], y[i][j])
        self.assertNear(x[i][j], y[i][j], msg)


