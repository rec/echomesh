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

  def test_resize(self):
    self.cl.resize(2)
    self.assertResult('[none, none]')
    self.cl.resize(0)
    self.assertResult('[]')

