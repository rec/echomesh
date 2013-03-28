from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.util import Registry

def _system_register():
  register = Registry.Registry('System')
  register.register_all(
    e=[[math.e, False]],
    pi=[[math.pi, False]],
    random=[[random.random, True]],
    time=[[time.time, True]],
    )
  return register

SYSTEM = _system_register()
