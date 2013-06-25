from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
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

  if player == 'aplay':
    from echomesh.sound import Aplay
    return Aplay.play(**kwds)

  if player == 'pyaudio':
    from echomesh.sound.FilePlayer import FilePlayer
    return FilePlayer(element, **kwds)

  if player == 'client':
    raise Exception('client player is not yet implemented')

  raise Exception('Don\'t understand player %s' % player)
