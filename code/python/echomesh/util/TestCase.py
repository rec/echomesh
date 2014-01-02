from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Path

Path.fix_sys_path()

import numpy
import unittest

class TestCase(unittest.TestCase):
  EPSILON = 0.000001

  def assertNear(self, x, y, msg=None):
    try:
      lx, ly = len(x), len(y)
    except:
      self.assertTrue(abs(x - y) < self.EPSILON, msg or ('%s != %s' % (x, y)))
    else:
      self.assertEquals(lx, ly)
      for xi, yi in zip(x, y):
        self.assertNear(xi, yi, msg)

  def assertArrayEquals(self, x, y):
    x, y = numpy.array(x), numpy.array(y)
    self.assertEqual(x.shape, y.shape)
    columns, rows = x.shape
    for i in range(columns):
      for j in range(rows):
        msg = 'for [%d][%d], %s != %s' % (i, j, x[i][j], y[i][j])
        self.assertNear(x[i][j], y[i][j], msg)


