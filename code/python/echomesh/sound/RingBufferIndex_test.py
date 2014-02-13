from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.TestCase import TestCase

import cechomesh

class RingBufferIndex_test(TestCase):
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

  def test_write_full_buffer(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 0, 31)

    self.assertTrue(self.buffer.write(1), [(31, 32)])
    self.assertEqual(self.buffer.begin(), 0)
    self.assertEqual(self.buffer.end(), 0)
    self.assertEqual(self.buffer.available(), 32)
    self.assertTrue(self.buffer.write(1), [(0, 1)])
    self.assertEqual(self.buffer.available(), 32)

  def test_write_overrun(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 0, 31)
    self.assertTrue(self.buffer.write(2), [(31, 32), (0, 1)])
    self.assertEqual(self.buffer.available(), 32)

  def test_write_wrap(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 24, 8)
    self.assertEqual(self.buffer.available(), 16)
    self.assertTrue(self.buffer.write(12), [(24, 32), (0, 8)])
    self.assertEqual(self.buffer.available(), 28)

  def test_simple_read(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 0, 8)
    self.assertTrue(self.buffer.read(6), [(0, 6)])
    self.assertEqual(self.buffer.available(), 2)

  def test_read_underrun(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 0, 8)
    self.assertTrue(self.buffer.read(10), [(0, 8)])
    self.assertEqual(self.buffer.available(), 0)
    self.assertEqual(self.buffer.begin(), 8)
    self.assertEqual(self.buffer.end(), 8)

  def test_read_wrap(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 28, 4)
    self.assertTrue(self.buffer.read(6), [(28, 32), (0, 2)])
    self.assertEqual(self.buffer.available(), 2)

  def test_read_wrap_underrun(self):
    self.buffer = cechomesh.PyRingBufferIndex(32, 28, 4)
    self.assertTrue(self.buffer.read(12), [(28, 32), (0, 4)])
    self.assertEqual(self.buffer.available(), 0)


