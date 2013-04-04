from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.expression import Units

SPEED_NAME = None
SPEED = None
MIN_SPEED = 1E-6

def speed():
  global SPEED, SPEED_NAME
  s = Config.get('speed')
  if SPEED_NAME != s:
    SPEED = max(MIN_SPEED, Units.convert(s))
    SPEED_NAME = s
  return SPEED
