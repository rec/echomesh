from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.sound import CPlayer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def play(element, **kwds):
  if 'type' in kwds:
    del kwds['type']

  if 'player' in kwds:
    player = kwds['player']
    del kwds['player']
  else:
    player = Config.get('audio', 'output', 'player')

  return CPlayer.Cplayer(player)(element, **kwds)
