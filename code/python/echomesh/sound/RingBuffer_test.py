from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.TestCase import TestCase

import cechomesh

class RingBuffer_test(TestCase):
  def setUp(self):
    self.buffer = cechomesh.PyRingBufferIndex(32)

  def test_empty(self):
    self.assertEqual(self.buffer.available(), 0)
    self.assertEqual(self.buffer.read(16), [])
    self.assertEqual(self.buffer.read(64), [])

  def test_write(self):
    self.assertEqual(self.buffer.write(3), [(0, 3)])
    self.assertEqual(self.buffer.begin(), 0)
    self.assertEqual(self.buffer.end(), 3)
    self.assertEqual(self.buffer.available(), 3)
    self.assertTrue(self.buffer.write(28), [(3, 31)])
    self.assertEqual(self.buffer.available(), 31)
