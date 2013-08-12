from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorTable
from echomesh.util.TestCase import TestCase


class TestColorTable(TestCase):
  def test_black(self):
    self.assertEqual(ColorTable.to_color('black'), (0.0, 0.0, 0.0))

  def test_white(self):
    self.assertEqual(ColorTable.to_color('white'), (1.0, 1.0, 1.0))

  def test_pink(self):
    self.assertEqual(ColorTable.to_color('pink'),
                     (1.0, 0.7529411764705882, 0.796078431372549))

  def test_gray(self):
    self.assertEqual(ColorTable.to_color('gray'),
                     (0.5019607843137255, 0.5019607843137255, 0.5019607843137255))

  def test_grey(self):
    self.assertEqual(ColorTable.to_color('grey'),
                     (0.5019607843137255, 0.5019607843137255, 0.5019607843137255))

  def test_grey3(self):
    self.assertEqual(ColorTable.to_color('grey 3'),
                     (0.03137254901960784, 0.03137254901960784, 0.03137254901960784))

