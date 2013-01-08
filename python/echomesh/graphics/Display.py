from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.config import Config
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def display(echomesh):
  if Config.is_enabled('display'):
    from echomesh.graphics import Pi3dDisplay
    return Pi3dDisplay.Pi3dDisplay(echomesh)
