from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

def next_poisson(mean):
  return mean * -math.log(random.random())
