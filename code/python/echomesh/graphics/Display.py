from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util.thread import Openable

LOGGER = Log.logger(__name__)

def display(echomesh):
  if Config.get('pi3d', 'enable'):
    from echomesh.graphics import Pi3dDisplay
    return Pi3dDisplay.Pi3dDisplay(echomesh)
