from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import ColorList

from echomesh.util.TestCase import TestCase

class ColorListTest(TestCase):
  def test_empty(self):
    self.assertEqual(str(ColorList()), 'ColorList()')

  def test_single(self):
    c = ColorList()
    c.append("red")
    self.assertEqual(str(c), 'ColorList(Color(red))')
