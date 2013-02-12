from __future__ import absolute_import, division, print_function, unicode_literals

# Inspired by
# https://github.com/adammhaile/RPi-LPD8806/blob/master/LPD8806.py#L90

from echomesh.util import ImportIf
numpy = ImportIf.imp('numpy')

def wheel_color(rotation=0):
  """
  Return a color from a color wheel.

  Arguments:
    *rotation*
      The amount of rotation of the wheel.  0 through 1 goes through a complete
      rotation, but you can use numbers greater than 1 or negative numbers.

  """
  rgb = numpy.array([0.0, 0.0, 0.0])

  # Divide the rotation into three segments
  rotation = (rotation % 1.0) * 3.0
  segment = int(rotation)

  rgb[segment] = rotation - segment
  rgb[(segment + 1) % 3] = 1.0 - rgb[segment]

  return rgb
