from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import ColorList

from echomesh.util.TestCase import TestCase

class ColorListTest(TestCase):
  def setUp(self):
    self.cl = ColorList()

  def assertResult(self, s):
    self.assertEqual(str(self.cl), s)

  def test_single(self):
    self.cl.append("red")
    self.assertResult('[red]')

  def test_empty(self):
    self.assertResult('[]')

  def test_appendn(self):
    self.cl.append("red")
    self.assertResult('[red]')
    self.assertRaises(ValueError, self.cl.append, 'glug')
    self.assertResult('[red]')

  def test_sort(self):
    self.cl.extend(['green', 'red', 'blue'])
    self.cl.sort()
    self.assertResult('[blue, green, red]')

  def test_count(self):
    self.cl.extend(['green', 'red', 'blue', 'red', 'pink'])
    self.assertEqual(self.cl.count('green'), 1)
    self.assertEqual(self.cl.count('yellow'), 0)
    self.assertEqual(self.cl.count('red'), 2)

