from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import make_output
from echomesh.util.TestCase import TestCase

DESCRIPTION_POSITIVE = {
  'type': 'offset',
  'offset': 4,
  'output': {'type': 'test'},
}

DESCRIPTION_NEGATIVE = {
  'type': 'offset',
  'offset': -4,
  'output': {'type': 'test'},
}

DESCRIPTION_ZERO = {
  'type': 'offset',
  'offset': 0,
  'output': {'type': 'test'},
}

DESCRIPTION_LENGTH = {
  'type': 'offset',
  'offset': 4,
  'length': 6,
  'output': {'type': 'test'},
}


class OffsetTest(TestCase):
  def test_positive(self):
    output = make_output(DESCRIPTION_POSITIVE)
    output.emit_output([1, 2, 3, 4])
    self.assertEqual(output.output[0].data, [None, None, None, None, 1, 2, 3, 4])

  def test_negative(self):
    output = make_output(DESCRIPTION_NEGATIVE)
    output.emit_output([1, 2, 3, 4, 5, 6])
    self.assertEqual(output.output[0].data, [5, 6])

  def test_zero(self):
    output = make_output(DESCRIPTION_ZERO)
    output.emit_output([1, 2, 3, 4])
    self.assertEqual(output.output[0].data, [1, 2, 3, 4])

  def test_length(self):
    output = make_output(DESCRIPTION_LENGTH)
    output.emit_output([1, 2, 3, 4])
    self.assertEqual(output.output[0].data, [None, None, None, None, 1, 2])

