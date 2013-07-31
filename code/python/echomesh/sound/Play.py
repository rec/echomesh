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


def _set_player(player, element,
               level=1, pan=0, loops=1, begin=0, end=INF, length=INF, **kwds):
  player._element = element
  player._file = kwds.pop('file')
  player._filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(player._file)
  if kwds:
    LOGGER.error('Unused keywords %s', kwds)
  player._passthrough = (level == 1 and pan == 0)

  player._length = length
  player._level = Expression(level, element)
  player._pan = Expression(pan, element)
  player._loops = loops
  player._begin = begin
  player._end = end


def play(element, **kwds):
  if 'type' in kwds:
    del kwds['type']

  if 'player' in kwds:
    player = kwds['player']
    del kwds['player']
  else:
    player = Config.get('audio', 'output', 'player')

  return _get_player(player)(element, **kwds)
