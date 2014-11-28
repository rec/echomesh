from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.TestCase import TestCase

class BidirectionalTest(TestCase):
    def test_start_forward(self):
        self.assertOutput(
          {'type': 'bidi', 'width': 4},
          ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
          ['a', 'b', 'c', 'd', 'g', 'f', 'e'])

    def test_start_backward(self):
        self.assertOutput(
          {'type': 'bidi', 'width': 4, 'start_forward': False},
          ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
          ['d', 'c', 'b', 'a', 'e', 'f', 'g'])

    def test_long(self):
        self.assertOutput(
          {'type': 'bidi', 'width': 2},
          ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
          ['a', 'b', 'd', 'c', 'e', 'f', 'h', 'g', 'i', 'j'])
