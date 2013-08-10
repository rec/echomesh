# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.Envelope import Envelope
from echomesh.util.TestCase import TestCase

ENVELOPE = Envelope({0: 5.0, 1: 10.0, 2: 20.0})
ENVELOPE2 = Envelope({0: [5.0, 50.0], 1: [10.0, 100.0], 2: [20.0, 200.0]})

class EnvelopeTest(TestCase):
  def test_before(self):
    self.assertEqual(ENVELOPE.interpolate(-1), 5.0)

  def test_start(self):
    self.assertEqual(ENVELOPE.interpolate(0), 5.0)

  def test_middle(self):
    self.assertEqual(ENVELOPE.interpolate(0.5), 7.5)

  def test_further(self):
    self.assertEqual(ENVELOPE.interpolate(1), 10.0)

  def test_near_end(self):
    self.assertEqual(ENVELOPE.interpolate(1.5), 15.0)

  def test_end(self):
    self.assertEqual(ENVELOPE.interpolate(2), 20.0)

  def test_after_end(self):
    self.assertEqual(ENVELOPE.interpolate(3), 20.0)

  def test_before_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(-1), [5.0, 50.0])

  def test_start_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(0), [5.0, 50.0])

  def test_middle_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(0.5), [7.5, 75.0])

  def test_further_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(1), [10.0, 100.0])

  def test_loop_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(1.5), [15.0, 150.0])

  def test_end_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(2), [20.0, 200.0])

  def test_after_end_multi(self):
    self.assertEqual(ENVELOPE2.interpolate(3), [20.0, 200.0])

