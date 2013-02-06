import numpy

import colorsys

GAMMA = 2.5
GAMMA_TABLE_STEPS = 512

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

def gamma_correct(x, gamma=GAMMA):
  return numpy.power(x, gamma)

def make_gamma_table(out_range=128, steps=GAMMA_TABLE_STEPS, gamma=GAMMA):
  step_iterator = (i / (steps - 1) for i in range(steps))
  corrected = (numpy.power(x, gamma) for x in step_iterator)
  return [int(0.5 + (out_range - 1) * c) for c in corrected]

GAMMA_TABLE = make_gamma_table()

def gamma_correct(x, gamma_table=GAMMA_TABLE):
  steps = len(gamma_table)
  return gamma_table[min(x * steps, steps - 1)]

class ChannelOrder(object):
  RGB = lambda r, g, b: (r, g, b)
  GRB = lambda r, g, b: (g, r, b)
  BRG = lambda r, g, b: (b, r, g)

