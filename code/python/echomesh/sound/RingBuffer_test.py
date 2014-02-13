from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.TestCase import TestCase

import cechomesh

class RingBuffer_test(TestCase):
  def setUp(self):
    self.buffer = cechomesh.AudioRingBuffer(1, 16)

  def test_empty(self):
    self.assertEqual(self.buffer.available(), 0)
    data = []
    self.assertEqual(self.buffer.read(16, data), 0)
    self.assertEqual(data, [[]])

  def test_all(self):
    self.assertEqual(self.buffer.write([range(16)]), 16)
    data = []
    self.assertEqual(self.buffer.read(16, data), 16)
    self.assertEqual(data, [[float(i) for i in range(16)]])

