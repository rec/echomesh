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

  def test_simple_write(self):
    self.assertEqual(self.buffer.write(3), [(0, 3)])
    self.assertEqual(self.buffer.begin(), 0)
    self.assertEqual(self.buffer.end(), 3)
    self.assertEqual(self.buffer.available(), 3)

  def test_write_all(self):
    self.assertEqual(self.buffer.write(32), [(0, 32)])
    self.assertEqual(self.buffer.begin(), 0)
    self.assertEqual(self.buffer.end(), 0)
    self.assertEqual(self.buffer.available(), 32)

  def test_full_buffer(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 0, 31)

    self.assertTrue(self.buffer.write(1), [(31, 32)])
    self.assertEqual(self.buffer.begin(), 0)
    self.assertEqual(self.buffer.end(), 0)
    self.assertEqual(self.buffer.available(), 32)
    self.assertTrue(self.buffer.write(1), [(0, 1)])
    self.assertEqual(self.buffer.available(), 32)
