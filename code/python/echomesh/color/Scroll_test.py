from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color.Scroll import scroll

from echomesh.util.TestCase import TestCase

class ScrollTest(TestCase):
  def setUp(self):
    self.data = [1, 2, 3, 4, 10, 20, 30, 40, 100, 200, 300, 400]

  def doTest(self, dx, dy, expected):
    self.assertEquals(scroll(self.data, 4, dx, dy, 0), expected)

  def test_empty(self):
    self.doTest(0, 0, self.data)

  def test_one_right(self):
    self.doTest(1, 0, [0, 1, 2, 3, 0, 10, 20, 30, 0, 100, 200, 300])

  def test_three_right(self):
    self.doTest(3, 0, [0, 0, 0, 1, 0, 0, 0, 10, 0, 0, 0, 100])

  def test_four_right(self):
    self.doTest(4, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def test_five_right(self):
    self.doTest(5, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def test_one_left(self):
    self.doTest(-1, 0, [2, 3, 4, 0, 20, 30, 40, 0, 200, 300, 400, 0])

  def test_three_left(self):
    self.doTest(-3, 0, [4, 0, 0, 0, 40, 0, 0, 0, 400, 0, 0, 0])

  def test_four_left(self):
    self.doTest(-4, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def test_five_left(self):
    self.doTest(-5, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def test_one_down(self):
    self.doTest(0, 1, [0, 0, 0, 0, 1, 2, 3, 4, 10, 20, 30, 40])

  def test_two_down(self):
    self.doTest(0, 2, [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4])

  def test_three_down(self):
    self.doTest(0, 3, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def test_four_down(self):
    self.doTest(0, 4, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

