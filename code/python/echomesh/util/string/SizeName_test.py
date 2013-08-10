from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.SizeName import size_name
from echomesh.util.TestCase import TestCase

class SizeNameTest(TestCase):
  def test_zero(self):
    self.assertEqual(size_name(0), '0')

  def test_FF(self):
    self.assertEqual(size_name(1023), '1023')

  def test_1K(self):
    self.assertEqual(size_name(1024), '1K')

  def test_1023K(self):
    self.assertEqual(size_name(1023 * 1024), '1023K')

  def test_1023K_2(self):
    self.assertEqual(size_name(1023 * 1024 + 511), '1023K')

  def test_1M(self):
    self.assertEqual(size_name(1023 * 1024 + 512), '1M')

  def test_1M2(self):
    self.assertEqual(size_name(1024 * 1024 - 1), '1M')

  def test_1M3(self):
    self.assertEqual(size_name(1024 * 1024), '1M')

  def test_1G(self):
    self.assertEqual(size_name(1024 * 1024 * 1024), '1G')

  def test_1G2(self):
    self.assertEqual(size_name(1024 * 1024 * 1024), '1G')
