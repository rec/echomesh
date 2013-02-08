from __future__ import absolute_import, division, print_function, unicode_literals

import numpy

GAMMA = 2.5
GAMMA_TABLE_STEPS = 512

# Inspired by
# https://github.com/adammhaile/RPi-LPD8806/blob/master/LPD8806.py#L90

class GammaTable(object):
  def __init__(self, out_range=128, steps=GAMMA_TABLE_STEPS, gamma=GAMMA):
    self.steps = steps
    step_iterator = (i / (steps - 1) for i in range(steps))
    corrected = (numpy.power(x, gamma) for x in step_iterator)
    self.table = [int(0.5 + (out_range - 1) * c) for c in corrected]

  def correct(self, x):
    return self.table[min(x * self.steps, self.steps - 1)]

GAMMA_TABLE = GammaTable()

correct = GAMMA_TABLE.correct
