from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import WheelColor
from echomesh.util.TestCase import TestCase

EXPECTED = [
  [ 0.,  1.,  0.],
  [ 0.3,  0.7,  0. ],
  [ 0.6,  0.4,  0. ],
  [ 0.9,  0.1,  0. ],
  [ 0. ,  0.2,  0.8],
  [ 0. ,  0.5,  0.5],
  [ 0. ,  0.8,  0.2],
  [ 0.9,  0. ,  0.1],
  [ 0.6,  0. ,  0.4],
  [ 0.3,  0. ,  0.7],
  [ 0.,  1.,  0.]]

class TestWheelColor(TestCase):
  def test_several(self):
    result = [WheelColor.wheel_color(r / 10.0) for r in range(11)]
    self.assertArrayEquals(result, EXPECTED)
