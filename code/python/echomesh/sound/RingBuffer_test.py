from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.TestCase import TestCase

import cechomesh

class RingBuffer_test(TestCase):
  def setUp(self):
    self.buffer = cechomesh.AudioRingBuffer(1, 32)

  def test_empty(self):
    self.assertEqual(self.buffer.sample_count(), 0)
    data = []
    self.assertFalse(self.buffer.read(16, data))
    self.assertFalse(self.buffer.read(64, data))

  def test_append(self):
    self.assertTrue(self.buffer.write([range(3)]))
    self.assertEqual(self.buffer.sample_count(), 3)
    self.assertTrue(self.buffer.write([range(28)]))
    self.assertEqual(self.buffer.sample_count(), 31)
