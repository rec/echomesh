from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.sound import Level
from echomesh.util.registry.Registry import Registry


def _system_register():
  CONSTANTS = {
    'e': [math.e, True],
    'level': [Level.input_level, False],
    'pi': [math.pi, True],
    'random': [random.random, False],
    'time': [time.time, False],
    }

  register = Registry('System')
  for name, value in CONSTANTS.items():
    register.register(value, function_name=name)
  return register

SYSTEM = _system_register()
