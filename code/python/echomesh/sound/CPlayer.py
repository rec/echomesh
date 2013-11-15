from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh.AudioPlayer import AudioPlayer

from echomesh.sound import PlayerSetter
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class CPlayer(Runnable):
  def __init__(self, element, level=1, pan=0, loops=1, length=_INF, **kwds):
    super(CPlayer, self).__init__()
    PlayerSetter.evaluate_player(
      self, element, level=level, pan=pan, loops=loops, length=length, **kwds)
    player = AudioPlayer(self)
    self._on_run = player.run
    self._on_stop = player.stop
    self._on_stop = player.pause
    self.unload = player.unload

