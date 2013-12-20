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

class OffsetTest(TestCase):
  def test_positive(self):
    output = make_output(DESCRIPTION_POSITIVE)
    output.emit_output([1, 2, 3, 4])
    self.assertEqual(output.output[0].data, [None, None, None, None, 1, 2, 3, 4])
