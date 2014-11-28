from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.TestCase import TestCase

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
        self.assertOutput(
          {'type': 'offset', 'offset': 4},
          [1, 2, 3, 4],
          [None, None, None, None, 1, 2, 3, 4])

    def test_negative(self):
        self.assertOutput(
          {'type': 'offset', 'offset': -4},
          [1, 2, 3, 4, 5, 6],
          [5, 6])

    def test_zero(self):
        self.assertOutput(
          {'type': 'offset', 'offset': 0},
          [1, 2, 3, 4],
          [1, 2, 3, 4])

    def test_length(self):
        self.assertOutput(
          {'type': 'offset', 'offset': 4, 'length': 6},
          [1, 2, 3, 4],
          [None, None, None, None, 1, 2])
