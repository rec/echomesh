from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.sound import Level
from echomesh.util import Registry

def _system_register():
  register = Registry.Registry('System')
  register.register_all(
    e=[[math.e, True]],
    level=[[Level.input_level, False]],
    pi=[[math.pi, True]],
    random=[[random.random, False]],
    time=[[time.time, False]],
    )
  return register

SYSTEM = _system_register()
