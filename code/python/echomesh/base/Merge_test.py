from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import Merge
from echomesh.util.TestCase import TestCase

class MergeTest(TestCase):
  def test_simple(self):
    self.assertEqual(Merge.merge({1: 2, 3: 5}, {1: 4, 2: 7}),
                     {1: 4, 2: 7, 3: 5})

  def test_simple(self):
    self.assertEqual(Merge.merge({1: 2, 3: 5}, {1: 4, 2: 7}, {1: 23, 5: 1000}),
                     {1: 23, 2: 7, 3: 5, 5: 1000})

  def test_simple(self):
    self.assertEqual(Merge.merge({1: 2, 3: 5}), {1: 2, 3: 5})

