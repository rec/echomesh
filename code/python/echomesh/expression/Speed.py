from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from echomesh.base import Config
from echomesh.expression import Units

SPEED = None
MIN_SPEED = 1E-6

class SpeedClient(object):
  def config_update(self, get):
    global SPEED
    SPEED = max(MIN_SPEED, Units.convert(get('speed')))

_CLIENT = SpeedClient()

def speed():
  if SPEED is None:
    Config.add_client(_CLIENT)
  return SPEED

