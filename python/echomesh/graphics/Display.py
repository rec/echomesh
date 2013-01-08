from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Log

LOGGER = Log.logger(__name__)

def display(echomesh):
  if Config.is_enabled('display'):
    from graphics import Pi3dDisplay
    return Pi3dDisplay.Pi3dDisplay(echomesh)
