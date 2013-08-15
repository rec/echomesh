from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log

LOGGER = Log.logger(__name__)

INF = float('inf')

def _get_player(player):
  if player == 'aplay':
    from echomesh.sound import AplayPlayer
    return AplayPlayer.AplayPlayer

  if player == 'pyaudio':
    from echomesh.sound import PyaudioPlayer
    return PyaudioPlayer.PyaudioPlayer

  if player == 'client':
    from echomesh.sound import ClientPlayer
    return ClientPlayer.ClientPlayer

  raise Exception('Don\'t understand player %s' % player)

def play(element, **kwds):
  if 'type' in kwds:
    del kwds['type']

  if 'player' in kwds:
    player = kwds['player']
    del kwds['player']
  else:
    player = Config.get('audio', 'output', 'player')

  return _get_player(player)(element, **kwds)
